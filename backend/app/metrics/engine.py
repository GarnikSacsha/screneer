from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from statistics import median

from app.domain.entities import MarketMetrics, SectorMetrics


def pct_change(current: float | None, previous: float | None) -> float | None:
    if current is None or previous is None or previous == 0:
        return None
    return (current / previous - 1.0) * 100.0


def safe_ratio(numerator: float | None, denominator: float | None) -> float | None:
    if numerator is None or denominator is None or denominator == 0:
        return None
    return numerator / denominator


def rolling_median(values: list[float]) -> float | None:
    cleaned = [value for value in values if value is not None and value >= 0]
    if not cleaned:
        return None
    return float(median(cleaned))


def volume_spike_ratio(current_quote_volume: float | None, historical_quote_volumes: list[float]) -> float | None:
    baseline = rolling_median(historical_quote_volumes)
    return safe_ratio(current_quote_volume, baseline)


def liquidation_pct(liquidations_usd: float | None, quote_volume: float | None) -> float | None:
    ratio = safe_ratio(liquidations_usd, quote_volume)
    if ratio is None:
        return None
    return ratio * 100.0


def sum_optional(values: list[float | None]) -> float | None:
    cleaned = [value for value in values if value is not None]
    if not cleaned:
        return None
    return sum(cleaned)


def anomaly_score(
    *,
    volume_spike_ratio_5m: float | None,
    return_15m_pct: float | None,
    oi_change_15m_pct: float | None,
    liq_pct_15m: float | None,
    relative_strength_1h: float | None,
) -> float:
    volume_component = min((volume_spike_ratio_5m or 0.0) / 5.0, 1.0) * 25.0
    return_component = min(abs(return_15m_pct or 0.0) / 10.0, 1.0) * 20.0
    oi_component = min(abs(oi_change_15m_pct or 0.0) / 10.0, 1.0) * 20.0
    liq_component = min((liq_pct_15m or 0.0) / 5.0, 1.0) * 20.0
    rs_component = min(abs(relative_strength_1h or 0.0) / 5.0, 1.0) * 15.0
    return round(volume_component + return_component + oi_component + liq_component + rs_component, 2)


@dataclass(frozen=True)
class MarketMetricInput:
    exchange: str
    market_type: str
    symbol: str
    ts: datetime
    close_now: float | None
    close_5m_ago: float | None = None
    close_15m_ago: float | None = None
    close_1h_ago: float | None = None
    close_24h_ago: float | None = None
    quote_volume_5m: float | None = None
    quote_volume_5m_history: list[float] | None = None
    quote_volume_15m: float | None = None
    quote_volume_15m_history: list[float] | None = None
    quote_volume_24h: float | None = None
    consolidation_range_1h_pct: float | None = None
    consolidation_breakout_pct: float | None = None
    consolidation_breakout_level: float | None = None
    oi_usd_now: float | None = None
    circulating_market_cap: float | None = None
    oi_usd_15m_ago: float | None = None
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
    sector_return_1h: float | None = None
    data_quality: str = "active"


def calculate_market_metrics(input_data: MarketMetricInput) -> MarketMetrics:
    return_1h = pct_change(input_data.close_now, input_data.close_1h_ago)
    liquidations_15m_usd = input_data.liquidations_15m_usd
    if liquidations_15m_usd is None:
        liquidation_parts = [
            input_data.long_liquidations_15m_usd,
            input_data.short_liquidations_15m_usd,
        ]
        liquidations_15m_usd = sum_optional(liquidation_parts)

    return MarketMetrics(
        exchange=input_data.exchange,
        market_type=input_data.market_type,
        symbol=input_data.symbol,
        ts=input_data.ts,
        price=input_data.close_now,
        return_5m=pct_change(input_data.close_now, input_data.close_5m_ago),
        return_15m=pct_change(input_data.close_now, input_data.close_15m_ago),
        return_1h=return_1h,
        return_24h=pct_change(input_data.close_now, input_data.close_24h_ago),
        volume_spike_ratio_5m=volume_spike_ratio(
            input_data.quote_volume_5m,
            input_data.quote_volume_5m_history or [],
        ),
        volume_spike_ratio_15m=volume_spike_ratio(
            input_data.quote_volume_15m,
            input_data.quote_volume_15m_history or [],
        ),
        quote_volume_5m=input_data.quote_volume_5m,
        quote_volume_24h=input_data.quote_volume_24h,
        consolidation_range_1h_pct=input_data.consolidation_range_1h_pct,
        consolidation_breakout_pct=input_data.consolidation_breakout_pct,
        consolidation_breakout_level=input_data.consolidation_breakout_level,
        oi_usd=input_data.oi_usd_now,
        oi_to_market_cap_pct=(
            safe_ratio(input_data.oi_usd_now, input_data.circulating_market_cap) * 100.0
            if safe_ratio(input_data.oi_usd_now, input_data.circulating_market_cap) is not None
            else None
        ),
        oi_change_15m=pct_change(input_data.oi_usd_now, input_data.oi_usd_15m_ago),
        base_days=input_data.base_days,
        base_high=input_data.base_high,
        base_low=input_data.base_low,
        base_range_pct=input_data.base_range_pct,
        base_distance_to_high_pct=input_data.base_distance_to_high_pct,
        base_breakout_pct=input_data.base_breakout_pct,
        base_volume_dry_up_ratio=input_data.base_volume_dry_up_ratio,
        base_prebreak_volume_ratio=input_data.base_prebreak_volume_ratio,
        daily_fvg_side=input_data.daily_fvg_side,
        daily_fvg_low=input_data.daily_fvg_low,
        daily_fvg_high=input_data.daily_fvg_high,
        daily_fvg_age_days=input_data.daily_fvg_age_days,
        daily_fvg_distance_pct=input_data.daily_fvg_distance_pct,
        daily_fvg_test=input_data.daily_fvg_test,
        funding_rate=input_data.funding_rate,
        cvd_15m=input_data.cvd_15m,
        order_book_bid_wall_usd=input_data.order_book_bid_wall_usd,
        order_book_ask_wall_usd=input_data.order_book_ask_wall_usd,
        order_book_imbalance_pct=input_data.order_book_imbalance_pct,
        order_book_wall_side=input_data.order_book_wall_side,
        order_book_wall_distance_pct=input_data.order_book_wall_distance_pct,
        ema_4h_50=input_data.ema_4h_50,
        ema_4h_100=input_data.ema_4h_100,
        ema_1d_50=input_data.ema_1d_50,
        ema_1d_100=input_data.ema_1d_100,
        liquidations_15m_usd=liquidations_15m_usd,
        long_liquidations_15m_usd=input_data.long_liquidations_15m_usd,
        short_liquidations_15m_usd=input_data.short_liquidations_15m_usd,
        liq_pct_15m=liquidation_pct(liquidations_15m_usd, input_data.quote_volume_5m),
        relative_strength_1h=(
            return_1h - input_data.sector_return_1h
            if return_1h is not None and input_data.sector_return_1h is not None
            else None
        ),
        data_quality=input_data.data_quality,  # type: ignore[arg-type]
    )


def average(values: list[float | None]) -> float | None:
    cleaned = [value for value in values if value is not None]
    if not cleaned:
        return None
    return sum(cleaned) / len(cleaned)


def calculate_sector_metrics(sector: str, ts: datetime, members: list[MarketMetrics], configured_member_count: int) -> SectorMetrics:
    active_members = [member for member in members if member.data_quality == "active"]
    active_member_ratio = len(active_members) / configured_member_count if configured_member_count else 0.0
    quote_volume_5m = sum_optional([member.quote_volume_5m for member in active_members])
    liquidations_15m_usd = sum_optional([member.liquidations_15m_usd for member in active_members])

    return SectorMetrics(
        sector=sector,
        ts=ts,
        return_5m=average([member.return_5m for member in active_members]),
        return_1h=average([member.return_1h for member in active_members]),
        return_24h=average([member.return_24h for member in active_members]),
        volume_spike_ratio_5m=rolling_median(
            [member.volume_spike_ratio_5m for member in active_members if member.volume_spike_ratio_5m is not None]
        ),
        quote_volume_5m=quote_volume_5m,
        quote_volume_24h=sum(member.quote_volume_24h or 0.0 for member in active_members) if active_members else None,
        oi_usd=sum(member.oi_usd or 0.0 for member in active_members) if active_members else None,
        oi_change_15m=average([member.oi_change_15m for member in active_members]),
        cvd_15m=sum(member.cvd_15m or 0.0 for member in active_members) if active_members else None,
        liquidations_15m_usd=liquidations_15m_usd,
        long_liquidations_15m_usd=sum_optional([member.long_liquidations_15m_usd for member in active_members]),
        short_liquidations_15m_usd=sum_optional([member.short_liquidations_15m_usd for member in active_members]),
        liq_pct_15m=liquidation_pct(liquidations_15m_usd, quote_volume_5m),
        active_member_ratio=active_member_ratio,
        data_quality="active" if active_member_ratio >= 0.6 else "degraded",
    )
