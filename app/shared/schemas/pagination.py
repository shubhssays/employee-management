"""
Pagination schemas used by all list endpoints.

All list endpoints return a PaginatedResponse envelope.
Query parameters follow the PageParams model.

Example request:
    GET /api/v1/employees?page=2&page_size=20

Example response:
    {
        "items": [...],
        "total": 47,
        "page": 2,
        "page_size": 20,
        "pages": 3
    }
"""

import math
from typing import Generic, TypeVar

from pydantic import BaseModel, Field, computed_field

T = TypeVar("T")


class PageParams(BaseModel):
    """Query parameters for paginated list endpoints."""

    page: int = Field(default=1, ge=1, description="Page number (1-indexed)")
    page_size: int = Field(default=20, ge=1, le=100, description="Items per page (max 100)")

    @property
    def offset(self) -> int:
        return (self.page - 1) * self.page_size

    @property
    def limit(self) -> int:
        return self.page_size


class PaginatedResponse(BaseModel, Generic[T]):
    """
    Standard paginated list response envelope.

    Use with a concrete item type:
        PaginatedResponse[EmployeeResponse]
    """

    items: list[T]
    total: int
    page: int
    page_size: int

    @computed_field  # type: ignore[misc]
    @property
    def pages(self) -> int:
        if self.page_size == 0:
            return 0
        return math.ceil(self.total / self.page_size)
