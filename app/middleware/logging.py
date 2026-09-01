"""
Request logging middleware.

Logs every incoming request and outgoing response with:
  - HTTP method
  - URL path
  - Response status code
  - Duration in milliseconds

Authentication context (user_id, organization_id) is bound to
structlog by the get_current_user dependency — this middleware
only logs transport-level metadata.
"""

import time

import structlog
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response
from starlette.types import ASGIApp

logger = structlog.get_logger(__name__)


class RequestLoggingMiddleware(BaseHTTPMiddleware):
    """Logs every request/response pair with timing."""

    def __init__(self, app: ASGIApp) -> None:
        super().__init__(app)

    async def dispatch(self, request: Request, call_next: object) -> Response:
        start = time.perf_counter()

        logger.info(
            "request_started",
            method=request.method,
            path=request.url.path,
        )

        response: Response = await call_next(request)  # type: ignore[operator]

        duration_ms = round((time.perf_counter() - start) * 1000, 2)

        logger.info(
            "request_finished",
            method=request.method,
            path=request.url.path,
            status_code=response.status_code,
            duration_ms=duration_ms,
        )

        return response
