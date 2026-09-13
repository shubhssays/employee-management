"""
Standard error response schemas.

All error responses from the API follow this structure:

    {
        "error": {
            "code": "SNAKE_CASE_ERROR_CODE",
            "message": "Human-readable description.",
            "details": null | { ... } | [ { "field": ..., "message": ... } ],
        }
    }

Clients should use `error.code` for programmatic error handling,
and `error.message` for display purposes.
"""

from typing import Any

from pydantic import BaseModel


class ValidationErrorDetail(BaseModel):
    """One field-level validation failure within a 422 response."""

    field: str
    message: str


class ErrorBody(BaseModel):
    """The `error` object inside every error response."""

    code: str
    message: str
    details: Any = None  # null | dict | list[ValidationErrorDetail]


class ErrorResponse(BaseModel):
    """Top-level wrapper for every error response body."""

    success: bool = False
    error: ErrorBody
