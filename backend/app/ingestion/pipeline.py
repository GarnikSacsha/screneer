from __future__ import annotations

import asyncio
from dataclasses import dataclass, replace
from datetime import datetime, timezone
from typing import Any

from app.anomalies.rules import detect_market_anomalies, detect_sector_anomalies
from app.core.config import load_thresholds, load_universe
from app.db.bootstrap import create_schema, seed_universe
from app.db.repositories import (
    insert_anomaly_events,
    insert_market_metrics,
    insert_sector_metrics,
    load_market_lookup,
    load_sector_lookup,
    upsert_candles,
)
from app.db.session import AsyncSessionLocal
from app.domain.entities import AnomalyEvent, MarketMetrics, SectorMetrics
from app.exchanges.binance import BinanceFuturesAdapter
from app.ingestion.binance_snapshot import BinanceMarketSnapshot, fetch_binance_market_snapshot
from app.metrics.engine import calculate_market_metrics, calculate_sector_metrics
from app.state import redis_keys
from app.state.flow_store import LiquidationWindow, get_liquidation_window
from app.state.redis_store import (
    get_redis_client,
    replace_latest_market_metrics,
    replace_latest_sector_metrics,
    save_events,
)


@dataclass(frozen=True)
class SnapshotResult:
    ts: datetime
    market_metrics: list[MarketMetrics]
    sector_metrics: list[SectorMetrics]
    events: list[AnomalyEvent]
    errors: dict[str, str]


EVENT_CONFIG_KEYS = {
    "VOLUME_SPIKE": "volume_spike",
    "OI_EXPANSION": "oi_expansion",
    "PRICE_BREAKOUT": "price_breakout",
    "SQUEEZE_RISK": "squeeze_risk",
    "SECTOR_LEADER": "sector_leader",
    "LAGGING_ASSET": "lagging_asset",
    "ABSORPTION_CANDIDATE": "absorption_candidate",
}


def enabled_binance_markets(universe: dict[str, Any]) -> list[dict[str, Any]]:
    return [
        item
        for item in universe.get("markets", [])
        if item.get("enabled", True)
        and item.get("exchange") == "binance"
        and item.get("market_type") == "futures"
    ]


def _asset_symbol_map(markets: list[dict[str, Any]]) -> dict[str, str]:
    return {market["asset"]: market["symbol"] for market in markets}


def _primary_sector_by_symbol(markets: list[dict[str, Any]]) -> dict[str, str]:
    return {market["symbol"]: market["sector"] for market in markets if market.get("sector")}


def _configured_sector_counts(universe: dict[str, Any], markets: list[dict[str, Any]]) -> dict[str, int]:
    asset_to_symbol = _asset_symbol_map(markets)
    counts: dict[str, int] = {}
    for sector, members in universe.get("sectors", {}).items():
        counts[sector] = sum(1 for asset in members if asset in asset_to_symbol)
    return counts


def _metrics_by_sector(
    universe: dict[str, Any],
    markets: list[dict[str, Any]],
    metrics_by_symbol: dict[str, MarketMetrics],
) -> dict[str, list[MarketMetrics]]:
    asset_to_symbol = _asset_symbol_map(markets)
    grouped: dict[str, list[MarketMetrics]] = {}
    for sector, members in universe.get("sectors", {}).items():
        for asset in members:
            symbol = asset_to_symbol.get(asset)
            metric = metrics_by_symbol.get(symbol) if symbol else None
            if metric:
                grouped.setdefault(sector, []).append(metric)
    return grouped


async def _fetch_snapshots(markets: list[dict[str, Any]], concurrency: int = 4) -> tuple[list[BinanceMarketSnapshot], dict[str, str]]:
    adapter = BinanceFuturesAdapter()
    semaphore = asyncio.Semaphore(concurrency)
    errors: dict[str, str] = {}

    async def fetch_one(symbol: str) -> BinanceMarketSnapshot | None:
        async with semaphore:
            try:
                return await fetch_binance_market_snapshot(symbol, adapter)
            except Exception as exc:
                errors[symbol] = f"{type(exc).__name__}: {exc}"
                return None

    results = await asyncio.gather(*(fetch_one(market["symbol"]) for market in markets))
    return [item for item in results if item is not None], errors


async def _dedupe_events(client: Any, events: list[AnomalyEvent], thresholds: dict[str, Any]) -> list[AnomalyEvent]:
    deduped: list[AnomalyEvent] = []
    event_thresholds = thresholds.get("events", {})
    for event in events:
        config_key = EVENT_CONFIG_KEYS.get(event.event_type, event.event_type.lower())
        ttl = int(event_thresholds.get(config_key, {}).get("dedupe_ttl_sec", 900))
        identity = event.symbol or event.sector or event.dedupe_key
        key = redis_keys.alert_dedupe(event.event_type, event.scope, identity)
        is_new = await client.set(key, "1", ex=ttl, nx=True)
        if is_new:
            deduped.append(event)
    return deduped


async def _load_liquidation_windows(markets: list[dict[str, Any]]) -> dict[str, LiquidationWindow]:
    client = get_redis_client()
    try:
        pairs = await asyncio.gather(
            *(
                get_liquidation_window(
                    client,
                    exchange=market["exchange"],
                    market_type=market["market_type"],
                    symbol=market["symbol"],
                )
                for market in markets
            ),
            return_exceptions=True,
        )
    except Exception:
        return {}
    finally:
        await client.aclose()

    windows: dict[str, LiquidationWindow] = {}
    for market, window in zip(markets, pairs):
        if isinstance(window, Exception):
            continue
        windows[market["symbol"]] = window
    return windows


async def run_binance_snapshot(
    *,
    universe_override: dict[str, Any] | None = None,
    persist_db: bool = True,
    write_redis: bool = True,
    create_tables: bool = True,
    read_flow_redis: bool = True,
) -> SnapshotResult:
    universe = universe_override or load_universe()
    thresholds = load_thresholds()
    markets = enabled_binance_markets(universe)
    preview_concurrency = 4 if len(markets) > 150 else 6
    snapshots, errors = await _fetch_snapshots(markets, concurrency=preview_concurrency if not persist_db else 4)
    liquidation_windows = await _load_liquidation_windows(markets) if read_flow_redis else {}

    base_metrics_by_symbol = {
        snapshot.symbol: calculate_market_metrics(snapshot.metric_input)
        for snapshot in snapshots
    }
    sector_counts = _configured_sector_counts(universe, markets)
    grouped_base = _metrics_by_sector(universe, markets, base_metrics_by_symbol)
    base_sector_metrics = {
        sector: calculate_sector_metrics(
            sector=sector,
            ts=datetime.now(timezone.utc),
            members=members,
            configured_member_count=sector_counts.get(sector, len(members)),
        )
        for sector, members in grouped_base.items()
    }

    final_metrics_by_symbol: dict[str, MarketMetrics] = {}
    primary_sector_by_symbol = _primary_sector_by_symbol(markets)
    for snapshot in snapshots:
        sector = primary_sector_by_symbol.get(snapshot.symbol)
        sector_return_1h = base_sector_metrics.get(sector).return_1h if sector in base_sector_metrics else None
        liquidation_window = liquidation_windows.get(snapshot.symbol, LiquidationWindow())

        metric_input = replace(
            snapshot.metric_input,
            sector_return_1h=sector_return_1h,
            liquidations_15m_usd=liquidation_window.liquidations_15m_usd,
            long_liquidations_15m_usd=liquidation_window.long_liquidations_15m_usd,
            short_liquidations_15m_usd=liquidation_window.short_liquidations_15m_usd,
        )
        final_metrics_by_symbol[snapshot.symbol] = calculate_market_metrics(metric_input)

    grouped_final = _metrics_by_sector(universe, markets, final_metrics_by_symbol)
    sector_metrics = [
        calculate_sector_metrics(
            sector=sector,
            ts=datetime.now(timezone.utc),
            members=members,
            configured_member_count=sector_counts.get(sector, len(members)),
        )
        for sector, members in grouped_final.items()
    ]

    market_metrics = sorted(final_metrics_by_symbol.values(), key=lambda item: item.symbol)
    market_events = [
        event
        for metric in market_metrics
        for event in detect_market_anomalies(metric, thresholds)
    ]
    sector_events = detect_sector_anomalies(sector_metrics, thresholds)
    events = market_events + sector_events

    if write_redis:
        client = get_redis_client()
        try:
            events = await _dedupe_events(client, events, thresholds)
            await replace_latest_market_metrics(client, market_metrics)
            await replace_latest_sector_metrics(client, sector_metrics)
            await save_events(client, events)
        finally:
            await client.aclose()

    if persist_db:
        if create_tables:
            await create_schema()

        async with AsyncSessionLocal() as session:
            await seed_universe(session, universe)
            market_lookup = await load_market_lookup(session)
            sector_lookup = await load_sector_lookup(session)
            await upsert_candles(
                session,
                [candle for snapshot in snapshots for candle in snapshot.candles],
                market_lookup,
            )
            await insert_market_metrics(session, market_metrics, market_lookup)
            await insert_sector_metrics(session, sector_metrics, sector_lookup)
            await insert_anomaly_events(session, events, market_lookup, sector_lookup)
            await session.commit()

    return SnapshotResult(
        ts=datetime.now(timezone.utc),
        market_metrics=market_metrics,
        sector_metrics=sector_metrics,
        events=events,
        errors=errors,
    )
