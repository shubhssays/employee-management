from typing import TypedDict

from pydantic import BaseModel, ConfigDict, EmailStr, Field, SecretStr


class EmployeeToken(TypedDict):
    emp_id: int
    token: str


class ResetTokenResponse(BaseModel):
    url: str


class ResetTokenChangePassword(BaseModel):
    """Prevents extra data in body"""
    model_config = ConfigDict(extra="forbid")

    email: EmailStr = Field(description="Email of employee")
    token: str = Field(description="Reset token")

    password: SecretStr = Field(description="New password ")
