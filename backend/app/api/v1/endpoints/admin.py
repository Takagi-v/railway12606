"""
Admin Endpoints
管理员相关API
"""
from typing import List
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.schemas.user import UserResponse
from app.schemas.role import (
    RoleCreate, RoleUpdate, RoleResponse, 
    PermissionCreate, PermissionUpdate, PermissionResponse,
    UserRoleAssign, UserRoleResponse
)
from app.schemas.common import Response
from app.models.user import User
from app.models.role import Role, Permission
from app.api.deps import get_current_user, require_admin

router = APIRouter()


@router.get("/users", response_model=Response[List[UserResponse]])
async def get_users(
    skip: int = Query(0, ge=0, description="跳过的记录数"),
    limit: int = Query(100, ge=1, le=1000, description="返回的记录数"),
    current_user: User = Depends(require_admin()),
    db: Session = Depends(get_db)
):
    """
    获取用户列表
    
    需要管理员权限
    """
    users = db.query(User).offset(skip).limit(limit).all()
    return Response(
        code=200,
        message="获取用户列表成功",
        data=[UserResponse.model_validate(user) for user in users]
    )


@router.get("/users/{user_id}", response_model=Response[UserResponse])
async def get_user(
    user_id: int,
    current_user: User = Depends(require_admin()),
    db: Session = Depends(get_db)
):
    """
    获取指定用户信息
    
    需要管理员权限
    """
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="用户不存在"
        )
    
    return Response(
        code=200,
        message="获取用户信息成功",
        data=UserResponse.model_validate(user)
    )


@router.post("/roles", response_model=Response[RoleResponse])
async def create_role(
    role_data: RoleCreate,
    current_user: User = Depends(require_admin()),
    db: Session = Depends(get_db)
):
    """
    创建角色
    
    需要管理员权限
    """
    # 检查角色名是否已存在
    if db.query(Role).filter(Role.name == role_data.name).first():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="角色名已存在"
        )
    
    # 创建角色
    new_role = Role(
        name=role_data.name,
        description=role_data.description,
        is_active=role_data.is_active
    )
    
    # 添加权限
    if role_data.permission_ids:
        permissions = db.query(Permission).filter(
            Permission.id.in_(role_data.permission_ids)
        ).all()
        new_role.permissions = permissions
    
    db.add(new_role)
    db.commit()
    db.refresh(new_role)
    
    return Response(
        code=200,
        message="角色创建成功",
        data=RoleResponse.model_validate(new_role)
    )


@router.get("/roles", response_model=Response[List[RoleResponse]])
async def get_roles(
    current_user: User = Depends(require_admin()),
    db: Session = Depends(get_db)
):
    """
    获取角色列表
    
    需要管理员权限
    """
    roles = db.query(Role).all()
    return Response(
        code=200,
        message="获取角色列表成功",
        data=[RoleResponse.model_validate(role) for role in roles]
    )


@router.post("/permissions", response_model=Response[PermissionResponse])
async def create_permission(
    permission_data: PermissionCreate,
    current_user: User = Depends(require_admin()),
    db: Session = Depends(get_db)
):
    """
    创建权限
    
    需要管理员权限
    """
    # 检查权限代码是否已存在
    if db.query(Permission).filter(Permission.code == permission_data.code).first():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="权限代码已存在"
        )
    
    new_permission = Permission(**permission_data.model_dump())
    db.add(new_permission)
    db.commit()
    db.refresh(new_permission)
    
    return Response(
        code=200,
        message="权限创建成功",
        data=PermissionResponse.model_validate(new_permission)
    )


@router.get("/permissions", response_model=Response[List[PermissionResponse]])
async def get_permissions(
    current_user: User = Depends(require_admin()),
    db: Session = Depends(get_db)
):
    """
    获取权限列表
    
    需要管理员权限
    """
    permissions = db.query(Permission).all()
    return Response(
        code=200,
        message="获取权限列表成功",
        data=[PermissionResponse.model_validate(permission) for permission in permissions]
    )


@router.post("/users/{user_id}/roles", response_model=Response[UserRoleResponse])
async def assign_user_roles(
    user_id: int,
    role_assign: UserRoleAssign,
    current_user: User = Depends(require_admin()),
    db: Session = Depends(get_db)
):
    """
    为用户分配角色
    
    需要管理员权限
    """
    # 检查用户是否存在
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="用户不存在"
        )
    
    # 获取角色
    roles = db.query(Role).filter(Role.id.in_(role_assign.role_ids)).all()
    if len(roles) != len(role_assign.role_ids):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="部分角色不存在"
        )
    
    # 分配角色
    user.roles = roles
    db.commit()
    db.refresh(user)
    
    return Response(
        code=200,
        message="角色分配成功",
        data=UserRoleResponse(
            user_id=user.id,
            username=user.username,
            roles=[RoleResponse.model_validate(role) for role in user.roles]
        )
    )


@router.get("/users/{user_id}/roles", response_model=Response[UserRoleResponse])
async def get_user_roles(
    user_id: int,
    current_user: User = Depends(require_admin()),
    db: Session = Depends(get_db)
):
    """
    获取用户角色
    
    需要管理员权限
    """
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="用户不存在"
        )
    
    return Response(
        code=200,
        message="获取用户角色成功",
        data=UserRoleResponse(
            user_id=user.id,
            username=user.username,
            roles=[RoleResponse.model_validate(role) for role in user.roles]
        )
    )