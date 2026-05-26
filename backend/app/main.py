from pathlib import Path

from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware

from app.api.routes import router
from app.core.config import get_settings

ROOT_DIR = Path(__file__).resolve().parents[2]
STATIC_FILES = {
    "/": ROOT_DIR / "index.html",
    "/index.html": ROOT_DIR / "index.html",
    "/app.js": ROOT_DIR / "app.js",
    "/styles.css": ROOT_DIR / "styles.css",
}


def create_app() -> FastAPI:
    settings = get_settings()
    app = FastAPI(title=settings.app_name, version="0.1.0")
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=False,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    app.include_router(router, prefix="/api")

    @app.get("/", include_in_schema=False)
    @app.get("/index.html", include_in_schema=False)
    @app.get("/app.js", include_in_schema=False)
    @app.get("/styles.css", include_in_schema=False)
    async def static_asset(request: Request) -> FileResponse:
        path = STATIC_FILES.get(request.url.path)
        if path is None or not path.exists():
            raise HTTPException(status_code=404, detail="Static asset not found")
        return FileResponse(path)

    return app


app = create_app()
