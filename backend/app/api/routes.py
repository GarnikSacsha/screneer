import asyncio
import json
from pathlib import Path

from fastapi import APIRouter, HTTPException
from redis.exceptions import RedisError

from app.core.config import get_settings, load_thresholds, load_universe
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
REDIS_READ_TIMEOUT_SEC = 0.9
CACHE_PATH = Path(__file__).resolve().parents[3] / "latest-preview.json"


@router.get("/health", response_model=HealthResponse)
async def health() -> HealthResponse:
    settings = get_settings()
    return HealthResponse(status="ok", app=settings.app_name, env=settings.app_env)


@router.get("/config/universe")
async def universe(mode: str = "core") -> dict:
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
        raise HTTPException(status_code=500, detail=f"Cached preview is invalid: {exc}") from exc

    payload.setdefault("universe", await build_scan_universe("core"))
    payload["source"] = "cache"
    return payload


@router.post("/ingestion/binance/snapshot", response_model=SnapshotRunResponse)
async def binance_snapshot() -> SnapshotRunResponse:
    try:
        result = await run_binance_snapshot()
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"Snapshot failed: {type(exc).__name__}: {exc}") from exc

    return SnapshotRunResponse(
        ts=result.ts,
        markets=len(result.market_metrics),
        sectors=len(result.sector_metrics),
        events=len(result.events),
        errors=result.errors,
    )


@router.post("/ingestion/binance/preview", response_model=SnapshotPreviewResponse)
async def binance_preview(mode: str = "core") -> SnapshotPreviewResponse:
    try:
        universe = await build_scan_universe(mode)
        result = await run_binance_snapshot(universe_override=universe, persist_db=False, write_redis=False, read_flow_redis=False)
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"Preview failed: {type(exc).__name__}: {exc}") from exc

    return SnapshotPreviewResponse(
        ts=result.ts,
        universe=universe,
        market_metrics=[MarketMetricsResponse(**item.__dict__) for item in result.market_metrics],
        sector_metrics=[SectorMetricsResponse(**item.__dict__) for item in result.sector_metrics],
        events=[AnomalyEventResponse(**event.__dict__) for event in result.events],
        errors=result.errors,
    )
