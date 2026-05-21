from datetime import datetime, timezone

from app.anomalies.rules import detect_market_anomalies
from app.domain.entities import MarketMetrics


def test_volume_spike_event_detected():
    thresholds = {
        "events": {
            "volume_spike": {
                "ratio_min": 2.0,
                "min_quote_volume_5m": 1_000_000,
            }
        }
    }
    metrics = MarketMetrics(
        exchange="binance",
        market_type="futures",
        symbol="SOLUSDT",
        ts=datetime.now(timezone.utc),
        volume_spike_ratio_5m=3.2,
        quote_volume_5m=2_000_000,
        data_quality="active",
    )

    events = detect_market_anomalies(metrics, thresholds)

    assert [event.event_type for event in events] == ["VOLUME_SPIKE"]


def test_stale_market_is_ignored():
    metrics = MarketMetrics(
        exchange="binance",
        market_type="futures",
        symbol="SOLUSDT",
        ts=datetime.now(timezone.utc),
        volume_spike_ratio_5m=10,
        quote_volume_5m=100_000_000,
        data_quality="stale",
    )

    assert detect_market_anomalies(metrics, {"events": {}}) == []
