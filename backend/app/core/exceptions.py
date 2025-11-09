"""
Exception Handlers
统一异常处理模块
"""
import logging
from typing import Union
from fastapi import Request, HTTPException, status
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException
from sqlalchemy.exc import SQLAlchemyError
from jose import JWTError

from app.schemas.common import Response as APIResponse

logger = logging.getLogger(__name__)


class BusinessException(Exception):
    """业务异常基类"""
    
    def __init__(self, message: str, code: int = 400):
        self.message = message
        self.code = code
        super().__init__(self.message)


class AuthenticationException(BusinessException):
    """认证异常"""
    
    def __init__(self, message: str = "认证失败"):
        super().__init__(message, 401)


class AuthorizationException(BusinessException):
    """授权异常"""
    
    def __init__(self, message: str = "权限不足"):
        super().__init__(message, 403)


class ValidationException(BusinessException):
    """验证异常"""
    
    def __init__(self, message: str = "数据验证失败"):
        super().__init__(message, 400)


class NotFoundException(BusinessException):
    """资源不存在异常"""
    
    def __init__(self, message: str = "资源不存在"):
        super().__init__(message, 404)


async def http_exception_handler(request: Request, exc: HTTPException) -> JSONResponse:
    """HTTP异常处理器"""
    logger.warning(f"HTTP Exception: {exc.status_code} - {exc.detail}")
    
    return JSONResponse(
        status_code=exc.status_code,
        content=APIResponse(
            code=exc.status_code,
            message=exc.detail,
            data=None
        ).model_dump()
    )


async def starlette_http_exception_handler(request: Request, exc: StarletteHTTPException) -> JSONResponse:
    """Starlette HTTP异常处理器"""
    logger.warning(f"Starlette HTTP Exception: {exc.status_code} - {exc.detail}")
    
    return JSONResponse(
        status_code=exc.status_code,
        content=APIResponse(
            code=exc.status_code,
            message=exc.detail,
            data=None
        ).model_dump()
    )


async def validation_exception_handler(request: Request, exc: RequestValidationError) -> JSONResponse:
    """请求验证异常处理器"""
    logger.warning(f"Validation Error: {exc.errors()}")
    
    # 提取验证错误信息
    error_messages = []
    for error in exc.errors():
        field = " -> ".join(str(loc) for loc in error["loc"])
        message = error["msg"]
        error_messages.append(f"{field}: {message}")
    
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content=APIResponse(
            code=422,
            message="请求数据验证失败: " + "; ".join(error_messages),
            data=None
        ).model_dump()
    )


async def business_exception_handler(request: Request, exc: BusinessException) -> JSONResponse:
    """业务异常处理器"""
    logger.warning(f"Business Exception: {exc.code} - {exc.message}")
    
    return JSONResponse(
        status_code=exc.code,
        content=APIResponse(
            code=exc.code,
            message=exc.message,
            data=None
        ).model_dump()
    )


async def sqlalchemy_exception_handler(request: Request, exc: SQLAlchemyError) -> JSONResponse:
    """SQLAlchemy异常处理器"""
    logger.error(f"Database Error: {str(exc)}")
    
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content=APIResponse(
            code=500,
            message="数据库操作失败",
            data=None
        ).model_dump()
    )


async def jwt_exception_handler(request: Request, exc: JWTError) -> JSONResponse:
    """JWT异常处理器"""
    logger.warning(f"JWT Error: {str(exc)}")
    
    return JSONResponse(
        status_code=status.HTTP_401_UNAUTHORIZED,
        content=APIResponse(
            code=401,
            message="令牌无效或已过期",
            data=None
        ).model_dump(),
        headers={"WWW-Authenticate": "Bearer"}
    )


async def general_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    """通用异常处理器"""
    logger.error(f"Unexpected Error: {type(exc).__name__}: {str(exc)}", exc_info=True)
    
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content=APIResponse(
            code=500,
            message="服务器内部错误",
            data=None
        ).model_dump()
    )