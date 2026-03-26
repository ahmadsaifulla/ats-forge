"""FastAPI application entrypoint."""

from __future__ import annotations

from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from app.api.routes import router
from app.core.config import get_settings
from app.core.logging import configure_logging
from app.utils.errors import ATSForgeError


@asynccontextmanager
async def lifespan(_: FastAPI):
    """Prepare application resources."""

    configure_logging()
    get_settings()
    yield


def create_app() -> FastAPI:
    """Create and configure the FastAPI app."""

    settings = get_settings()
    app = FastAPI(
        title=settings.app_name,
        version=settings.app_version,
        debug=settings.debug,
        lifespan=lifespan,
    )
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.cors_origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    app.include_router(router, prefix=settings.api_prefix)

    @app.exception_handler(ATSForgeError)
    async def handle_ats_error(_, exc: ATSForgeError):
        return JSONResponse(
            status_code=exc.status_code,
            content={"error": exc.error, "reason": exc.reason},
        )

    @app.exception_handler(RequestValidationError)
    async def handle_validation_error(_, exc: RequestValidationError):
        message = "; ".join(error["msg"] for error in exc.errors())
        return JSONResponse(
            status_code=422,
            content={"error": "validation_error", "reason": message},
        )

    @app.get("/health")
    async def healthcheck():
        return {"status": "ok"}

    return app


app = create_app()
