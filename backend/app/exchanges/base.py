from abc import ABC, abstractmethod
from typing import Any


class ExchangeAdapter(ABC):
    code: str

    @abstractmethod
    async def get_klines(self, symbol: str, interval: str, limit: int = 500) -> list[dict[str, Any]]:
        raise NotImplementedError

    @abstractmethod
    async def get_24h_ticker(self, symbol: str | None = None) -> dict[str, Any] | list[dict[str, Any]]:
        raise NotImplementedError

    @abstractmethod
    async def get_open_interest(self, symbol: str) -> dict[str, Any]:
        raise NotImplementedError
