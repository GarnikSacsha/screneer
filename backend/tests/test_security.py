from __future__ import annotations

from unittest.mock import patch

import pytest
from fastapi import HTTPException
from httpx import ASGITransport, AsyncClient
from starlette.requests import Request

from app.core.config import Settings
from app.core.security import expensive_endpoint_limiter, require_expensive_access
from app.main import create_app


def _request(path: str = "/api/agent/risk-brief") -> Request:
    return Request(
        {
            "type": "http",
            "http_version": "1.1",
            "method": "POST",
            "scheme": "http",
            "path": path,
            "raw_path": path.encode(),
            "query_string": b"",
            "headers": [],
            "client": ("127.0.0.1", 12345),
            "server": ("testserver", 80),
        }
    )


@pytest.mark.asyncio
async def test_production_fails_closed_without_admin_key():
    settings = Settings(app_env="production", admin_api_key=None)

    with (
        patch("app.core.security.get_settings", return_value=settings),
        pytest.raises(HTTPException) as caught,
    ):
        await require_expensive_access(_request(), None)

    assert caught.value.status_code == 503


@pytest.mark.asyncio
async def test_admin_key_is_compared_before_request_budget():
    settings = Settings(app_env="production", admin_api_key="correct-secret")
    await expensive_endpoint_limiter.reset()

    with patch("app.core.security.get_settings", return_value=settings):
        with pytest.raises(HTTPException) as caught:
            await require_expensive_access(_request(), "wrong-secret")
        await require_expensive_access(_request(), "correct-secret")

    assert caught.value.status_code == 401


@pytest.mark.asyncio
async def test_expensive_endpoint_has_a_request_budget():
    settings = Settings(
        app_env="development",
        expensive_rate_limit_requests=1,
        expensive_rate_limit_window_sec=60,
    )
    await expensive_endpoint_limiter.reset()

    with patch("app.core.security.get_settings", return_value=settings):
        await require_expensive_access(_request(), None)
        with pytest.raises(HTTPException) as caught:
            await require_expensive_access(_request(), None)

    assert caught.value.status_code == 429
    assert caught.value.headers["Retry-After"]


@pytest.mark.asyncio
async def test_security_headers_and_production_docs_policy():
    settings = Settings(
        app_env="production",
        admin_api_key="test-secret",
        allowed_hosts=["testserver"],
        allowed_origins=["https://quant.example"],
    )
    async with AsyncClient(
        transport=ASGITransport(app=create_app(settings)),
        base_url="http://testserver",
    ) as client:
        response = await client.get("/", headers={"Origin": "https://quant.example"})
        docs_response = await client.get("/docs")

    assert response.status_code == 200
    assert response.headers["access-control-allow-origin"] == "https://quant.example"
    assert response.headers["content-security-policy"].startswith("default-src 'self'")
    assert response.headers["strict-transport-security"].startswith("max-age=")
    assert response.headers["x-content-type-options"] == "nosniff"
    assert response.headers["x-frame-options"] == "DENY"
    assert docs_response.status_code == 404
