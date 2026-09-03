"""
Centralized FastAPI exception handlers.

Registered in main.py. Every exception type maps to the standard
error response format so clients never see raw Python tracebacks
or framework-internal error shapes.

Handler registration order:
  1. AppException — all application-defined errors
  2. RequestValidationError — Pydantic 422 validation failures
  3. HTTPException — FastAPI/Starlette HTTP exceptions (e.g., 405 Method Not Allowed)
  4. Exception — catch-all for unexpected errors (always returns 500)

Security: The catch-all handler logs the full traceback internally
but returns a safe, generic message to the client. Internal error
details are NEVER exposed in HTTP responses.
"""

import structlog
from fastapi import Request
from fastapi.exceptions import HTTPException, RequestValidationError
from fastapi.responses import JSONResponse

from app.core.exceptions import AppException
from app.shared.schemas.errors import ErrorBody, ErrorResponse, ValidationErrorDetail

logger = structlog.get_logger(__name__)


def _get_request_id(request: Request) -> str | None:
    return getattr(request.state, "request_id", None) or request.headers.get("X-Request-ID")


async def app_exception_handler(request: Request, exc: AppException) -> JSONResponse:
    """
    Handle all application-defined exceptions (AppException subclasses).
    Maps them to structured JSON error responses with the correct HTTP status.
    """
    logger.warning(
        "application_error",
        error_code=exc.error_code,
        message=exc.message,
        status_code=exc.status_code,
        path=request.url.path,
    )
    body = ErrorResponse(
        error=ErrorBody(
            code=exc.error_code,
            message=exc.message,
            details=exc.details,
            request_id=_get_request_id(request),
        )
    )
    return JSONResponse(status_code=exc.status_code, content=body.model_dump())


async def validation_exception_handler(
    request: Request, exc: RequestValidationError
) -> JSONResponse:
    """
    Handle Pydantic validation errors (422).
    Converts the Pydantic error list into a flat, field-keyed list.
    """
    details = [
        ValidationErrorDetail(
            field=" → ".join(str(loc) for loc in error["loc"]),
            message=error["msg"],
        )
        for error in exc.errors()
    ]
    body = ErrorResponse(
        error=ErrorBody(
            code="VALIDATION_ERROR",
            message="Request validation failed.",
            details=[d.model_dump() for d in details],
            request_id=_get_request_id(request),
        )
    )
    return JSONResponse(status_code=422, content=body.model_dump())


async def http_exception_handler(request: Request, exc: HTTPException) -> JSONResponse:
    """
    Handle FastAPI/Starlette HTTPExceptions (e.g., 404, 405, 422 from routing).
    """
    body = ErrorResponse(
        error=ErrorBody(
            code="HTTP_ERROR",
            message=str(exc.detail),
            request_id=_get_request_id(request),
        )
    )
    return JSONResponse(status_code=exc.status_code, content=body.model_dump())


async def unhandled_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    """
    Catch-all for any exception not handled above.
    Logs the full traceback but returns a safe generic 500 to the client.
    Internal details are NEVER sent to clients.
    """
    logger.error(
        "unhandled_exception",
        path=request.url.path,
        exc_info=exc,
    )
    body = ErrorResponse(
        error=ErrorBody(
            code="INTERNAL_SERVER_ERROR",
            message="An unexpected error occurred. Please try again later.",
            request_id=_get_request_id(request),
        )
    )
    return JSONResponse(status_code=500, content=body.model_dump())
