from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

import httpx

from app.core.config import get_settings
from app.domain.entities import Candle
from app.exchanges.base import ExchangeAdapter


def _dt_from_ms(value: int) -> datetime:
    return datetime.fromtimestamp(value / 1000, tz=timezone.utc)


class BinanceFuturesAdapter(ExchangeAdapter):
    code = "binance"

    def __init__(self, base_url: str | None = None, timeout: float = 10.0) -> None:
        self.base_url = base_url or get_settings().binance_futures_base_url
        self.timeout = timeout

    async def _get(self, path: str, params: dict[str, Any]) -> Any:
        async with httpx.AsyncClient(base_url=self.base_url, timeout=self.timeout) as client:
            response = await client.get(path, params=params)
            response.raise_for_status()
            return response.json()

    async def get_klines(self, symbol: str, interval: str, limit: int = 500) -> list[dict[str, Any]]:
        return await self._get("/fapi/v1/klines", {"symbol": symbol, "interval": interval, "limit": limit})

    async def get_24h_ticker(self, symbol: str | None = None) -> dict[str, Any] | list[dict[str, Any]]:
        params = {"symbol": symbol} if symbol else {}
        return await self._get("/fapi/v1/ticker/24hr", params)

    async def get_exchange_info(self) -> dict[str, Any]:
        return await self._get("/fapi/v1/exchangeInfo", {})

    async def get_open_interest(self, symbol: str) -> dict[str, Any]:
        return await self._get("/fapi/v1/openInterest", {"symbol": symbol})

    async def get_open_interest_history(self, symbol: str, period: str = "5m", limit: int = 4) -> list[dict[str, Any]]:
        return await self._get(
            "/futures/data/openInterestHist",
            {"symbol": symbol, "period": period, "limit": limit},
        )

    async def get_order_book(self, symbol: str, limit: int = 100) -> dict[str, Any]:
        return await self._get("/fapi/v1/depth", {"symbol": symbol, "limit": limit})

    @staticmethod
    def normalize_kline(raw: list[Any], symbol: str, interval: str) -> Candle:
        return Candle(
            exchange="binance",
            market_type="futures",
            symbol=symbol,
            timeframe=interval,
            open_time=_dt_from_ms(int(raw[0])),
            open=float(raw[1]),
            high=float(raw[2]),
            low=float(raw[3]),
            close=float(raw[4]),
            base_volume=float(raw[5]),
            close_time=_dt_from_ms(int(raw[6])),
            quote_volume=float(raw[7]),
            trade_count=int(raw[8]) if raw[8] is not None else None,
            taker_buy_base_volume=float(raw[9]) if len(raw) > 9 and raw[9] is not None else None,
            taker_buy_quote_volume=float(raw[10]) if len(raw) > 10 and raw[10] is not None else None,
            is_closed=True,
        )
