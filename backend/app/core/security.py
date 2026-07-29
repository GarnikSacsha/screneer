from __future__ import annotations

import asyncio
import secrets
import time
from collections import defaultdict, deque
from typing import Annotated

from fastapi import Header, HTTPException, Request, status

from app.core.config import Settings, get_settings


class SlidingWindowRateLimiter:
    """Small per-process guard for costly demo endpoints.

    Production deployments with multiple workers should replace this with a
    shared gateway or Redis-backed limiter.
    """

    def __init__(self) -> None:
        self._requests: dict[str, deque[float]] = defaultdict(deque)
        self._lock = asyncio.Lock()

    async def check(self, key: str, *, limit: int, window_sec: int) -> int:
        now = time.monotonic()
        cutoff = now - window_sec
        async with self._lock:
            bucket = self._requests[key]
            while bucket and bucket[0] <= cutoff:
                bucket.popleft()
            if len(bucket) >= limit:
                retry_after = max(1, round(window_sec - (now - bucket[0])))
                return retry_after
            bucket.append(now)
        return 0

    async def reset(self) -> None:
        async with self._lock:
            self._requests.clear()


expensive_endpoint_limiter = SlidingWindowRateLimiter()


def _client_key(request: Request) -> str:
    # Do not trust X-Forwarded-For unless a deployment configures a trusted proxy.
    return request.client.host if request.client else "unknown"


def _verify_admin_key(settings: Settings, provided_key: str | None) -> None:
    configured = settings.admin_api_key
    if settings.is_production and configured is None:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Protected endpoints are disabled until ADMIN_API_KEY is configured",
        )
    if configured is None:
        return

    expected = configured.get_secret_value()
    if not provided_key or not secrets.compare_digest(provided_key, expected):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="A valid API key is required",
            headers={"WWW-Authenticate": "API-Key"},
        )


async def require_expensive_access(
    request: Request,
    api_key: Annotated[str | None, Header(alias="X-Quant-Desk-Key")] = None,
) -> None:
    settings = get_settings()
    _verify_admin_key(settings, api_key)

    retry_after = await expensive_endpoint_limiter.check(
        f"{_client_key(request)}:{request.url.path}",
        limit=settings.expensive_rate_limit_requests,
        window_sec=settings.expensive_rate_limit_window_sec,
    )
    if retry_after:
        raise HTTPException(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail="Request budget exceeded",
            headers={"Retry-After": str(retry_after)},
        )
