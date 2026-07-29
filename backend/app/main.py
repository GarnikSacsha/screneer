from pathlib import Path

from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from starlette.middleware.trustedhost import TrustedHostMiddleware

from app.api.routes import router
from app.core.config import Settings, get_settings

ROOT_DIR = Path(__file__).resolve().parents[2]
STATIC_FILES = {
    "/": ROOT_DIR / "index.html",
    "/index.html": ROOT_DIR / "index.html",
    "/app.js": ROOT_DIR / "app.js",
    "/styles.css": ROOT_DIR / "styles.css",
    "/assets/favicon.svg": ROOT_DIR / "assets" / "favicon.svg",
    "/favicon.ico": ROOT_DIR / "assets" / "favicon.svg",
}


def create_app(settings: Settings | None = None) -> FastAPI:
    settings = settings or get_settings()
    app = FastAPI(
        title=settings.app_name,
        version="0.1.0",
        docs_url=None if settings.is_production else "/docs",
        redoc_url=None if settings.is_production else "/redoc",
        openapi_url=None if settings.is_production else "/openapi.json",
    )
    app.add_middleware(TrustedHostMiddleware, allowed_hosts=settings.allowed_hosts)
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.allowed_origins,
        allow_credentials=False,
        allow_methods=["GET", "POST", "OPTIONS"],
        allow_headers=["Content-Type", "X-Quant-Desk-Key"],
    )

    @app.middleware("http")
    async def security_headers(request: Request, call_next):
        response = await call_next(request)
        response.headers["Content-Security-Policy"] = (
            "default-src 'self'; "
            "base-uri 'none'; "
            "connect-src 'self' http://127.0.0.1:8000 http://localhost:8000; "
            "frame-ancestors 'none'; "
            "form-action 'self'; "
            "img-src 'self' data:; "
            "object-src 'none'; "
            "script-src 'self'; "
            "style-src 'self' 'unsafe-inline'"
        )
        response.headers["Cross-Origin-Opener-Policy"] = "same-origin"
        response.headers["Cross-Origin-Resource-Policy"] = "same-origin"
        response.headers["Permissions-Policy"] = "camera=(), microphone=(), geolocation=()"
        response.headers["Referrer-Policy"] = "no-referrer"
        response.headers["X-Content-Type-Options"] = "nosniff"
        response.headers["X-Frame-Options"] = "DENY"
        if request.url.path.startswith("/api/"):
            response.headers["Cache-Control"] = "no-store"
        if settings.is_production:
            response.headers["Strict-Transport-Security"] = "max-age=31536000; includeSubDomains"
        return response

    app.include_router(router, prefix="/api")

    @app.get("/", include_in_schema=False)
    @app.get("/index.html", include_in_schema=False)
    @app.get("/app.js", include_in_schema=False)
    @app.get("/styles.css", include_in_schema=False)
    @app.get("/assets/favicon.svg", include_in_schema=False)
    @app.get("/favicon.ico", include_in_schema=False)
    async def static_asset(request: Request) -> FileResponse:
        path = STATIC_FILES.get(request.url.path)
        if path is None or not path.exists():
            raise HTTPException(status_code=404, detail="Static asset not found")
        return FileResponse(path)

    return app


app = create_app()
