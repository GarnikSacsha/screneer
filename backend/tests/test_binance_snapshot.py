from app.ingestion.binance_snapshot import _daily_fvg_metrics_from_klines


def _kline(high: float, low: float) -> list[float]:
    return [0, 0, high, low, 0, 0, 0, 0]


def test_daily_fvg_metrics_detects_open_bullish_gap_test() -> None:
    klines = [
        _kline(10, 8),
        _kline(12, 9),
        _kline(15, 13),
        _kline(16, 14),
        _kline(15, 12.5),
        _kline(15, 14),
    ]

    result = _daily_fvg_metrics_from_klines(klines, latest_price=12.8)

    assert result["daily_fvg_side"] == "bullish"
    assert result["daily_fvg_low"] == 10
    assert result["daily_fvg_high"] == 13
    assert result["daily_fvg_test"] is True


def test_daily_fvg_metrics_ignores_fully_filled_gap() -> None:
    klines = [
        _kline(10, 8),
        _kline(12, 9),
        _kline(15, 13),
        _kline(14, 9.5),
        _kline(15, 14),
    ]

    result = _daily_fvg_metrics_from_klines(klines, latest_price=14)

    assert result["daily_fvg_side"] is None
