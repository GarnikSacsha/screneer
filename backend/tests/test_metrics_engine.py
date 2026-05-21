from datetime import datetime, timezone

from app.metrics.engine import MarketMetricInput, calculate_market_metrics, pct_change, volume_spike_ratio


def test_pct_change():
    assert round(pct_change(110, 100) or 0, 6) == 10
    assert round(pct_change(90, 100) or 0, 6) == -10
    assert pct_change(100, 0) is None


def test_volume_spike_ratio_uses_median():
    ratio = volume_spike_ratio(200, [90, 100, 110, 1000])
    assert round(ratio, 2) == 1.9


def test_calculate_market_metrics():
    metrics = calculate_market_metrics(
        MarketMetricInput(
            exchange="binance",
            market_type="futures",
            symbol="SOLUSDT",
            ts=datetime.now(timezone.utc),
            close_now=110,
            close_5m_ago=100,
            close_15m_ago=100,
            close_1h_ago=100,
            close_24h_ago=100,
            quote_volume_5m=200,
            quote_volume_5m_history=[90, 100, 110],
            oi_usd_now=103,
            oi_usd_15m_ago=100,
            liquidations_15m_usd=10,
            sector_return_1h=5,
        )
    )

    assert round(metrics.return_5m or 0, 2) == 10
    assert round(metrics.oi_change_15m or 0, 2) == 3
    assert round(metrics.liq_pct_15m or 0, 2) == 5
    assert round(metrics.relative_strength_1h or 0, 2) == 5
