"""
API v1 Router
集中管理所有API路由
"""
from fastapi import APIRouter
from app.api.v1.endpoints import auth, users, passengers, trains, orders, admin, permissions, roles, user_roles, password_recovery

api_router = APIRouter()

# 认证相关路由
api_router.include_router(
    auth.router,
    prefix="/auth",
    tags=["认证"]
)

# 找回密码路由
api_router.include_router(
    password_recovery.router,
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

# 管理员路由
api_router.include_router(
    admin.router,
    prefix="/admin",
    tags=["管理员"]
)

# 权限管理路由
api_router.include_router(
    permissions.router,
    prefix="/permissions",
    tags=["权限管理"]
)

# 角色管理路由
api_router.include_router(
    roles.router,
    prefix="/roles",
    tags=["角色管理"]
)

# 用户角色分配路由
api_router.include_router(
    user_roles.router,
    prefix="/user-roles",
    tags=["用户角色分配"]
)

