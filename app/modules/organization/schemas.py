from datetime import datetime
from typing import Literal

from pydantic import BaseModel, Field, ConfigDict


class OrganizationCreate(BaseModel):
    """Schema for POST /organizations."""

    """Prevents extra data in body"""
    model_config = ConfigDict(extra="forbid")

    name: str = Field(min_length=3, max_length=200, description="Organization name")
    slug: str = Field(min_length=3, max_length=200, description="Organization slug")


class OrganizationUpdate(BaseModel):
    """Schema for PATCH /organizations/{organization_id}."""

    """Prevents extra data in body"""
    model_config = ConfigDict(extra="forbid")
    name: str | None = Field(default=None, max_length=200, description="Organization name")
    is_active: bool | None = Field(default=None, description="Organization status")


class OrganizationGetList(BaseModel):
    """Schema for GET /organizations?organization_ids=1,2,3&slug=abc&page=1&page_size=10&sort_by=abc&sort_order=desc"""
    ids: list[int] | None = Field(default=None,description="Id(s) of Organization")
    slugs: list[str] | None = Field(default=None, description="Slug(s) of Organization")
    page: int | None = Field(default=1, ge=1)
    page_size: int | None = Field(default=20, ge=1, le=100)
    sort_by: Literal["id","name","slug","created_at","updated_at"] = "created_at"
    sort_order: Literal["asc", "desc"] = "desc"


class OrganizationResponse(BaseModel):
    """Schema for GET /organizations/{organization_id}."""

    # Without this, we would have to manually map every field.
    model_config = {"from_attributes": True}

    id: int
    name: str
    slug: str
    is_active: bool
    created_at: datetime
    updated_at: datetime | None
    created_by: int
    updated_by: int | None


class OrganizationListResponse(BaseModel):
    """Schema for GET /organizations."""
    items: list[OrganizationResponse]
    total: int
    page: int
    page_size: int
    pages: int
