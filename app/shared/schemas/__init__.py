# shared/schemas package
from app.shared.schemas.errors import ErrorResponse, ErrorBody, ValidationErrorDetail
from app.shared.schemas.pagination import PageParams, PaginatedResponse
from app.shared.schemas.response import SuccessResponse

__all__ = [
    "SuccessResponse",
    "ErrorResponse",
    "ErrorBody",
    "ValidationErrorDetail",
    "PageParams",
    "PaginatedResponse"
]
