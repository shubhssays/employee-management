from pydantic import BaseModel, ConfigDict, EmailStr, SecretStr


class AdminLogin(BaseModel):
    """Prevents extra data in body"""
    model_config = ConfigDict(extra="forbid")

    email: str = EmailStr
    password: str = SecretStr


class AdminLoginResponse(BaseModel):
    # Without this, we would have to manually map every field.
    model_config = {"from_attributes": True}

    id: int
    email: str
    name: str
    token: str
