from __future__ import annotations

import json
import re
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from app.agent.models import RiskEvidence, RiskHorizon
from app.core.config import load_risk_playbook, load_universe


class SnapshotNotFoundError(LookupError):
    """Raised when a requested symbol is not present in the latest snapshot."""


@dataclass(frozen=True)
class RiskContext:
    symbol: str
    horizon: RiskHorizon
    sector: str | None
    snapshot_ts: datetime
    snapshot_age_minutes: float
    data_quality: str
    source: str
    market: dict[str, Any]
    sector_metrics: dict[str, Any] | None
    events: list[dict[str, Any]]
    evidence: list[RiskEvidence]
    policy_rules: list[dict[str, Any]]

    def tool_payload(self) -> dict[str, Any]:
        return {
            "symbol": self.symbol,
            "horizon": self.horizon,
            "sector": self.sector,
            "snapshot_ts": self.snapshot_ts.isoformat(),
            "snapshot_age_minutes": round(self.snapshot_age_minutes, 2),
            "data_quality": self.data_quality,
            "source": self.source,
            "market": self.market,
            "sector_metrics": self.sector_metrics,
            "events": self.events,
            "evidence": [item.model_dump() for item in self.evidence if item.category != "policy"],
        }


def _parse_timestamp(value: str | datetime) -> datetime:
    if isinstance(value, datetime):
        parsed = value
    else:
        parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    return parsed if parsed.tzinfo else parsed.replace(tzinfo=timezone.utc)


def _format_number(value: Any, suffix: str = "", digits: int = 2) -> str:
    if not isinstance(value, (int, float)):
        return "unavailable"
    return f"{value:,.{digits}f}{suffix}"


def _asset_lookup(universe: dict[str, Any]) -> dict[str, str]:
    return {
        str(market.get("asset", "")).upper(): str(market.get("symbol", "")).upper()
        for market in universe.get("markets", [])
        if market.get("enabled", True) and market.get("symbol")
    }


def _resolve_symbol(requested: str, universe: dict[str, Any], metrics: list[dict[str, Any]]) -> str:
    requested = requested.upper()
    available = {str(metric.get("symbol", "")).upper() for metric in metrics}
    if requested in available:
        return requested

    asset_map = _asset_lookup(universe)
    if requested in asset_map and asset_map[requested] in available:
        return asset_map[requested]
    if not requested.endswith("USDT") and f"{requested}USDT" in available:
        return f"{requested}USDT"
    raise SnapshotNotFoundError(f"{requested} is not present in the latest materialized snapshot")


def _sector_for_symbol(symbol: str, universe: dict[str, Any]) -> str | None:
    for market in universe.get("markets", []):
        if str(market.get("symbol", "")).upper() == symbol:
            return market.get("sector")
    return None


def _risk_query(market: dict[str, Any], horizon: RiskHorizon) -> str:
    terms = [horizon, "data freshness", "human review", "leverage", "liquidity"]
    metric_terms = {
        "oi_change_15m": "open interest crowding",
        "oi_to_market_cap_pct": "open interest market cap reflexivity",
        "cvd_15m": "flow divergence cvd",
        "liq_pct_15m": "liquidation cascade",
        "volume_spike_ratio_5m": "volume expansion",
        "base_breakout_pct": "base breakout",
        "daily_fvg_side": "fair value gap",
        "order_book_imbalance_pct": "orderbook imbalance",
    }
    terms.extend(label for key, label in metric_terms.items() if market.get(key) is not None)
    return " ".join(terms)


def retrieve_playbook(query: str, limit: int = 5) -> list[dict[str, Any]]:
    playbook = load_risk_playbook()
    query_terms = set(re.findall(r"[a-z0-9_]+", query.lower()))
    scored: list[tuple[int, dict[str, Any]]] = []
    for rule in playbook.get("rules", []):
        haystack = " ".join(
            [
                str(rule.get("id", "")),
                str(rule.get("title", "")),
                str(rule.get("guidance", "")),
                " ".join(rule.get("keywords", [])),
            ]
        ).lower()
        score = sum(1 for term in query_terms if term in haystack)
        if rule.get("always"):
            score += 100
        scored.append((score, rule))
    scored.sort(key=lambda item: (-item[0], str(item[1].get("id", ""))))
    return [rule for score, rule in scored if score > 0][: max(1, min(limit, 8))]


def _build_evidence(
    market: dict[str, Any],
    sector: dict[str, Any] | None,
    events: list[dict[str, Any]],
    age_minutes: float,
    source: str,
    rules: list[dict[str, Any]],
) -> list[RiskEvidence]:
    evidence = [
        RiskEvidence(
            id="quality:freshness",
            category="quality",
            label="Snapshot freshness",
            value=f"{age_minutes:.1f} minutes old",
            source=source,
        ),
        RiskEvidence(
            id="snapshot:returns",
            category="snapshot",
            label="Price returns",
            value=(
                f"1H {_format_number(market.get('return_1h'), '%')}; "
                f"24H {_format_number(market.get('return_24h'), '%')}"
            ),
            source="Binance USD-M snapshot",
        ),
        RiskEvidence(
            id="snapshot:volume",
            category="snapshot",
            label="Liquidity and volume",
            value=(
                f"24H ${_format_number(market.get('quote_volume_24h'), digits=0)}; "
                f"5M spike {_format_number(market.get('volume_spike_ratio_5m'), 'x')}"
            ),
            source="Binance USD-M snapshot",
        ),
        RiskEvidence(
            id="snapshot:oi",
            category="snapshot",
            label="Open interest",
            value=(
                f"${_format_number(market.get('oi_usd'), digits=0)}; "
                f"15M {_format_number(market.get('oi_change_15m'), '%')}; "
                f"OI/MCAP {_format_number(market.get('oi_to_market_cap_pct'), '%')}"
            ),
            source="Binance USD-M snapshot",
        ),
        RiskEvidence(
            id="snapshot:flow",
            category="snapshot",
            label="Flow and liquidations",
            value=(
                f"CVD ${_format_number(market.get('cvd_15m'), digits=0)}; "
                f"LIQ {_format_number(market.get('liq_pct_15m'), '%')}"
            ),
            source="Quant Desk flow pipeline",
        ),
        RiskEvidence(
            id="snapshot:structure",
            category="snapshot",
            label="Market structure",
            value=(
                f"base {market.get('base_days') or 'n/a'}d; "
                f"breakout {_format_number(market.get('base_breakout_pct'), '%')}; "
                f"orderbook {_format_number(market.get('order_book_imbalance_pct'), '%')}"
            ),
            source="Quant Desk metric engine",
        ),
    ]
    if sector:
        evidence.append(
            RiskEvidence(
                id="sector:context",
                category="sector",
                label=f"{sector.get('sector', 'Sector')} context",
                value=(
                    f"1H {_format_number(sector.get('return_1h'), '%')}; "
                    f"OI 15M {_format_number(sector.get('oi_change_15m'), '%')}; "
                    f"active {_format_number((sector.get('active_member_ratio') or 0) * 100, '%')}"
                ),
                source="Quant Desk sector aggregation",
            )
        )
    for index, event in enumerate(events[:3], start=1):
        evidence.append(
            RiskEvidence(
                id=f"event:{index}",
                category="event",
                label=str(event.get("event_type", "Anomaly event")),
                value=str(event.get("message", "")),
                source="Quant Desk anomaly engine",
            )
        )
    evidence.extend(
        RiskEvidence(
            id=f"policy:{rule['id']}",
            category="policy",
            label=str(rule["title"]),
            value=str(rule["guidance"]),
            source="Risk playbook",
        )
        for rule in rules
    )
    return evidence


def load_risk_context(
    cache_path: Path,
    requested_symbol: str,
    horizon: RiskHorizon,
    *,
    now: datetime | None = None,
) -> RiskContext:
    if not cache_path.exists():
        raise SnapshotNotFoundError("No materialized snapshot is available")
    payload = json.loads(cache_path.read_text(encoding="utf-8-sig"))
    universe = payload.get("universe") or load_universe()
    metrics = payload.get("market_metrics", [])
    symbol = _resolve_symbol(requested_symbol, universe, metrics)
    market = next(item for item in metrics if str(item.get("symbol", "")).upper() == symbol)
    snapshot_ts = _parse_timestamp(market.get("ts") or payload["ts"])
    current = now or datetime.now(timezone.utc)
    age_minutes = max(0.0, (current - snapshot_ts).total_seconds() / 60)
    sector_name = _sector_for_symbol(symbol, universe)
    sector_metrics = next(
        (item for item in payload.get("sector_metrics", []) if item.get("sector") == sector_name),
        None,
    )
    events = [
        item
        for item in payload.get("events", [])
        if item.get("symbol") == symbol or (sector_name and item.get("sector") == sector_name)
    ]
    rules = retrieve_playbook(_risk_query(market, horizon))
    source = str(payload.get("source", "materialized_snapshot"))
    data_quality = str(market.get("data_quality", "unknown"))
    evidence = _build_evidence(market, sector_metrics, events, age_minutes, source, rules)
    return RiskContext(
        symbol=symbol,
        horizon=horizon,
        sector=sector_name,
        snapshot_ts=snapshot_ts,
        snapshot_age_minutes=age_minutes,
        data_quality=data_quality,
        source=source,
        market=market,
        sector_metrics=sector_metrics,
        events=events,
        evidence=evidence,
        policy_rules=rules,
    )
