import json
from datetime import datetime, timedelta, timezone

import pytest

from app.agent.context import SnapshotNotFoundError, load_risk_context
from app.agent.models import RiskBriefRequest
from app.agent.service import OpenAIRiskAgent, build_risk_brief
from app.core.config import Settings


def _write_snapshot(path, *, age_minutes: int = 5) -> datetime:
    snapshot_ts = datetime.now(timezone.utc) - timedelta(minutes=age_minutes)
    payload = {
        "ts": snapshot_ts.isoformat(),
        "source": "test",
        "universe": {
            "markets": [
                {
                    "exchange": "binance",
                    "market_type": "futures",
                    "symbol": "SOLUSDT",
                    "asset": "SOL",
                    "sector": "Layer1",
                    "enabled": True,
                }
            ],
            "sectors": {"Layer1": ["SOL"]},
        },
        "market_metrics": [
            {
                "exchange": "binance",
                "market_type": "futures",
                "symbol": "SOLUSDT",
                "ts": snapshot_ts.isoformat(),
                "return_1h": 2.4,
                "return_24h": 8.2,
                "quote_volume_24h": 800_000_000,
                "volume_spike_ratio_5m": 1.8,
                "oi_usd": 900_000_000,
                "oi_change_15m": 2.1,
                "oi_to_market_cap_pct": 1.2,
                "cvd_15m": 4_000_000,
                "liq_pct_15m": 1.5,
                "base_days": 8,
                "base_breakout_pct": 0.7,
                "order_book_imbalance_pct": 12.0,
                "data_quality": "active",
            }
        ],
        "sector_metrics": [
            {
                "sector": "Layer1",
                "ts": snapshot_ts.isoformat(),
                "return_1h": 0.8,
                "oi_change_15m": 0.4,
                "active_member_ratio": 1.0,
            }
        ],
        "events": [
            {
                "event_type": "VOLUME_SPIKE",
                "symbol": "SOLUSDT",
                "message": "SOLUSDT volume expanded above its rolling median.",
            }
        ],
    }
    path.write_text(json.dumps(payload), encoding="utf-8")
    return snapshot_ts


def test_context_resolves_asset_and_retrieves_grounding(tmp_path):
    cache_path = tmp_path / "snapshot.json"
    _write_snapshot(cache_path)

    context = load_risk_context(cache_path, "SOL", "intrawick")

    assert context.symbol == "SOLUSDT"
    assert context.sector == "Layer1"
    assert context.policy_rules
    assert "quality:freshness" in {item.id for item in context.evidence}
    assert "event:1" in {item.id for item in context.evidence}


def test_context_rejects_symbol_outside_snapshot(tmp_path):
    cache_path = tmp_path / "snapshot.json"
    _write_snapshot(cache_path)

    with pytest.raises(SnapshotNotFoundError):
        load_risk_context(cache_path, "BTC", "intrawick")


def test_agent_tool_cannot_escape_approved_symbol(tmp_path):
    cache_path = tmp_path / "snapshot.json"
    _write_snapshot(cache_path)
    context = load_risk_context(cache_path, "SOL", "intrawick")

    with pytest.raises(ValueError, match="exceeded"):
        OpenAIRiskAgent._dispatch_tool(
            "get_market_snapshot",
            {"symbol": "BTCUSDT", "horizon": "intrawick"},
            context,
        )


@pytest.mark.asyncio
async def test_unconfigured_agent_returns_audited_deterministic_fallback(tmp_path):
    cache_path = tmp_path / "snapshot.json"
    _write_snapshot(cache_path)
    settings = Settings(
        config_dir=tmp_path,
        risk_agent_enabled=True,
        openai_api_key=None,
        risk_agent_max_snapshot_age_minutes=30,
    )

    result = await build_risk_brief(
        RiskBriefRequest(symbol="SOL", horizon="intrawick"),
        settings,
        cache_path,
    )

    assert result.symbol == "SOLUSDT"
    assert result.trace.provider == "deterministic"
    assert result.trace.status == "fallback"
    assert [tool.name for tool in result.trace.tool_calls] == [
        "get_market_snapshot",
        "retrieve_risk_playbook",
    ]
    assert result.requires_human_review is True
    assert result.execution_allowed is False
    assert set(result.evidence_ids) <= {item.id for item in result.evidence}


@pytest.mark.asyncio
async def test_stale_snapshot_forces_needs_context(tmp_path):
    cache_path = tmp_path / "snapshot.json"
    _write_snapshot(cache_path, age_minutes=180)
    settings = Settings(
        config_dir=tmp_path,
        risk_agent_enabled=True,
        openai_api_key=None,
        risk_agent_max_snapshot_age_minutes=30,
    )

    result = await build_risk_brief(
        RiskBriefRequest(symbol="SOLUSDT", horizon="intrawick"),
        settings,
        cache_path,
    )

    assert result.stance == "needs_context"
    assert result.regime == "needs_context"
    assert result.risk_level == "unknown"
    assert result.confidence <= 0.1
