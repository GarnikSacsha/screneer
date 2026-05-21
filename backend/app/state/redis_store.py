from __future__ import annotations

import json
from dataclasses import asdict
from datetime import datetime
from typing import Any
from uuid import UUID

import redis.asyncio as redis

from app.core.config import get_settings
from app.domain.entities import AnomalyEvent, MarketMetrics, SectorMetrics
from app.state import redis_keys


MARKET_METRICS_INDEX = "latest:metrics:index"
SECTOR_METRICS_INDEX = "latest:sector:index"
RECENT_EVENTS_KEY = "events:recent"


def get_redis_client() -> redis.Redis:
    return redis.from_url(
        get_settings().redis_url,
        decode_responses=True,
        socket_connect_timeout=0.35,
        socket_timeout=0.75,
    )


def _json_default(value: Any) -> str:
    if isinstance(value, datetime):
        return value.isoformat()
    if isinstance(value, UUID):
        return str(value)
    raise TypeError(f"Cannot JSON encode {type(value)!r}")


def _dump(value: Any) -> str:
    return json.dumps(asdict(value), default=_json_default, ensure_ascii=False)


def _parse_datetime(value: str) -> datetime:
    return datetime.fromisoformat(value.replace("Z", "+00:00"))


def _market_metrics_from_payload(payload: dict[str, Any]) -> MarketMetrics:
    return MarketMetrics(
        exchange=payload["exchange"],
        market_type=payload["market_type"],
        symbol=payload["symbol"],
        ts=_parse_datetime(payload["ts"]),
        price=payload.get("price"),
        return_5m=payload.get("return_5m"),
        return_15m=payload.get("return_15m"),
        return_1h=payload.get("return_1h"),
        return_24h=payload.get("return_24h"),
        volume_spike_ratio_5m=payload.get("volume_spike_ratio_5m"),
        volume_spike_ratio_15m=payload.get("volume_spike_ratio_15m"),
        quote_volume_5m=payload.get("quote_volume_5m"),
        quote_volume_24h=payload.get("quote_volume_24h"),
        consolidation_range_1h_pct=payload.get("consolidation_range_1h_pct"),
        consolidation_breakout_pct=payload.get("consolidation_breakout_pct"),
        consolidation_breakout_level=payload.get("consolidation_breakout_level"),
        oi_usd=payload.get("oi_usd"),
        oi_to_market_cap_pct=payload.get("oi_to_market_cap_pct"),
        oi_change_15m=payload.get("oi_change_15m"),
        base_days=payload.get("base_days"),
        base_high=payload.get("base_high"),
        base_low=payload.get("base_low"),
        base_range_pct=payload.get("base_range_pct"),
        base_distance_to_high_pct=payload.get("base_distance_to_high_pct"),
        base_breakout_pct=payload.get("base_breakout_pct"),
        base_volume_dry_up_ratio=payload.get("base_volume_dry_up_ratio"),
        base_prebreak_volume_ratio=payload.get("base_prebreak_volume_ratio"),
        daily_fvg_side=payload.get("daily_fvg_side"),
        daily_fvg_low=payload.get("daily_fvg_low"),
        daily_fvg_high=payload.get("daily_fvg_high"),
        daily_fvg_age_days=payload.get("daily_fvg_age_days"),
        daily_fvg_distance_pct=payload.get("daily_fvg_distance_pct"),
        daily_fvg_test=payload.get("daily_fvg_test"),
        funding_rate=payload.get("funding_rate"),
        cvd_15m=payload.get("cvd_15m"),
        order_book_bid_wall_usd=payload.get("order_book_bid_wall_usd"),
        order_book_ask_wall_usd=payload.get("order_book_ask_wall_usd"),
        order_book_imbalance_pct=payload.get("order_book_imbalance_pct"),
        order_book_wall_side=payload.get("order_book_wall_side"),
        order_book_wall_distance_pct=payload.get("order_book_wall_distance_pct"),
        ema_4h_50=payload.get("ema_4h_50"),
        ema_4h_100=payload.get("ema_4h_100"),
        ema_1d_50=payload.get("ema_1d_50"),
        ema_1d_100=payload.get("ema_1d_100"),
        liquidations_15m_usd=payload.get("liquidations_15m_usd"),
        long_liquidations_15m_usd=payload.get("long_liquidations_15m_usd"),
        short_liquidations_15m_usd=payload.get("short_liquidations_15m_usd"),
        liq_pct_15m=payload.get("liq_pct_15m"),
        relative_strength_1h=payload.get("relative_strength_1h"),
        data_quality=payload.get("data_quality", "active"),
    )


def _sector_metrics_from_payload(payload: dict[str, Any]) -> SectorMetrics:
    return SectorMetrics(
        sector=payload["sector"],
        ts=_parse_datetime(payload["ts"]),
        return_5m=payload.get("return_5m"),
        return_1h=payload.get("return_1h"),
        return_24h=payload.get("return_24h"),
        volume_spike_ratio_5m=payload.get("volume_spike_ratio_5m"),
        quote_volume_5m=payload.get("quote_volume_5m"),
        quote_volume_24h=payload.get("quote_volume_24h"),
        oi_usd=payload.get("oi_usd"),
        oi_change_15m=payload.get("oi_change_15m"),
        cvd_15m=payload.get("cvd_15m"),
        liquidations_15m_usd=payload.get("liquidations_15m_usd"),
        long_liquidations_15m_usd=payload.get("long_liquidations_15m_usd"),
        short_liquidations_15m_usd=payload.get("short_liquidations_15m_usd"),
        liq_pct_15m=payload.get("liq_pct_15m"),
        active_member_ratio=payload.get("active_member_ratio", 0.0),
        data_quality=payload.get("data_quality", "active"),
    )


def _event_from_payload(payload: dict[str, Any]) -> AnomalyEvent:
    return AnomalyEvent(
        id=UUID(payload["id"]),
        event_type=payload["event_type"],
        scope=payload["scope"],
        exchange=payload.get("exchange"),
        market_type=payload.get("market_type"),
        symbol=payload.get("symbol"),
        sector=payload.get("sector"),
        ts=_parse_datetime(payload["ts"]),
        score=payload["score"],
        severity=payload["severity"],
        dedupe_key=payload["dedupe_key"],
        formula_inputs=payload.get("formula_inputs", {}),
        message=payload["message"],
    )


async def save_market_metrics(client: redis.Redis, metrics: list[MarketMetrics]) -> None:
    if not metrics:
        return

    pipeline = client.pipeline()
    for item in metrics:
        key = redis_keys.latest_metrics(item.exchange, item.market_type, item.symbol)
        pipeline.set(key, _dump(item))
        pipeline.sadd(MARKET_METRICS_INDEX, key)
    await pipeline.execute()


async def replace_latest_market_metrics(client: redis.Redis, metrics: list[MarketMetrics]) -> None:
    old_keys = await client.smembers(MARKET_METRICS_INDEX)
    pipeline = client.pipeline()
    if old_keys:
        pipeline.delete(*old_keys)
    pipeline.delete(MARKET_METRICS_INDEX)
    await pipeline.execute()
    await save_market_metrics(client, metrics)


async def save_sector_metrics(client: redis.Redis, metrics: list[SectorMetrics]) -> None:
    if not metrics:
        return

    pipeline = client.pipeline()
    for item in metrics:
        key = redis_keys.latest_sector(item.sector)
        pipeline.set(key, _dump(item))
        pipeline.sadd(SECTOR_METRICS_INDEX, key)
    await pipeline.execute()


async def replace_latest_sector_metrics(client: redis.Redis, metrics: list[SectorMetrics]) -> None:
    old_keys = await client.smembers(SECTOR_METRICS_INDEX)
    pipeline = client.pipeline()
    if old_keys:
        pipeline.delete(*old_keys)
    pipeline.delete(SECTOR_METRICS_INDEX)
    await pipeline.execute()
    await save_sector_metrics(client, metrics)


async def save_events(client: redis.Redis, events: list[AnomalyEvent], limit: int = 200) -> None:
    if not events:
        return

    pipeline = client.pipeline()
    for event in events:
        pipeline.lpush(RECENT_EVENTS_KEY, _dump(event))
    pipeline.ltrim(RECENT_EVENTS_KEY, 0, limit - 1)
    await pipeline.execute()


async def get_latest_market_metrics(client: redis.Redis) -> list[MarketMetrics]:
    keys = sorted(await client.smembers(MARKET_METRICS_INDEX))
    if not keys:
        return []

    values = await client.mget(keys)
    items = [_market_metrics_from_payload(json.loads(value)) for value in values if value]
    return sorted(items, key=lambda item: item.symbol)


async def get_latest_sector_metrics(client: redis.Redis) -> list[SectorMetrics]:
    keys = sorted(await client.smembers(SECTOR_METRICS_INDEX))
    if not keys:
        return []

    values = await client.mget(keys)
    items = [_sector_metrics_from_payload(json.loads(value)) for value in values if value]
    return sorted(items, key=lambda item: item.sector)


async def get_recent_events(client: redis.Redis, limit: int = 50) -> list[AnomalyEvent]:
    values = await client.lrange(RECENT_EVENTS_KEY, 0, limit - 1)
    return [_event_from_payload(json.loads(value)) for value in values]
