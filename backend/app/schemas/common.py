"""
Common Schemas
通用的响应模型
"""
from typing import Any, Generic, TypeVar, Optional
from pydantic import BaseModel, Field

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


class PageInfo(BaseModel):
    """分页信息"""
    page: int = Field(description="当前页码", ge=1)
    size: int = Field(description="每页大小", ge=1, le=100)
    total: int = Field(description="总记录数", ge=0)
    pages: int = Field(description="总页数", ge=0)


class PagedResponse(BaseModel, Generic[T]):
    """分页响应格式"""
    code: int = Field(default=200, description="响应状态码")
    message: str = Field(default="success", description="响应消息")
    data: Optional[list[T]] = Field(default=None, description="响应数据列表")
    page_info: Optional[PageInfo] = Field(default=None, description="分页信息")


class TokenResponse(BaseModel):
    """令牌响应"""
    access_token: str = Field(description="访问令牌")
    token_type: str = Field(default="bearer", description="令牌类型")
    expires_in: int = Field(description="过期时间（秒）")


class MessageResponse(BaseModel):
    """消息响应"""
    message: str = Field(description="消息内容")

