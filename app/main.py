"""
FastAPI application factory.

This module creates and configures the FastAPI application instance.
It wires together:
  - Configuration loading
  - Logging initialization
  - Middleware (request ID, CORS, request logging)
  - Exception handlers
  - API router registration (versioned under /api/v1)
  - Application lifespan (startup/shutdown hooks)

Usage:
    uv run uvicorn app.main:app --reload

The `app` symbol at the bottom of this file is the ASGI entry point.
"""

from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager

import structlog
from fastapi import FastAPI
from fastapi.exceptions import HTTPException, RequestValidationError
from fastapi.middleware.cors import CORSMiddleware

from app.api.exception_handlers import (
    app_exception_handler,
    http_exception_handler,
    unhandled_exception_handler,
    validation_exception_handler,
)
from app.api.v1.router import api_router
from app.core.config import settings
from app.core.exceptions import AppException
from app.core.logging import configure_logging
from app.middleware.logging import RequestLoggingMiddleware
from app.middleware.request_id import RequestIDMiddleware

logger = structlog.get_logger(__name__)


# ---------------------------------------------------------------------------
# Lifespan — startup and shutdown hooks
# ---------------------------------------------------------------------------


@asynccontextmanager
async def lifespan(application: FastAPI) -> AsyncGenerator[None, None]:
    """
    Application lifespan context manager.

    Startup: configure logging, verify database connectivity, start scheduler.
    Shutdown: stop scheduler, close database connections.
    """
    # ── Startup ──────────────────────────────────────────────────────────
    configure_logging()
    logger.info(
        "application_starting",
        app_name=settings.APP_NAME,
        environment=settings.APP_ENV,
        debug=settings.DEBUG,
    )

    # Database connectivity check
    try:
        from sqlalchemy import text

        from app.db.session import engine

        async with engine.connect() as conn:
            await conn.execute(text("SELECT 1"))
        logger.info("database_connected")
    except Exception as exc:
        logger.error("database_connection_failed", exc_info=exc)
        raise exc

    # TODO (Phase 1 enhancement): Start APScheduler here
    # if settings.SCHEDULER_ENABLED:
    #     from app.scheduler import start_scheduler
    #     start_scheduler()

    logger.info("application_ready")

    yield  # Application runs here

    # ── Shutdown ──────────────────────────────────────────────────────────
    logger.info("application_shutting_down")

    # TODO: Stop APScheduler here
    # TODO: Close database engine pool explicitly if needed

    logger.info("application_stopped")


# ---------------------------------------------------------------------------
# Application factory
# ---------------------------------------------------------------------------


def create_application() -> FastAPI:
    """
    Create and configure the FastAPI application.

    Centralizing creation here allows easy testing by creating
    fresh application instances per test with different config.
    """
    application = FastAPI(
        title=settings.APP_NAME,
        description=(
            "Multi-tenant SaaS for work tracking, attendance, and leave management. "
            "See /api/v1/docs for the interactive API documentation."
        ),
        version="1.0.0",
        docs_url=f"{settings.API_V1_PREFIX}/docs",
        redoc_url=f"{settings.API_V1_PREFIX}/redoc",
        openapi_url=f"{settings.API_V1_PREFIX}/openapi.json",
        lifespan=lifespan,
    )

    # ── Middleware (order matters — applied in reverse registration order) ─
    # RequestID must be outermost so request_id is in context for all other middleware
    application.add_middleware(RequestIDMiddleware)
    application.add_middleware(RequestLoggingMiddleware)
    application.add_middleware(
        CORSMiddleware,
        allow_origins=settings.cors_origins_list,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # ── Exception handlers ─────────────────────────────────────────────────
    application.add_exception_handler(AppException, app_exception_handler)  # type: ignore[arg-type]
    application.add_exception_handler(RequestValidationError, validation_exception_handler)  # type: ignore[arg-type]
    application.add_exception_handler(HTTPException, http_exception_handler)  # type: ignore[arg-type]
    application.add_exception_handler(Exception, unhandled_exception_handler)

    # ── API routers ────────────────────────────────────────────────────────
    application.include_router(api_router, prefix=settings.API_V1_PREFIX)

    return application


# ---------------------------------------------------------------------------
# ASGI entry point
# ---------------------------------------------------------------------------

app = create_application()
