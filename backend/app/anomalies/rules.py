from __future__ import annotations

from app.domain.entities import AnomalyEvent, MarketMetrics, SectorMetrics
from app.metrics.engine import anomaly_score


def severity_from_score(score: float) -> str:
    if score >= 85:
        return "critical"
    if score >= 70:
        return "high"
    if score >= 50:
        return "medium"
    return "info"


def _score(metrics: MarketMetrics) -> float:
    return anomaly_score(
        volume_spike_ratio_5m=metrics.volume_spike_ratio_5m,
        return_15m_pct=metrics.return_15m,
        oi_change_15m_pct=metrics.oi_change_15m,
        liq_pct_15m=metrics.liq_pct_15m,
        relative_strength_1h=metrics.relative_strength_1h,
    )


def detect_market_anomalies(metrics: MarketMetrics, thresholds: dict) -> list[AnomalyEvent]:
    if metrics.data_quality != "active":
        return []

    events: list[AnomalyEvent] = []
    event_thresholds = thresholds.get("events", {})

    volume_cfg = event_thresholds.get("volume_spike", {})
    if (
        metrics.volume_spike_ratio_5m is not None
        and metrics.quote_volume_5m is not None
        and metrics.volume_spike_ratio_5m >= float(volume_cfg.get("ratio_min", 2.0))
        and metrics.quote_volume_5m >= float(volume_cfg.get("min_quote_volume_5m", 1_000_000))
    ):
        score = _score(metrics)
        events.append(
            AnomalyEvent(
                event_type="VOLUME_SPIKE",
                scope="market",
                exchange=metrics.exchange,
                market_type=metrics.market_type,
                symbol=metrics.symbol,
                ts=metrics.ts,
                score=score,
                severity=severity_from_score(score),  # type: ignore[arg-type]
                dedupe_key=f"VOLUME_SPIKE:{metrics.exchange}:{metrics.symbol}",
                formula_inputs={
                    "volume_spike_ratio_5m": metrics.volume_spike_ratio_5m,
                    "quote_volume_5m": metrics.quote_volume_5m,
                },
                message=(
                    f"{metrics.symbol} volume spike: "
                    f"{metrics.volume_spike_ratio_5m:.2f}x vs rolling median."
                ),
            )
        )

    oi_cfg = event_thresholds.get("oi_expansion", {})
    if (
        metrics.oi_change_15m is not None
        and metrics.oi_usd is not None
        and metrics.oi_change_15m >= float(oi_cfg.get("change_15m_min_pct", 3.0))
        and metrics.oi_usd >= float(oi_cfg.get("min_oi_usd", 5_000_000))
    ):
        score = _score(metrics)
        events.append(
            AnomalyEvent(
                event_type="OI_EXPANSION",
                scope="market",
                exchange=metrics.exchange,
                market_type=metrics.market_type,
                symbol=metrics.symbol,
                ts=metrics.ts,
                score=score,
                severity=severity_from_score(score),  # type: ignore[arg-type]
                dedupe_key=f"OI_EXPANSION:{metrics.exchange}:{metrics.symbol}",
                formula_inputs={"oi_change_15m": metrics.oi_change_15m, "oi_usd": metrics.oi_usd},
                message=f"{metrics.symbol} OI expanded {metrics.oi_change_15m:.2f}% in 15m.",
            )
        )

    breakout_cfg = event_thresholds.get("price_breakout", {})
    if (
        metrics.return_15m is not None
        and metrics.volume_spike_ratio_5m is not None
        and metrics.return_15m >= float(breakout_cfg.get("return_15m_min_pct", 3.0))
        and metrics.volume_spike_ratio_5m >= float(breakout_cfg.get("volume_spike_ratio_min", 1.8))
    ):
        score = _score(metrics)
        events.append(
            AnomalyEvent(
                event_type="PRICE_BREAKOUT",
                scope="market",
                exchange=metrics.exchange,
                market_type=metrics.market_type,
                symbol=metrics.symbol,
                ts=metrics.ts,
                score=score,
                severity=severity_from_score(score),  # type: ignore[arg-type]
                dedupe_key=f"PRICE_BREAKOUT:{metrics.exchange}:{metrics.symbol}",
                formula_inputs={
                    "return_15m": metrics.return_15m,
                    "volume_spike_ratio_5m": metrics.volume_spike_ratio_5m,
                },
                message=f"{metrics.symbol} breakout: 15m return {metrics.return_15m:.2f}%.",
            )
        )

    squeeze_cfg = event_thresholds.get("squeeze_risk", {})
    long_liq = metrics.long_liquidations_15m_usd or 0.0
    short_liq = metrics.short_liquidations_15m_usd or 0.0
    total_liq = long_liq + short_liq
    max_side_share = max(long_liq, short_liq) / total_liq if total_liq > 0 else None
    if (
        metrics.liq_pct_15m is not None
        and max_side_share is not None
        and metrics.liq_pct_15m >= float(squeeze_cfg.get("liq_pct_15m_min", 2.0))
        and max_side_share >= float(squeeze_cfg.get("long_short_skew_min", 0.65))
    ):
        score = _score(metrics)
        crowded_side = "longs" if long_liq >= short_liq else "shorts"
        events.append(
            AnomalyEvent(
                event_type="SQUEEZE_RISK",
                scope="market",
                exchange=metrics.exchange,
                market_type=metrics.market_type,
                symbol=metrics.symbol,
                ts=metrics.ts,
                score=score,
                severity=severity_from_score(score),  # type: ignore[arg-type]
                dedupe_key=f"SQUEEZE_RISK:{metrics.exchange}:{metrics.symbol}",
                formula_inputs={
                    "liq_pct_15m": metrics.liq_pct_15m,
                    "long_liquidations_15m_usd": metrics.long_liquidations_15m_usd,
                    "short_liquidations_15m_usd": metrics.short_liquidations_15m_usd,
                    "max_side_share": max_side_share,
                },
                message=f"{metrics.symbol} liquidation pressure is skewed toward {crowded_side}.",
            )
        )

    absorption_cfg = event_thresholds.get("absorption_candidate", {})
    if (
        metrics.cvd_15m is not None
        and metrics.return_15m is not None
        and metrics.oi_change_15m is not None
        and metrics.cvd_15m < 0
        and abs(metrics.return_15m) <= float(absorption_cfg.get("max_abs_return_15m_pct", 0.5))
        and metrics.oi_change_15m > float(absorption_cfg.get("min_oi_change_15m_pct", 0.0))
    ):
        score = _score(metrics)
        events.append(
            AnomalyEvent(
                event_type="ABSORPTION_CANDIDATE",
                scope="market",
                exchange=metrics.exchange,
                market_type=metrics.market_type,
                symbol=metrics.symbol,
                ts=metrics.ts,
                score=score,
                severity=severity_from_score(score),  # type: ignore[arg-type]
                dedupe_key=f"ABSORPTION:{metrics.exchange}:{metrics.symbol}",
                formula_inputs={
                    "cvd_15m": metrics.cvd_15m,
                    "return_15m": metrics.return_15m,
                    "oi_change_15m": metrics.oi_change_15m,
                },
                message=f"{metrics.symbol} absorption candidate: negative CVD while price holds.",
            )
        )

    return events


def detect_sector_anomalies(sector_metrics: list[SectorMetrics], thresholds: dict) -> list[AnomalyEvent]:
    event_thresholds = thresholds.get("events", {})
    leader_cfg = event_thresholds.get("sector_leader", {})
    top_n = int(leader_cfg.get("top_n", 3))
    min_return = float(leader_cfg.get("return_1h_min_pct", 2.0))

    ranked = sorted(
        [item for item in sector_metrics if item.return_1h is not None and item.data_quality == "active"],
        key=lambda item: item.return_1h or 0.0,
        reverse=True,
    )

    events: list[AnomalyEvent] = []
    for rank, sector in enumerate(ranked[:top_n], start=1):
        if sector.return_1h is None or sector.return_1h < min_return:
            continue

        score = min(abs(sector.return_1h) / 10.0, 1.0) * 70.0 + min(sector.active_member_ratio, 1.0) * 30.0
        score = round(score, 2)
        events.append(
            AnomalyEvent(
                event_type="SECTOR_LEADER",
                scope="sector",
                sector=sector.sector,
                ts=sector.ts,
                score=score,
                severity=severity_from_score(score),  # type: ignore[arg-type]
                dedupe_key=f"SECTOR_LEADER:{sector.sector}",
                formula_inputs={
                    "sector_return_1h": sector.return_1h,
                    "rank": rank,
                    "active_member_ratio": sector.active_member_ratio,
                },
                message=f"{sector.sector} sector is #{rank} by 1h return: {sector.return_1h:.2f}%.",
            )
        )

    return events
