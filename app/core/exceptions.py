"""
Centralized exception hierarchy and HTTP error mapping.

All application exceptions descend from AppException.
A single FastAPI exception handler in main.py catches AppException
and converts it to the standard error response shape:

    {
        "error": {
            "code": "SNAKE_CASE_CODE",
            "message": "Human readable description",
            "details": null | {...} | [...]
        }
    }

Never let framework-internal exception types leak to the HTTP layer.
"""

from typing import Any


class AppError(Exception):  # noqa: N818 — intentional base name
    """
    Base for all application-defined exceptions.

    Subclasses set their own default status_code and error_code
    so that every raise site stays clean — no HTTP details scattered
    across the service/domain layers.
    """

    status_code: int = 500
    error_code: str = "INTERNAL_SERVER_ERROR"

    def __init__(
            self,
            message: str | None = None,
            details: Any = None,
            error_code: str | None = None,
    ) -> None:
        self.message = message or "An unexpected error occurred."
        self.details = details
        if error_code:
            self.error_code = error_code
        super().__init__(self.message)


# Backward-compatible alias — import AppException anywhere that needs the base
AppException = AppError


# ---------------------------------------------------------------------------
# 400 — Bad Request
# ---------------------------------------------------------------------------
class BadRequestError(AppException):
    status_code = 400
    error_code = "BAD_REQUEST"


# ---------------------------------------------------------------------------
# 401 — Unauthenticated
# ---------------------------------------------------------------------------
class AuthenticationError(AppException):
    status_code = 401
    error_code = "AUTHENTICATION_REQUIRED"


class InvalidCredentialsError(AppException):
    status_code = 401
    error_code = "INVALID_CREDENTIALS"


class TokenExpiredError(AppException):
    status_code = 401
    error_code = "TOKEN_EXPIRED"


class TokenInvalidError(AppException):
    status_code = 401
    error_code = "TOKEN_INVALID"


class TokenNotFoundError(AppException):
    status_code = 401
    error_code = "TOKEN_NOT_FOUND"


class RefreshTokenExpiredError(AppException):
    status_code = 401
    error_code = "REFRESH_TOKEN_EXPIRED"


# ---------------------------------------------------------------------------
# 403 — Forbidden
# ---------------------------------------------------------------------------
class ForbiddenError(AppException):
    status_code = 403
    error_code = "INSUFFICIENT_PERMISSIONS"


class AccountDeactivatedError(AppException):
    status_code = 403
    error_code = "ACCOUNT_DEACTIVATED"


class AccessDeniedError(AppException):
    status_code = 403
    error_code = "ACCESS_DENIED"


# ---------------------------------------------------------------------------
# 404 — Not Found
# ---------------------------------------------------------------------------
class NotFoundError(AppException):
    status_code = 404
    error_code = "NOT_FOUND"


# ---------------------------------------------------------------------------
# 409 — Conflict
# ---------------------------------------------------------------------------
class ConflictError(AppException):
    status_code = 409
    error_code = "CONFLICT"


# ---------------------------------------------------------------------------
# 422 — Unprocessable
# ---------------------------------------------------------------------------
class UnprocessableError(AppException):
    status_code = 422
    error_code = "UNPROCESSABLE"
