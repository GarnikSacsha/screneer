import asyncio
import json
from pathlib import Path
from typing import Literal

import structlog
from fastapi import APIRouter, Depends, HTTPException
from redis.exceptions import RedisError

from app.agent.context import SnapshotNotFoundError
from app.agent.models import RiskAgentConfigResponse, RiskBriefRequest, RiskBriefResponse
from app.agent.service import build_risk_brief
from app.core.config import get_settings, load_thresholds
from app.core.security import require_expensive_access
from app.ingestion.market_scan import build_scan_universe
from app.ingestion.pipeline import run_binance_snapshot
from app.schemas import (
    AnomalyEventResponse,
    HealthResponse,
    MarketMetricsResponse,
    SectorMetricsResponse,
    SnapshotPreviewResponse,
    SnapshotRunResponse,
)
from app.state.redis_store import (
    get_latest_market_metrics,
    get_latest_sector_metrics,
    get_recent_events,
    get_redis_client,
)

router = APIRouter()
logger = structlog.get_logger(__name__)
REDIS_READ_TIMEOUT_SEC = 0.9
CACHE_PATH = Path(__file__).resolve().parents[3] / "latest-preview.json"


@router.get("/health", response_model=HealthResponse)
async def health() -> HealthResponse:
    settings = get_settings()
    return HealthResponse(status="ok", app=settings.app_name, env=settings.app_env)


@router.get("/agent/config", response_model=RiskAgentConfigResponse)
async def risk_agent_config() -> RiskAgentConfigResponse:
    settings = get_settings()
    return RiskAgentConfigResponse(
        enabled=settings.risk_agent_enabled,
        configured=bool(settings.openai_api_key),
        model=settings.risk_agent_model,
        tools=["get_market_snapshot", "retrieve_risk_playbook"],
    )


@router.post(
    "/agent/risk-brief",
    response_model=RiskBriefResponse,
    dependencies=[Depends(require_expensive_access)],
)
async def risk_brief(request: RiskBriefRequest) -> RiskBriefResponse:
    settings = get_settings()
    if not settings.risk_agent_enabled:
        raise HTTPException(status_code=503, detail="Risk analyst is disabled")
    try:
        return await build_risk_brief(request, settings, CACHE_PATH)
    except SnapshotNotFoundError as exc:
        raise HTTPException(status_code=404, detail="Symbol is unavailable in the latest snapshot") from exc
    except json.JSONDecodeError as exc:
        logger.exception("risk_brief_invalid_snapshot")
        raise HTTPException(status_code=500, detail="Materialized snapshot is invalid") from exc


@router.get("/config/universe", dependencies=[Depends(require_expensive_access)])
async def universe(mode: Literal["core", "expanded", "full"] = "core") -> dict:
    return await build_scan_universe(mode)


@router.get("/config/thresholds")
async def thresholds() -> dict:
    return load_thresholds()


@router.get("/metrics/latest", response_model=list[MarketMetricsResponse])
async def latest_metrics() -> list[MarketMetricsResponse]:
    client = get_redis_client()
    try:
        metrics = await asyncio.wait_for(get_latest_market_metrics(client), timeout=REDIS_READ_TIMEOUT_SEC)
    except (RedisError, TimeoutError, asyncio.TimeoutError):
        return []
    finally:
        await client.aclose()

    return [MarketMetricsResponse(**item.__dict__) for item in metrics]


@router.get("/sectors/latest", response_model=list[SectorMetricsResponse])
async def latest_sectors() -> list[SectorMetricsResponse]:
    client = get_redis_client()
    try:
        metrics = await asyncio.wait_for(get_latest_sector_metrics(client), timeout=REDIS_READ_TIMEOUT_SEC)
    except (RedisError, TimeoutError, asyncio.TimeoutError):
        return []
    finally:
        await client.aclose()

    return [SectorMetricsResponse(**item.__dict__) for item in metrics]


@router.get("/events", response_model=list[AnomalyEventResponse])
async def events() -> list[AnomalyEventResponse]:
    client = get_redis_client()
    try:
        detected = await asyncio.wait_for(get_recent_events(client), timeout=REDIS_READ_TIMEOUT_SEC)
    except (RedisError, TimeoutError, asyncio.TimeoutError):
        return []
    finally:
        await client.aclose()

    return [AnomalyEventResponse(**event.__dict__) for event in detected]


@router.get("/cache/latest-preview")
async def latest_preview_cache() -> dict:
    if not CACHE_PATH.exists():
        raise HTTPException(status_code=404, detail="No cached preview available")

    try:
        payload = json.loads(CACHE_PATH.read_text(encoding="utf-8-sig"))
    except json.JSONDecodeError as exc:
        logger.exception("cached_preview_invalid")
        raise HTTPException(status_code=500, detail="Cached preview is invalid") from exc

    payload.setdefault("universe", await build_scan_universe("core"))
    payload["source"] = "cache"
    return payload


@router.post(
    "/ingestion/binance/snapshot",
    response_model=SnapshotRunResponse,
    dependencies=[Depends(require_expensive_access)],
)
async def binance_snapshot() -> SnapshotRunResponse:
    try:
        result = await run_binance_snapshot()
    except Exception as exc:
        logger.exception("binance_snapshot_failed")
        raise HTTPException(status_code=502, detail="Market snapshot provider is unavailable") from exc

    return SnapshotRunResponse(
        ts=result.ts,
        markets=len(result.market_metrics),
        sectors=len(result.sector_metrics),
        events=len(result.events),
        errors=result.errors,
    )


@router.post(
    "/ingestion/binance/preview",
    response_model=SnapshotPreviewResponse,
    dependencies=[Depends(require_expensive_access)],
)
async def binance_preview(
    mode: Literal["core", "expanded", "full"] = "core",
) -> SnapshotPreviewResponse:
    try:
        universe = await build_scan_universe(mode)
        result = await run_binance_snapshot(
            universe_override=universe,
            persist_db=False,
            write_redis=False,
            read_flow_redis=False,
        )
    except Exception as exc:
        logger.exception("binance_preview_failed", mode=mode)
        raise HTTPException(status_code=502, detail="Market preview provider is unavailable") from exc

    response = SnapshotPreviewResponse(
        ts=result.ts,
        universe=universe,
        market_metrics=[MarketMetricsResponse(**item.__dict__) for item in result.market_metrics],
        sector_metrics=[SectorMetricsResponse(**item.__dict__) for item in result.sector_metrics],
        events=[AnomalyEventResponse(**event.__dict__) for event in result.events],
        errors=result.errors,
    )
    if mode == "core" and response.market_metrics and response.sector_metrics:
        CACHE_PATH.write_text(json.dumps(response.model_dump(mode="json"), ensure_ascii=False), encoding="utf-8")
    return response
