from pydantic import BaseModel, ConfigDict, EmailStr, SecretStr, Field

from app.core.enums import UserRole


class Login(BaseModel):
    """Prevents extra data in body"""
    model_config = ConfigDict(extra="forbid")

    email: EmailStr
    password: SecretStr


class AdminLoginResponse(BaseModel):
    # Without this, we would have to manually map every field.
    model_config = {"from_attributes": True}

    id: int
    email: str
    name: str
    roles: list[str]
    access_token: str


class LoginResponse(BaseModel):
    # Without this, we would have to manually map every field.
    model_config = {"from_attributes": True}

    id: int
    email: str
    mobile: str | None
    first_name: str
    last_name: str | None
    roles: list[str]
    access_token: str


class SwitchRole(BaseModel):
    """Prevents extra data in body"""
    model_config = ConfigDict(extra="forbid")

    role: UserRole = Field(description="Employee Role slug")
