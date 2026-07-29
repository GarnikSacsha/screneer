from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, Literal
from uuid import UUID, uuid4

MarketStatus = Literal["active", "degraded", "stale", "disabled"]
EventSeverity = Literal["info", "medium", "high", "critical"]
EventScope = Literal["market", "sector"]


@dataclass(frozen=True)
class Candle:
    exchange: str
    market_type: str
    symbol: str
    timeframe: str
    open_time: datetime
    close_time: datetime
    open: float
    high: float
    low: float
    close: float
    base_volume: float
    quote_volume: float
    trade_count: int | None = None
    taker_buy_base_volume: float | None = None
    taker_buy_quote_volume: float | None = None
    is_closed: bool = True
    source_event_time: datetime | None = None


@dataclass(frozen=True)
class MarketMetrics:
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
    funding_rate: float | None = None
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
    relative_strength_1h: float | None = None
    data_quality: MarketStatus = "active"


@dataclass(frozen=True)
class SectorMetrics:
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
    active_member_ratio: float = 0.0
    data_quality: MarketStatus = "active"


@dataclass(frozen=True)
class AnomalyEvent:
    event_type: str
    scope: EventScope
    ts: datetime
    score: float
    severity: EventSeverity
    dedupe_key: str
    formula_inputs: dict[str, Any]
    message: str
    id: UUID = field(default_factory=uuid4)
    exchange: str | None = None
    market_type: str | None = None
    symbol: str | None = None
    sector: str | None = None
