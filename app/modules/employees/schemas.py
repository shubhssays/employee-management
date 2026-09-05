from datetime import datetime
from typing import Literal

from pydantic import BaseModel, ConfigDict, EmailStr, Field, SecretStr

from app.core.enums import DepartmentType


class EmployeeCreate(BaseModel):
    """Prevents extra data in body"""
    model_config = ConfigDict(extra="forbid")

    first_name: str = Field(min_length=3, max_length=50, description="Employee Firstname")
    last_name: str = Field(min_length=3, max_length=50, description="Employee Lastname")
    email: EmailStr = Field(description="Emmployee field")
    mobile: str | None = Field(default=None, min_length=5, max_length=50, description="Employee Mobile")
    password: SecretStr = Field(description="Employee password")
    address: str | None = Field(default=None, min_length=5, max_length=200, description="Employee Address")
    department: DepartmentType = Field("Employee Department")
    organization_id: int = Field(gt=0, description="Organization Id to which employee belongs to")


class EmployeeCreateResponse(BaseModel):
    # Without this, we would have to manually map every field.
    model_config = {"from_attributes": True}

    id: int
    first_name: str
    last_name: str | None = None
    email: str
    mobile: str | None = None
    address: str | None = None
    department: DepartmentType
    organization_id: int
    created_at: datetime
    updated_at: datetime | None = None


class EmployeeDetailResponse(EmployeeCreateResponse):
    organization_name: str | None = None
    created_by_admin_name: str | None = None
    updated_by_admin_name: str | None = None
    created_by_employee_name: str | None = None
    updated_by_employee_name: str | None = None


class EmployeeUpdate(BaseModel):
    """Prevents extra data in body"""
    model_config = ConfigDict(extra="forbid")

    first_name: str | None = Field(default=None, min_length=3, max_length=50, description="Employee Firstname")
    last_name: str | None = Field(default=None, min_length=3, max_length=50, description="Employee Lastname")
    email: EmailStr | None = Field(default=None, description="Employee field")
    mobile: str | None = Field(default=None, min_length=5, max_length=50, description="Employee Mobile")
    password: SecretStr | None = Field(default=None, description="Employee password")
    address: str | None = Field(default=None, min_length=5, max_length=200, description="Employee Address")
    is_active: bool | None = Field(default=None, description="Flags employee active or inactive")


class EmployeeGetList(BaseModel):
    ids: list[int] | None = Field(default=None, description="Id(s) of Employee")
    organization_ids: list[int] | None = Field(default=None, description="Filter using organization_id(s)")
    departments: list[str] | None = Field(default=None, description="Filter using department(s)")
    email: str | None = Field(default=None, description="Search using email of Employee")
    mobile: str | None = Field(default=None, description="Search using mobile of Employee")
    first_name: str | None = Field(default=None, description="Search using first_name of Employee")
    last_name: str | None = Field(default=None, description="Search using last_name of Employee")
    page: int | None = Field(default=1, ge=1)
    page_size: int | None = Field(default=20, ge=1, le=100)
    sort_by: Literal[
        "id", "organization_id", "department", "first_name", "last_name", "created_at", "updated_at"] = "created_at"
    sort_order: Literal["asc", "desc"] = "desc"


class EmployeeListResponse(BaseModel):
    items: list[EmployeeDetailResponse]
    total: int
    page: int
    page_size: int
    pages: int
