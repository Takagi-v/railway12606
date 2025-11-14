"""
User Role Assignment API Endpoints
用户角色分配API端点
"""
from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api.deps import get_current_active_user
from app.core.permissions import require_permissions, Permissions, PermissionValidator
from app.db.session import get_db
from app.models.user import User
from app.models.role import Role
from app.schemas.role import (
    UserRoleAssign,
    UserRoleResponse,
    UserPermissionCheck,
    RoleResponse,
    PermissionResponse
)

router = APIRouter()


@router.get("/{user_id}/roles", response_model=UserRoleResponse)
async def get_user_roles(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """
    获取用户的角色列表
    
    Args:
        user_id: 用户ID
        db: 数据库会话
        current_user: 当前用户
        
    Returns:
        UserRoleResponse: 用户角色信息
        
    Raises:
        HTTPException: 用户不存在时抛出404错误
    """
    user = db.query(User).filter(User.id == user_id).first()
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="用户不存在"
        )
    
    # 仅允许访问自己的角色，除非具有用户查看权限
    if user.id != current_user.id:
        if Permissions.USER_READ not in PermissionValidator.get_user_permissions(current_user):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="权限不足"
            )

    return UserRoleResponse(
        user_id=user.id,
        username=user.username,
        roles=user.roles
    )


@router.post("/{user_id}/roles", status_code=status.HTTP_201_CREATED)
async def assign_roles_to_user(
    user_id: int,
    role_ids: List[int],
    db: Session = Depends(get_db),
    current_user: User = Depends(require_permissions(Permissions.USER_MANAGE))
):
    """
    为用户分配角色
    
    Args:
        user_id: 用户ID
        role_ids: 角色ID列表
        db: 数据库会话
        current_user: 当前用户
        
    Raises:
        HTTPException: 用户不存在时抛出404错误
    """
    user = db.query(User).filter(User.id == user_id).first()
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="用户不存在"
        )
    
    # 获取有效的角色
    roles = db.query(Role).filter(
        Role.id.in_(role_ids),
        Role.is_active == 1
    ).all()
    
    if len(roles) != len(role_ids):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="部分角色不存在或已禁用"
        )
    
    # 替换用户的所有角色
    user.roles = roles
    db.commit()


@router.post("/{user_id}/roles/{role_id}", status_code=status.HTTP_201_CREATED)
async def assign_single_role_to_user(
    user_id: int,
    role_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_permissions(Permissions.USER_MANAGE))
):
    """
    为用户分配单个角色
    
    Args:
        user_id: 用户ID
        role_id: 角色ID
        db: 数据库会话
        current_user: 当前用户
        
    Raises:
        HTTPException: 用户或角色不存在时抛出404错误
    """
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="用户不存在"
        )
    
    role = db.query(Role).filter(Role.id == role_id, Role.is_active == 1).first()
    if not role:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="角色不存在或已禁用"
        )
    
    # 检查是否已经分配
    if role in user.roles:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="用户已经拥有该角色"
        )
    
    user.roles.append(role)
    db.commit()


@router.delete("/{user_id}/roles/{role_id}", status_code=status.HTTP_204_NO_CONTENT)
async def remove_role_from_user(
    user_id: int,
    role_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_permissions(Permissions.USER_MANAGE))
):
    """
    从用户中移除角色
    
    Args:
        user_id: 用户ID
        role_id: 角色ID
        db: 数据库会话
        current_user: 当前用户
        
    Raises:
        HTTPException: 用户或角色不存在时抛出404错误
    """
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="用户不存在"
        )
    
    role = db.query(Role).filter(Role.id == role_id).first()
    if not role:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="角色不存在"
        )
    
    # 检查角色是否已分配
    if role not in user.roles:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="用户未拥有该角色"
        )
    
    user.roles.remove(role)
    db.commit()


@router.get("/{user_id}/permissions")
async def get_user_permissions(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """
    获取用户的所有权限
    
    Args:
        user_id: 用户ID
        db: 数据库会话
        current_user: 当前用户
        
    Returns:
        dict: 用户权限信息
        
    Raises:
        HTTPException: 用户不存在时抛出404错误
    """
    user = db.query(User).filter(User.id == user_id).first()
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="用户不存在"
        )
    
    # 仅允许访问自己的权限，除非具有用户查看权限
    if user.id != current_user.id:
        if Permissions.USER_READ not in PermissionValidator.get_user_permissions(current_user):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="权限不足"
            )

    # 返回完整的角色对象和权限对象
    # 去重权限
    seen_perm_ids = set()
    permission_objs = []
    for role in user.roles:
        for perm in role.permissions:
            if perm.is_active == 1 and perm.id not in seen_perm_ids:
                seen_perm_ids.add(perm.id)
                permission_objs.append(PermissionResponse.model_validate(perm))

    role_objs = [RoleResponse.model_validate(r) for r in user.roles]

    return {
        "user_id": user.id,
        "username": user.username,
        "roles": role_objs,
        "permissions": permission_objs
    }


@router.post("/{user_id}/permissions/check")
async def check_user_permission(
    user_id: int,
    request: UserPermissionCheck,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """
    检查用户是否具有指定权限
    
    Args:
        user_id: 用户ID
        request: 权限检查请求
        db: 数据库会话
        current_user: 当前用户
        
    Returns:
        dict: 权限检查结果
        
    Raises:
        HTTPException: 用户不存在时抛出404错误
    """
    user = db.query(User).filter(User.id == user_id).first()
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="用户不存在"
        )
    
    # 允许自查，否则需要查看用户权限的权限
    if user.id != current_user.id:
        if Permissions.USER_READ not in PermissionValidator.get_user_permissions(current_user):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="权限不足"
            )

    has_permission = PermissionValidator.validate_user_permission(user, request.permission_code)
    
    return {
        "user_id": user.id,
        "username": user.username,
        "permission_code": request.permission_code,
        "has_permission": has_permission
    }


@router.post("/{user_id}/roles/check")
async def check_user_role(
    user_id: int,
    role_name: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """
    检查用户是否具有指定角色
    
    Args:
        user_id: 用户ID
        role_name: 角色名称
        db: 数据库会话
        current_user: 当前用户
        
    Returns:
        dict: 角色检查结果
        
    Raises:
        HTTPException: 用户不存在时抛出404错误
    """
    user = db.query(User).filter(User.id == user_id).first()
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="用户不存在"
        )
    
    # 允许自查，否则需要查看用户权限的权限
    if user.id != current_user.id:
        if Permissions.USER_READ not in PermissionValidator.get_user_permissions(current_user):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="权限不足"
            )

    has_role = PermissionValidator.validate_user_role(user, role_name)
    
    return {
        "user_id": user.id,
        "username": user.username,
        "role_name": role_name,
        "has_role": has_role
    }


@router.get("/", response_model=List[UserRoleResponse])
async def get_all_users_roles(
    db: Session = Depends(get_db),
    current_user: User = Depends(require_permissions(Permissions.USER_READ))
):
    """
    获取所有用户的角色信息
    
    Args:
        db: 数据库会话
        current_user: 当前用户
        
    Returns:
        List[UserRoleResponse]: 用户角色信息列表
    """
    users = db.query(User).filter(User.is_active == 1).all()
    
    return [
        UserRoleResponse(
            user_id=user.id,
            username=user.username,
            roles=user.roles
        )
        for user in users
    ]


@router.get("/roles/{role_id}/users")
async def get_role_users(
    role_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_permissions(Permissions.ROLE_READ))
):
    """
    获取拥有指定角色的用户列表
    
    Args:
        role_id: 角色ID
        db: 数据库会话
        current_user: 当前用户
        
    Returns:
        dict: 角色和用户信息
        
    Raises:
        HTTPException: 角色不存在时抛出404错误
    """
    role = db.query(Role).filter(Role.id == role_id).first()
    
    if not role:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="角色不存在"
        )
    
    users = [
        {
            "id": user.id,
            "username": user.username,
            "real_name": user.real_name,
            "is_active": user.is_active
        }
        for user in role.users
    ]
    
    return {
        "role_id": role.id,
        "role_name": role.name,
        "role_description": role.description,
        "users": users,
        "user_count": len(users)
    }