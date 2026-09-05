from datetime import datetime

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
    email: EmailStr | None = Field(default=None, description="Emmployee field")
    mobile: str | None = Field(default=None, min_length=5, max_length=50, description="Employee Mobile")
    password: SecretStr | None = Field(default=None, description="Employee password")
    address: str | None = Field(default=None, min_length=5, max_length=200, description="Employee Address")
    is_active: bool | None = Field(default=None, description="Flags employee active or inactive")
