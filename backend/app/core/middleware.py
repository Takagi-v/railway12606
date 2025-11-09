"""
Security Middleware
安全中间件模块
"""
import time
import logging
from typing import Callable
from fastapi import Request, Response, HTTPException
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.types import ASGIApp

from app.schemas.common import Response as APIResponse

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class SecurityMiddleware(BaseHTTPMiddleware):
    """安全中间件"""
    
    def __init__(self, app: ASGIApp):
        super().__init__(app)
    
    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        """处理请求"""
        start_time = time.time()
        
        # 记录请求信息
        logger.info(
            f"Request: {request.method} {request.url.path} "
            f"from {request.client.host if request.client else 'unknown'}"
        )
        
        try:
            # 处理请求
            response = await call_next(request)
            
            # 添加安全头
            response.headers["X-Content-Type-Options"] = "nosniff"
            response.headers["X-Frame-Options"] = "DENY"
            response.headers["X-XSS-Protection"] = "1; mode=block"
            response.headers["Strict-Transport-Security"] = "max-age=31536000; includeSubDomains"
            
            # 记录响应时间
            process_time = time.time() - start_time
            response.headers["X-Process-Time"] = str(process_time)
            
            logger.info(
                f"Response: {response.status_code} "
                f"in {process_time:.4f}s"
            )
            
            return response
            
        except Exception as e:
            # 记录错误
            process_time = time.time() - start_time
            logger.error(
                f"Error processing request {request.method} {request.url.path}: "
                f"{str(e)} in {process_time:.4f}s"
            )
            
            # 返回统一错误响应
            return JSONResponse(
                status_code=500,
                content=APIResponse(
                    code=500,
                    message="服务器内部错误",
                    data=None
                ).model_dump()
            )


class RateLimitMiddleware(BaseHTTPMiddleware):
    """简单的速率限制中间件"""
    
    def __init__(self, app: ASGIApp, max_requests: int = 100, window_seconds: int = 60):
        super().__init__(app)
        self.max_requests = max_requests
        self.window_seconds = window_seconds
        self.requests = {}  # 简单的内存存储，生产环境应使用Redis
    
    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        """处理请求"""
        client_ip = request.client.host if request.client else "unknown"
        current_time = time.time()
        
        # 清理过期记录
        self.cleanup_expired_requests(current_time)
        
        # 检查速率限制
        if client_ip in self.requests:
            request_times = self.requests[client_ip]
            if len(request_times) >= self.max_requests:
                return JSONResponse(
                    status_code=429,
                    content=APIResponse(
                        code=429,
                        message="请求过于频繁，请稍后再试",
                        data=None
                    ).model_dump()
                )
        
        # 记录请求时间
        if client_ip not in self.requests:
            self.requests[client_ip] = []
        self.requests[client_ip].append(current_time)
        
        return await call_next(request)
    
    def cleanup_expired_requests(self, current_time: float):
        """清理过期的请求记录"""
        cutoff_time = current_time - self.window_seconds
        for client_ip in list(self.requests.keys()):
            self.requests[client_ip] = [
                req_time for req_time in self.requests[client_ip]
                if req_time > cutoff_time
            ]
            if not self.requests[client_ip]:
                del self.requests[client_ip]


class RequestValidationMiddleware(BaseHTTPMiddleware):
    """请求验证中间件"""
    
    def __init__(self, app: ASGIApp):
        super().__init__(app)
    
    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        """处理请求"""
        # 检查请求大小
        content_length = request.headers.get("content-length")
        if content_length and int(content_length) > 10 * 1024 * 1024:  # 10MB限制
            return JSONResponse(
                status_code=413,
                content=APIResponse(
                    code=413,
                    message="请求体过大",
                    data=None
                ).model_dump()
            )
        
        # 检查Content-Type（对于POST/PUT请求）
        if request.method in ["POST", "PUT", "PATCH"]:
            content_type = request.headers.get("content-type", "")
            if not content_type.startswith(("application/json", "multipart/form-data")):
                # 允许某些特殊路径
                if not request.url.path.startswith("/docs") and not request.url.path.startswith("/openapi"):
                    return JSONResponse(
                        status_code=415,
                        content=APIResponse(
                            code=415,
                            message="不支持的媒体类型",
                            data=None
                        ).model_dump()
                    )
        
        return await call_next(request)