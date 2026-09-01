"""
Unit tests for shared pagination schemas.
"""

import pytest
from pydantic import ValidationError

from app.shared.schemas.pagination import PageParams, PaginatedResponse


class TestPageParams:
    def test_default_values(self) -> None:
        params = PageParams()
        assert params.page == 1
        assert params.page_size == 20

    def test_offset_calculation(self) -> None:
        params = PageParams(page=3, page_size=20)
        assert params.offset == 40  # (3-1) * 20

    def test_limit_equals_page_size(self) -> None:
        params = PageParams(page=1, page_size=50)
        assert params.limit == 50

    def test_page_must_be_positive(self) -> None:
        with pytest.raises(ValidationError):
            PageParams(page=0)

    def test_page_size_max_100(self) -> None:
        with pytest.raises(ValidationError):
            PageParams(page_size=101)

    def test_first_page_offset_is_zero(self) -> None:
        params = PageParams(page=1, page_size=20)
        assert params.offset == 0


class TestPaginatedResponse:
    def test_pages_computed_correctly(self) -> None:
        response = PaginatedResponse[str](
            items=["a", "b"],
            total=47,
            page=1,
            page_size=20,
        )
        assert response.pages == 3  # ceil(47/20)

    def test_pages_exact_division(self) -> None:
        response = PaginatedResponse[str](
            items=[],
            total=40,
            page=1,
            page_size=20,
        )
        assert response.pages == 2

    def test_empty_result(self) -> None:
        response = PaginatedResponse[str](
            items=[],
            total=0,
            page=1,
            page_size=20,
        )
        assert response.pages == 0
        assert response.items == []
