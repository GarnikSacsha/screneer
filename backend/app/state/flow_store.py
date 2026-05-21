from __future__ import annotations

import json
from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Any

import redis.asyncio as redis


RETENTION_MS = 60 * 60 * 1000
WINDOW_MS = 15 * 60 * 1000


@dataclass(frozen=True)
class LiquidationWindow:
    liquidations_15m_usd: float | None = None
    long_liquidations_15m_usd: float | None = None
    short_liquidations_15m_usd: float | None = None


def liquidation_key(exchange: str, market_type: str, symbol: str) -> str:
    return f"flow:liquidations:{exchange}:{market_type}:{symbol}"


def _now_ms() -> int:
    return int(datetime.now(timezone.utc).timestamp() * 1000)


async def save_liquidation_event(
    client: redis.Redis,
    *,
    exchange: str,
    market_type: str,
    symbol: str,
    event_time_ms: int,
    side: str,
    usd: float,
) -> None:
    key = liquidation_key(exchange, market_type, symbol)
    payload = {
        "event_time_ms": event_time_ms,
        "side": side,
        "usd": usd,
    }
    member = json.dumps(payload, separators=(",", ":"), ensure_ascii=False)
    pipeline = client.pipeline()
    pipeline.zadd(key, {member: event_time_ms})
    pipeline.zremrangebyscore(key, 0, event_time_ms - RETENTION_MS)
    await pipeline.execute()


async def get_liquidation_window(
    client: redis.Redis,
    *,
    exchange: str,
    market_type: str,
    symbol: str,
    window_ms: int = WINDOW_MS,
) -> LiquidationWindow:
    key = liquidation_key(exchange, market_type, symbol)
    cutoff = _now_ms() - window_ms
    values = await client.zrangebyscore(key, cutoff, "+inf")

    if not values:
        return LiquidationWindow()

    long_usd = 0.0
    short_usd = 0.0
    for value in values:
        item: dict[str, Any] = json.loads(value)
        side = str(item.get("side", "")).upper()
        usd = float(item.get("usd") or 0.0)
        if side == "SELL":
            long_usd += usd
        elif side == "BUY":
            short_usd += usd

    total = long_usd + short_usd
    return LiquidationWindow(
        liquidations_15m_usd=total if total > 0 else None,
        long_liquidations_15m_usd=long_usd if long_usd > 0 else None,
        short_liquidations_15m_usd=short_usd if short_usd > 0 else None,
    )
