"""
API v1 Router
集中管理所有API路由
"""
from fastapi import APIRouter
from app.api.v1.endpoints import auth, users, passengers, trains, orders

api_router = APIRouter()

# 认证相关路由
api_router.include_router(
    auth.router,
    prefix="/auth",
    tags=["认证"]
)

# 用户相关路由
api_router.include_router(
    users.router,
    prefix="/user",
    tags=["用户"]
)

# 乘客管理路由
api_router.include_router(
    passengers.router,
    prefix="/passengers",
    tags=["乘客管理"]
)

# 车次查询路由
api_router.include_router(
    trains.router,
    prefix="/trains",
    tags=["车次查询"]
)

# 订单管理路由
api_router.include_router(
    orders.router,
    prefix="/orders",
    tags=["订单管理"]
)

