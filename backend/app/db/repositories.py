from __future__ import annotations

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models import (
    AnomalyEventModel,
    CandleModel,
    Exchange,
    Market,
    MarketMetricSnapshot,
    Sector,
    SectorMetricSnapshot,
)
from app.domain.entities import AnomalyEvent, Candle, MarketMetrics, SectorMetrics

MarketKey = tuple[str, str, str]


async def load_market_lookup(session: AsyncSession) -> dict[MarketKey, int]:
    result = await session.execute(
        select(Exchange.code, Market.market_type, Market.symbol, Market.id).join(
            Exchange,
            Exchange.id == Market.exchange_id,
        )
    )
    return {(exchange, market_type, symbol): market_id for exchange, market_type, symbol, market_id in result.all()}


async def load_sector_lookup(session: AsyncSession) -> dict[str, int]:
    result = await session.execute(select(Sector.code, Sector.id))
    return {code: sector_id for code, sector_id in result.all()}


async def upsert_candles(session: AsyncSession, candles: list[Candle], market_lookup: dict[MarketKey, int]) -> None:
    for candle in candles:
        market_id = market_lookup.get((candle.exchange, candle.market_type, candle.symbol))
        if market_id is None:
            continue

        result = await session.execute(
            select(CandleModel).where(
                CandleModel.market_id == market_id,
                CandleModel.timeframe == candle.timeframe,
                CandleModel.open_time == candle.open_time,
            )
        )
        model = result.scalar_one_or_none()
        if model is None:
            session.add(
                CandleModel(
                    market_id=market_id,
                    timeframe=candle.timeframe,
                    open_time=candle.open_time,
                    close_time=candle.close_time,
                    open=candle.open,
                    high=candle.high,
                    low=candle.low,
                    close=candle.close,
                    base_volume=candle.base_volume,
                    quote_volume=candle.quote_volume,
                    trade_count=candle.trade_count,
                    taker_buy_base_volume=candle.taker_buy_base_volume,
                    taker_buy_quote_volume=candle.taker_buy_quote_volume,
                    source_event_time=candle.source_event_time,
                )
            )
        else:
            model.close_time = candle.close_time
            model.open = candle.open
            model.high = candle.high
            model.low = candle.low
            model.close = candle.close
            model.base_volume = candle.base_volume
            model.quote_volume = candle.quote_volume
            model.trade_count = candle.trade_count
            model.taker_buy_base_volume = candle.taker_buy_base_volume
            model.taker_buy_quote_volume = candle.taker_buy_quote_volume
            model.source_event_time = candle.source_event_time


async def insert_market_metrics(
    session: AsyncSession,
    metrics: list[MarketMetrics],
    market_lookup: dict[MarketKey, int],
) -> None:
    for item in metrics:
        market_id = market_lookup.get((item.exchange, item.market_type, item.symbol))
        if market_id is None:
            continue

        session.add(
            MarketMetricSnapshot(
                market_id=market_id,
                ts=item.ts,
                price=item.price,
                return_5m=item.return_5m,
                return_15m=item.return_15m,
                return_1h=item.return_1h,
                return_24h=item.return_24h,
                volume_spike_ratio_5m=item.volume_spike_ratio_5m,
                quote_volume_5m=item.quote_volume_5m,
                quote_volume_24h=item.quote_volume_24h,
                oi_usd=item.oi_usd,
                oi_change_15m=item.oi_change_15m,
                funding_rate=item.funding_rate,
                cvd_15m=item.cvd_15m,
                liquidations_15m_usd=item.liquidations_15m_usd,
                long_liquidations_15m_usd=item.long_liquidations_15m_usd,
                short_liquidations_15m_usd=item.short_liquidations_15m_usd,
                liq_pct_15m=item.liq_pct_15m,
                relative_strength_1h=item.relative_strength_1h,
                data_quality=item.data_quality,
            )
        )


async def insert_sector_metrics(
    session: AsyncSession,
    metrics: list[SectorMetrics],
    sector_lookup: dict[str, int],
) -> None:
    for item in metrics:
        sector_id = sector_lookup.get(item.sector)
        if sector_id is None:
            continue

        session.add(
            SectorMetricSnapshot(
                sector_id=sector_id,
                ts=item.ts,
                return_5m=item.return_5m,
                return_1h=item.return_1h,
                return_24h=item.return_24h,
                volume_spike_ratio_5m=item.volume_spike_ratio_5m,
                quote_volume_5m=item.quote_volume_5m,
                quote_volume_24h=item.quote_volume_24h,
                oi_usd=item.oi_usd,
                oi_change_15m=item.oi_change_15m,
                cvd_15m=item.cvd_15m,
                liquidations_15m_usd=item.liquidations_15m_usd,
                long_liquidations_15m_usd=item.long_liquidations_15m_usd,
                short_liquidations_15m_usd=item.short_liquidations_15m_usd,
                liq_pct_15m=item.liq_pct_15m,
                active_member_ratio=item.active_member_ratio,
                data_quality=item.data_quality,
            )
        )


async def insert_anomaly_events(
    session: AsyncSession,
    events: list[AnomalyEvent],
    market_lookup: dict[MarketKey, int],
    sector_lookup: dict[str, int],
) -> None:
    for event in events:
        result = await session.execute(select(AnomalyEventModel.id).where(AnomalyEventModel.id == event.id))
        if result.scalar_one_or_none() is not None:
            continue

        market_id = None
        if event.exchange and event.market_type and event.symbol:
            market_id = market_lookup.get((event.exchange, event.market_type, event.symbol))

        sector_id = sector_lookup.get(event.sector) if event.sector else None
        session.add(
            AnomalyEventModel(
                id=event.id,
                event_type=event.event_type,
                scope=event.scope,
                market_id=market_id,
                sector_id=sector_id,
                ts=event.ts,
                score=event.score,
                severity=event.severity,
                dedupe_key=event.dedupe_key,
                formula_inputs=event.formula_inputs,
                message=event.message,
            )
        )
