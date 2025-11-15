"""
API v1 Router
集中管理所有API路由
"""
from fastapi import APIRouter
from app.api.v1.endpoints import auth, users, passengers, trains, orders
from app.api.v1.endpoints import membership, points, beneficiaries, redemptions

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

# 会员相关路由
api_router.include_router(
    membership.router,
    prefix="/members",
    tags=["会员服务"]
)

# 积分相关路由
api_router.include_router(
    points.router,
    prefix="/points",
    tags=["积分账户"]
)

# 受让人管理路由
api_router.include_router(
    beneficiaries.router,
    prefix="/beneficiaries",
    tags=["受让人管理"]
)

# 积分兑换路由
api_router.include_router(
    redemptions.router,
    prefix="/redemptions",
    tags=["积分兑换"]
)

