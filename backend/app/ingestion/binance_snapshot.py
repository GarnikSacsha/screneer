from __future__ import annotations

import asyncio
from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Any

from app.domain.entities import Candle
from app.exchanges.binance import BinanceFuturesAdapter
from app.metrics.engine import MarketMetricInput


@dataclass(frozen=True)
class BinanceMarketSnapshot:
    symbol: str
    metric_input: MarketMetricInput
    candles: list[Candle]
    candles_count: int


def _float_or_none(value: Any) -> float | None:
    if value is None:
        return None
    try:
        return float(value)
    except (TypeError, ValueError):
        return None


def _open_interest_usd(open_interest_contracts: float | None, price: float | None) -> float | None:
    if open_interest_contracts is None or price is None:
        return None
    return open_interest_contracts * price


def _candle_cvd_quote(candle: Candle) -> float | None:
    if candle.taker_buy_quote_volume is None:
        return None
    taker_sell_quote = candle.quote_volume - candle.taker_buy_quote_volume
    return candle.taker_buy_quote_volume - taker_sell_quote


def _cvd_15m_from_candles(candles: list[Candle]) -> float | None:
    window = candles[-3:]
    values = [_candle_cvd_quote(candle) for candle in window]
    cleaned = [value for value in values if value is not None]
    if not cleaned:
        return None
    return sum(cleaned)


def _rolling_sum(values: list[float], window: int) -> list[float]:
    if len(values) < window:
        return []
    return [sum(values[index : index + window]) for index in range(0, len(values) - window + 1)]


def _consolidation_breakout_from_candles(candles: list[Candle]) -> tuple[float | None, float | None, float | None]:
    if len(candles) < 14:
        return None, None, None

    latest = candles[-1]
    box = candles[-13:-1]
    box_high = max(candle.high for candle in box)
    box_low = min(candle.low for candle in box)
    if latest.close <= 0 or box_high <= 0:
        return None, None, None

    range_pct = ((box_high / box_low) - 1) * 100 if box_low > 0 else None
    breakout_pct = ((latest.close / box_high) - 1) * 100
    return range_pct, breakout_pct, box_high


def _ema(values: list[float], period: int) -> float | None:
    if len(values) < period:
        return None

    seed = sum(values[:period]) / period
    multiplier = 2 / (period + 1)
    current = seed
    for value in values[period:]:
        current = (value - current) * multiplier + current
    return current


def _ema_from_raw_klines(raw_klines: list[dict[str, Any]] | list[list[Any]], period: int) -> float | None:
    closes = [_float_or_none(raw[4]) for raw in raw_klines]
    cleaned = [value for value in closes if value is not None]
    return _ema(cleaned, period)


def _median(values: list[float]) -> float | None:
    cleaned = sorted(value for value in values if value >= 0)
    if not cleaned:
        return None
    middle = len(cleaned) // 2
    if len(cleaned) % 2:
        return cleaned[middle]
    return (cleaned[middle - 1] + cleaned[middle]) / 2


def _base_metrics_from_daily_klines(
    raw_klines: list[dict[str, Any]] | list[list[Any]],
    latest_price: float | None,
    current_24h_quote_volume: float | None,
    base_days: int = 20,
) -> dict[str, float | int | None]:
    if latest_price is None or len(raw_klines) < 8:
        return {
            "base_days": None,
            "base_high": None,
            "base_low": None,
            "base_range_pct": None,
            "base_distance_to_high_pct": None,
            "base_breakout_pct": None,
            "base_volume_dry_up_ratio": None,
            "base_prebreak_volume_ratio": None,
        }

    closed_base = raw_klines[-(base_days + 1) : -1] if len(raw_klines) > base_days else raw_klines[:-1]
    if len(closed_base) < 5:
        closed_base = raw_klines[-min(len(raw_klines), base_days) :]

    highs = [_float_or_none(raw[2]) for raw in closed_base]
    lows = [_float_or_none(raw[3]) for raw in closed_base]
    volumes = [_float_or_none(raw[7]) for raw in closed_base]
    highs_clean = [value for value in highs if value is not None]
    lows_clean = [value for value in lows if value is not None]
    volumes_clean = [value for value in volumes if value is not None]
    if not highs_clean or not lows_clean:
        return {
            "base_days": len(closed_base),
            "base_high": None,
            "base_low": None,
            "base_range_pct": None,
            "base_distance_to_high_pct": None,
            "base_breakout_pct": None,
            "base_volume_dry_up_ratio": None,
            "base_prebreak_volume_ratio": None,
        }

    base_high = max(highs_clean)
    base_low = min(lows_clean)
    volume_median = _median(volumes_clean)
    latest_closed_volume = volumes_clean[-1] if volumes_clean else None

    return {
        "base_days": len(closed_base),
        "base_high": base_high,
        "base_low": base_low,
        "base_range_pct": ((base_high / base_low) - 1) * 100 if base_low > 0 else None,
        "base_distance_to_high_pct": ((latest_price / base_high) - 1) * 100 if base_high > 0 else None,
        "base_breakout_pct": ((latest_price / base_high) - 1) * 100 if base_high > 0 else None,
        "base_volume_dry_up_ratio": latest_closed_volume / volume_median if latest_closed_volume is not None and volume_median else None,
        "base_prebreak_volume_ratio": current_24h_quote_volume / volume_median if current_24h_quote_volume is not None and volume_median else None,
    }


def _daily_fvg_metrics_from_klines(
    raw_klines: list[dict[str, Any]] | list[list[Any]],
    latest_price: float | None,
    lookback: int = 60,
) -> dict[str, float | int | str | bool | None]:
    empty = {
        "daily_fvg_side": None,
        "daily_fvg_low": None,
        "daily_fvg_high": None,
        "daily_fvg_age_days": None,
        "daily_fvg_distance_pct": None,
        "daily_fvg_test": None,
    }
    if latest_price is None or latest_price <= 0 or len(raw_klines) < 4:
        return empty

    closed = raw_klines[:-1]
    if len(closed) < 3:
        return empty

    candidates: list[dict[str, float | int | str | bool]] = []
    start = max(0, len(closed) - lookback)
    for index in range(start, len(closed) - 2):
        first = closed[index]
        third = closed[index + 2]
        first_high = _float_or_none(first[2])
        first_low = _float_or_none(first[3])
        third_high = _float_or_none(third[2])
        third_low = _float_or_none(third[3])
        if None in (first_high, first_low, third_high, third_low):
            continue

        side: str | None = None
        low: float | None = None
        high: float | None = None
        if first_high < third_low:
            side = "bullish"
            low = first_high
            high = third_low
            fully_filled = any((_float_or_none(candle[3]) or float("inf")) <= low for candle in closed[index + 3 :])
        elif first_low > third_high:
            side = "bearish"
            low = third_high
            high = first_low
            fully_filled = any((_float_or_none(candle[2]) or float("-inf")) >= high for candle in closed[index + 3 :])
        else:
            continue

        if fully_filled or low is None or high is None:
            continue

        in_zone = low <= latest_price <= high
        nearest = low if latest_price < low else high if latest_price > high else latest_price
        distance_pct = ((latest_price / nearest) - 1) * 100 if nearest > 0 else None
        candidates.append(
            {
                "daily_fvg_side": side,
                "daily_fvg_low": low,
                "daily_fvg_high": high,
                "daily_fvg_age_days": len(closed) - (index + 3),
                "daily_fvg_distance_pct": distance_pct or 0.0,
                "daily_fvg_test": in_zone,
            }
        )

    if not candidates:
        return empty

    return min(candidates, key=lambda item: abs(float(item["daily_fvg_distance_pct"])))


def _order_book_metrics(
    raw_order_book: dict[str, Any] | None,
    price: float | None,
    proximity_pct: float = 0.8,
) -> dict[str, float | str | None]:
    if not raw_order_book or price is None or price <= 0:
        return {
            "order_book_bid_wall_usd": None,
            "order_book_ask_wall_usd": None,
            "order_book_imbalance_pct": None,
            "order_book_wall_side": None,
            "order_book_wall_distance_pct": None,
        }

    lower = price * (1 - proximity_pct / 100)
    upper = price * (1 + proximity_pct / 100)
    bids: list[tuple[float, float, float]] = []
    asks: list[tuple[float, float, float]] = []

    for raw_price, raw_qty in raw_order_book.get("bids", []):
        level_price = _float_or_none(raw_price)
        qty = _float_or_none(raw_qty)
        if level_price is None or qty is None or level_price <= 0 or qty <= 0 or level_price < lower:
            continue
        bids.append((level_price, qty, level_price * qty))

    for raw_price, raw_qty in raw_order_book.get("asks", []):
        level_price = _float_or_none(raw_price)
        qty = _float_or_none(raw_qty)
        if level_price is None or qty is None or level_price <= 0 or qty <= 0 or level_price > upper:
            continue
        asks.append((level_price, qty, level_price * qty))

    bid_sum = sum(item[2] for item in bids)
    ask_sum = sum(item[2] for item in asks)
    total = bid_sum + ask_sum
    imbalance = ((bid_sum - ask_sum) / total) * 100 if total > 0 else None
    largest_bid = max(bids, key=lambda item: item[2], default=None)
    largest_ask = max(asks, key=lambda item: item[2], default=None)
    bid_wall = largest_bid[2] if largest_bid else None
    ask_wall = largest_ask[2] if largest_ask else None

    if bid_wall is not None and (ask_wall is None or bid_wall >= ask_wall):
        wall_side = "bid"
        wall_price = largest_bid[0] if largest_bid else None
    elif ask_wall is not None:
        wall_side = "ask"
        wall_price = largest_ask[0] if largest_ask else None
    else:
        wall_side = None
        wall_price = None

    return {
        "order_book_bid_wall_usd": bid_wall,
        "order_book_ask_wall_usd": ask_wall,
        "order_book_imbalance_pct": imbalance,
        "order_book_wall_side": wall_side,
        "order_book_wall_distance_pct": ((wall_price / price) - 1) * 100 if wall_price else None,
    }


async def build_binance_metric_input(symbol: str, adapter: BinanceFuturesAdapter | None = None) -> MarketMetricInput:
    """Fetch a minimal REST snapshot for a symbol.

    This is intentionally small: live ingestion will later move to WebSockets,
    while REST remains useful for bootstrap and recovery.
    """

    adapter = adapter or BinanceFuturesAdapter()
    snapshot = await fetch_binance_market_snapshot(symbol, adapter)
    return snapshot.metric_input


async def fetch_binance_market_snapshot(
    symbol: str,
    adapter: BinanceFuturesAdapter | None = None,
) -> BinanceMarketSnapshot:
    adapter = adapter or BinanceFuturesAdapter()
    klines_result, open_interest_result, ticker_result, klines_4h_result, klines_1d_result, order_book_result = await asyncio.gather(
        adapter.get_klines(symbol=symbol, interval="5m", limit=288),
        adapter.get_open_interest(symbol),
        adapter.get_24h_ticker(symbol),
        adapter.get_klines(symbol=symbol, interval="4h", limit=200),
        adapter.get_klines(symbol=symbol, interval="1d", limit=200),
        adapter.get_order_book(symbol=symbol, limit=100),
        return_exceptions=True,
    )

    if isinstance(klines_result, Exception):
        raise klines_result
    if isinstance(open_interest_result, Exception):
        raise open_interest_result
    if isinstance(ticker_result, Exception):
        raise ticker_result

    klines = klines_result
    open_interest = open_interest_result
    ticker = ticker_result
    klines_4h = [] if isinstance(klines_4h_result, Exception) else klines_4h_result
    klines_1d = [] if isinstance(klines_1d_result, Exception) else klines_1d_result
    order_book = None if isinstance(order_book_result, Exception) else order_book_result

    try:
        open_interest_history = await adapter.get_open_interest_history(symbol=symbol, period="5m", limit=4)
    except Exception:
        open_interest_history = []

    candles = [adapter.normalize_kline(raw, symbol=symbol, interval="5m") for raw in klines]
    closed = [candle for candle in candles if candle.is_closed]
    latest = closed[-1] if closed else None
    previous_5m = closed[-2] if len(closed) >= 2 else None
    previous_15m = closed[-4] if len(closed) >= 4 else None
    previous_1h = closed[-13] if len(closed) >= 13 else None
    previous_24h = closed[0] if len(closed) >= 288 else None

    last_price = _float_or_none(ticker.get("lastPrice")) if isinstance(ticker, dict) else None
    price_for_oi = last_price or (latest.close if latest else None)

    oi_contracts_now = _float_or_none(open_interest.get("openInterest"))
    oi_usd_now = _open_interest_usd(oi_contracts_now, price_for_oi)
    oi_usd_15m_ago = None
    circulating_market_cap = None
    if len(open_interest_history) >= 4:
        historical_value = _float_or_none(open_interest_history[0].get("sumOpenInterestValue"))
        historical_contracts = _float_or_none(open_interest_history[0].get("sumOpenInterest"))
        oi_usd_15m_ago = historical_value or _open_interest_usd(historical_contracts, previous_15m.close if previous_15m else price_for_oi)
        circulating_supply = _float_or_none(open_interest_history[-1].get("CMCCirculatingSupply"))
        circulating_market_cap = circulating_supply * price_for_oi if circulating_supply is not None and price_for_oi is not None else None

    quote_volume_15m = sum(candle.quote_volume for candle in closed[-3:]) if len(closed) >= 3 else None
    quote_volume_15m_history = _rolling_sum([candle.quote_volume for candle in closed[:-1]], 3)
    consolidation_range_1h_pct, consolidation_breakout_pct, consolidation_breakout_level = _consolidation_breakout_from_candles(closed)
    quote_volume_24h = _float_or_none(ticker.get("quoteVolume")) if isinstance(ticker, dict) else None
    base_metrics = _base_metrics_from_daily_klines(klines_1d, price_for_oi, quote_volume_24h)
    daily_fvg_metrics = _daily_fvg_metrics_from_klines(klines_1d, price_for_oi)
    order_book_metrics = _order_book_metrics(order_book, price_for_oi)

    metric_input = MarketMetricInput(
        exchange="binance",
        market_type="futures",
        symbol=symbol,
        ts=datetime.now(timezone.utc),
        close_now=latest.close if latest else None,
        close_5m_ago=previous_5m.close if previous_5m else None,
        close_15m_ago=previous_15m.close if previous_15m else None,
        close_1h_ago=previous_1h.close if previous_1h else None,
        close_24h_ago=previous_24h.close if previous_24h else None,
        quote_volume_5m=latest.quote_volume if latest else None,
        quote_volume_5m_history=[candle.quote_volume for candle in closed[:-1]],
        quote_volume_15m=quote_volume_15m,
        quote_volume_15m_history=quote_volume_15m_history,
        quote_volume_24h=quote_volume_24h,
        consolidation_range_1h_pct=consolidation_range_1h_pct,
        consolidation_breakout_pct=consolidation_breakout_pct,
        consolidation_breakout_level=consolidation_breakout_level,
        oi_usd_now=oi_usd_now,
        circulating_market_cap=circulating_market_cap,
        oi_usd_15m_ago=oi_usd_15m_ago,
        base_days=base_metrics["base_days"],
        base_high=base_metrics["base_high"],
        base_low=base_metrics["base_low"],
        base_range_pct=base_metrics["base_range_pct"],
        base_distance_to_high_pct=base_metrics["base_distance_to_high_pct"],
        base_breakout_pct=base_metrics["base_breakout_pct"],
        base_volume_dry_up_ratio=base_metrics["base_volume_dry_up_ratio"],
        base_prebreak_volume_ratio=base_metrics["base_prebreak_volume_ratio"],
        daily_fvg_side=daily_fvg_metrics["daily_fvg_side"],
        daily_fvg_low=daily_fvg_metrics["daily_fvg_low"],
        daily_fvg_high=daily_fvg_metrics["daily_fvg_high"],
        daily_fvg_age_days=daily_fvg_metrics["daily_fvg_age_days"],
        daily_fvg_distance_pct=daily_fvg_metrics["daily_fvg_distance_pct"],
        daily_fvg_test=daily_fvg_metrics["daily_fvg_test"],
        cvd_15m=_cvd_15m_from_candles(closed),
        order_book_bid_wall_usd=order_book_metrics["order_book_bid_wall_usd"],
        order_book_ask_wall_usd=order_book_metrics["order_book_ask_wall_usd"],
        order_book_imbalance_pct=order_book_metrics["order_book_imbalance_pct"],
        order_book_wall_side=order_book_metrics["order_book_wall_side"],
        order_book_wall_distance_pct=order_book_metrics["order_book_wall_distance_pct"],
        ema_4h_50=_ema_from_raw_klines(klines_4h, 50),
        ema_4h_100=_ema_from_raw_klines(klines_4h, 100),
        ema_1d_50=_ema_from_raw_klines(klines_1d, 50),
        ema_1d_100=_ema_from_raw_klines(klines_1d, 100),
    )

    return BinanceMarketSnapshot(symbol=symbol, metric_input=metric_input, candles=closed, candles_count=len(closed))
