from datetime import datetime
from typing import Any
from uuid import UUID

from pydantic import BaseModel


class HealthResponse(BaseModel):
    status: str
    app: str
    env: str


class MarketMetricsResponse(BaseModel):
    exchange: str
    market_type: str
    symbol: str
    ts: datetime
    price: float | None = None
    return_5m: float | None = None
    return_15m: float | None = None
    return_1h: float | None = None
    return_24h: float | None = None
    volume_spike_ratio_5m: float | None = None
    volume_spike_ratio_15m: float | None = None
    quote_volume_5m: float | None = None
    quote_volume_24h: float | None = None
    consolidation_range_1h_pct: float | None = None
    consolidation_breakout_pct: float | None = None
    consolidation_breakout_level: float | None = None
    oi_usd: float | None = None
    oi_to_market_cap_pct: float | None = None
    oi_change_15m: float | None = None
    base_days: int | None = None
    base_high: float | None = None
    base_low: float | None = None
    base_range_pct: float | None = None
    base_distance_to_high_pct: float | None = None
    base_breakout_pct: float | None = None
    base_volume_dry_up_ratio: float | None = None
    base_prebreak_volume_ratio: float | None = None
    daily_fvg_side: str | None = None
    daily_fvg_low: float | None = None
    daily_fvg_high: float | None = None
    daily_fvg_age_days: int | None = None
    daily_fvg_distance_pct: float | None = None
    daily_fvg_test: bool | None = None
    cvd_15m: float | None = None
    order_book_bid_wall_usd: float | None = None
    order_book_ask_wall_usd: float | None = None
    order_book_imbalance_pct: float | None = None
    order_book_wall_side: str | None = None
    order_book_wall_distance_pct: float | None = None
    ema_4h_50: float | None = None
    ema_4h_100: float | None = None
    ema_1d_50: float | None = None
    ema_1d_100: float | None = None
    liquidations_15m_usd: float | None = None
    long_liquidations_15m_usd: float | None = None
    short_liquidations_15m_usd: float | None = None
    liq_pct_15m: float | None = None
    data_quality: str


class SectorMetricsResponse(BaseModel):
    sector: str
    ts: datetime
    return_5m: float | None = None
    return_1h: float | None = None
    return_24h: float | None = None
    volume_spike_ratio_5m: float | None = None
    quote_volume_5m: float | None = None
    quote_volume_24h: float | None = None
    oi_usd: float | None = None
    oi_change_15m: float | None = None
    cvd_15m: float | None = None
    liquidations_15m_usd: float | None = None
    long_liquidations_15m_usd: float | None = None
    short_liquidations_15m_usd: float | None = None
    liq_pct_15m: float | None = None
    active_member_ratio: float
    data_quality: str


class AnomalyEventResponse(BaseModel):
    id: UUID
    event_type: str
    scope: str
    ts: datetime
    score: float
    severity: str
    dedupe_key: str
    formula_inputs: dict[str, Any]
    message: str
    exchange: str | None = None
    market_type: str | None = None
    symbol: str | None = None
    sector: str | None = None


class SnapshotRunResponse(BaseModel):
    ts: datetime
    markets: int
    sectors: int
    events: int
    errors: dict[str, str]


class SnapshotPreviewResponse(BaseModel):
    ts: datetime
    universe: dict[str, Any] | None = None
    market_metrics: list[MarketMetricsResponse]
    sector_metrics: list[SectorMetricsResponse]
    events: list[AnomalyEventResponse]
    errors: dict[str, str]
