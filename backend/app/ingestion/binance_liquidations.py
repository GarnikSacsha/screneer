from __future__ import annotations

import asyncio
import json
from typing import Any

import websockets

from app.core.config import get_settings
from app.state.flow_store import save_liquidation_event
from app.state.redis_store import get_redis_client


def _float_or_zero(value: Any) -> float:
    try:
        return float(value)
    except (TypeError, ValueError):
        return 0.0


def _liquidation_usd(order: dict[str, Any]) -> float:
    quantity = _float_or_zero(order.get("z")) or _float_or_zero(order.get("q"))
    price = _float_or_zero(order.get("ap")) or _float_or_zero(order.get("p"))
    return quantity * price


async def run_binance_liquidation_stream(reconnect_delay: float = 5.0) -> None:
    """Collect Binance USD-M Futures liquidation events into Redis.

    Binance's REST historical liquidation endpoint currently cannot be used
    reliably, so this worker keeps a rolling Redis window from the public
    `!forceOrder@arr` stream. A SELL liquidation order means long positions
    were force-closed; a BUY liquidation order means shorts were force-closed.
    """

    settings = get_settings()
    url = f"{settings.binance_futures_ws_url.rstrip('/')}/!forceOrder@arr"
    client = get_redis_client()

    try:
        while True:
            try:
                async with websockets.connect(url, ping_interval=20, ping_timeout=20) as websocket:
                    print("binance liquidation stream connected")
                    async for raw in websocket:
                        payload = json.loads(raw)
                        order = payload.get("o") or {}
                        symbol = order.get("s")
                        side = order.get("S")
                        event_time_ms = int(payload.get("E") or order.get("T") or 0)
                        usd = _liquidation_usd(order)

                        if not symbol or not side or event_time_ms <= 0 or usd <= 0:
                            continue

                        await save_liquidation_event(
                            client,
                            exchange="binance",
                            market_type="futures",
                            symbol=symbol,
                            event_time_ms=event_time_ms,
                            side=side,
                            usd=usd,
                        )
            except Exception as exc:  # noqa: BLE001 - the long-lived stream reconnects after any provider failure
                print(f"binance liquidation stream reconnecting after {type(exc).__name__}: {exc}")
                await asyncio.sleep(reconnect_delay)
    finally:
        await client.aclose()
