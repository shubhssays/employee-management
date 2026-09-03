"""
Request ID middleware.

Assigns a unique request ID to every incoming HTTP request.

Behavior:
  - If the client sends X-Request-ID, the value is used as-is.
  - Otherwise, a new UUID is generated.
  - The ID is bound to the structlog context for the duration of the request.
  - The ID is echoed back in the X-Request-ID response header.
  - The ID is available in error responses via the request_id field.

This makes every log line for a request traceable by a single ID.
"""

import uuid

import structlog
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response
from starlette.types import ASGIApp

REQUEST_ID_HEADER = "X-Request-ID"


class RequestIDMiddleware(BaseHTTPMiddleware):
    """Assigns and propagates a unique request ID for each HTTP request."""

    def __init__(self, app: ASGIApp) -> None:
        super().__init__(app)

    async def dispatch(self, request: Request, call_next: object) -> Response:
        # Use client-provided ID or generate a new one
        request_id = request.headers.get(REQUEST_ID_HEADER, f"req_{uuid.uuid4().hex[:12]}")
        request.state.request_id = request_id

        # Bind to structlog context — all log entries during this request carry this ID
        structlog.contextvars.clear_contextvars()
        structlog.contextvars.bind_contextvars(request_id=request_id)

        response: Response = await call_next(request)  # type: ignore[operator]

        # Echo the ID back in response headers
        response.headers[REQUEST_ID_HEADER] = request_id
        return response
