from typing import TypeVar, Generic

from pydantic import BaseModel

T = TypeVar("T")


class SuccessResponse(BaseModel, Generic[T]):
    """Standard API success response envelope."""
    success: bool = True
    data: T
    message: str = "Success"
