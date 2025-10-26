"""
Common Schemas
通用的响应模型
"""
from typing import Any, Generic, TypeVar, Optional
from pydantic import BaseModel

T = TypeVar('T')


class Response(BaseModel, Generic[T]):
    """Standard API response"""
    code: int = 200
    message: str = "success"
    data: Optional[T] = None


class ErrorResponse(BaseModel):
    """Error response"""
    code: int
    message: str
    detail: Optional[str] = None

