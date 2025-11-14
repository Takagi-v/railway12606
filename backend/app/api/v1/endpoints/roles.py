"""
Role Management API Endpoints
角色管理API端点
"""
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session

from app.api.deps import get_current_active_user
from app.core.permissions import require_permissions, Permissions
from app.db.session import get_db
from app.models.user import User
from app.models.role import Role, Permission, role_permissions
from app.schemas.role import (
    RoleCreate,
    RoleUpdate,
    RoleResponse,
    PermissionResponse
)

router = APIRouter()


@router.post("/", response_model=RoleResponse, status_code=status.HTTP_201_CREATED)
async def create_role(
    role_data: RoleCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_permissions(Permissions.ROLE_CREATE))
):
    """
    创建新角色
    
    Args:
        role_data: 角色创建数据
        db: 数据库会话
        current_user: 当前用户
        
    Returns:
        RoleResponse: 创建的角色信息
        
    Raises:
        HTTPException: 角色名称已存在时抛出400错误
    """
    # 检查角色名称是否已存在
    existing_role = db.query(Role).filter(Role.name == role_data.name).first()
    
    if existing_role:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="角色名称已存在"
        )
    
    # 创建新角色
    role = Role(
        name=role_data.name,
        description=role_data.description,
        is_active=role_data.is_active
    )
    
    db.add(role)
    db.commit()
    db.refresh(role)
    
    # 分配权限
    if role_data.permission_ids:
        permissions = db.query(Permission).filter(
            Permission.id.in_(role_data.permission_ids)
        ).all()
        role.permissions = permissions
        db.commit()
        db.refresh(role)
    
    return role


@router.get("/", response_model=List[RoleResponse])
async def get_roles(
    skip: int = Query(0, ge=0, description="跳过的记录数"),
    limit: int = Query(100, ge=1, le=1000, description="返回的记录数"),
    search: Optional[str] = Query(None, description="搜索关键词"),
    is_active: Optional[int] = Query(None, description="是否激活"),
    db: Session = Depends(get_db),
    current_user: User = Depends(require_permissions(Permissions.ROLE_READ))
):
    """
    获取角色列表
    
    Args:
        skip: 跳过的记录数
        limit: 返回的记录数
        search: 搜索关键词
        is_active: 是否激活
        db: 数据库会话
        current_user: 当前用户
        
    Returns:
        List[RoleResponse]: 角色列表
    """
    query = db.query(Role)
    
    # 搜索过滤
    if search:
        query = query.filter(
            Role.name.contains(search) |
            Role.description.contains(search)
        )
    
    # 状态过滤
    if is_active is not None:
        query = query.filter(Role.is_active == is_active)
    
    # 分页
    roles = query.offset(skip).limit(limit).all()
    
    return roles


@router.get("/{role_id}", response_model=RoleResponse)
async def get_role(
    role_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_permissions(Permissions.ROLE_READ))
):
    """
    获取指定角色信息
    
    Args:
        role_id: 角色ID
        db: 数据库会话
        current_user: 当前用户
        
    Returns:
        RoleResponse: 角色信息
        
    Raises:
        HTTPException: 角色不存在时抛出404错误
    """
    role = db.query(Role).filter(Role.id == role_id).first()
    
    if not role:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="角色不存在"
        )
    
    return role


@router.put("/{role_id}", response_model=RoleResponse)
async def update_role(
    role_id: int,
    role_data: RoleUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_permissions(Permissions.ROLE_UPDATE))
):
    """
    更新角色信息
    
    Args:
        role_id: 角色ID
        role_data: 角色更新数据
        db: 数据库会话
        current_user: 当前用户
        
    Returns:
        RoleResponse: 更新后的角色信息
        
    Raises:
        HTTPException: 角色不存在时抛出404错误
    """
    role = db.query(Role).filter(Role.id == role_id).first()
    
    if not role:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="角色不存在"
        )
    
    # 更新角色基本信息
    update_data = role_data.dict(exclude_unset=True, exclude={'permission_ids'})
    for field, value in update_data.items():
        setattr(role, field, value)
    
    # 更新权限分配
    if role_data.permission_ids is not None:
        permissions = db.query(Permission).filter(
            Permission.id.in_(role_data.permission_ids)
        ).all()
        role.permissions = permissions
    
    db.commit()
    db.refresh(role)
    
    return role


@router.delete("/{role_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_role(
    role_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_permissions(Permissions.ROLE_DELETE))
):
    """
    删除角色
    
    Args:
        role_id: 角色ID
        db: 数据库会话
        current_user: 当前用户
        
    Raises:
        HTTPException: 角色不存在时抛出404错误
    """
    role = db.query(Role).filter(Role.id == role_id).first()
    
    if not role:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="角色不存在"
        )
    
    # 检查是否有用户正在使用此角色
    if role.users:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="无法删除正在使用的角色，请先从相关用户中移除"
        )
    
    db.delete(role)
    db.commit()


@router.get("/{role_id}/permissions", response_model=List[PermissionResponse])
async def get_role_permissions(
    role_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_permissions(Permissions.ROLE_READ))
):
    """
    获取角色的权限列表
    
    Args:
        role_id: 角色ID
        db: 数据库会话
        current_user: 当前用户
        
    Returns:
        List[PermissionResponse]: 权限列表
        
    Raises:
        HTTPException: 角色不存在时抛出404错误
    """
    role = db.query(Role).filter(Role.id == role_id).first()
    
    if not role:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="角色不存在"
        )
    
    return role.permissions


@router.post("/{role_id}/permissions/{permission_id}", status_code=status.HTTP_201_CREATED)
async def assign_permission_to_role(
    role_id: int,
    permission_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_permissions(Permissions.ROLE_UPDATE))
):
    """
    为角色分配权限
    
    Args:
        role_id: 角色ID
        permission_id: 权限ID
        db: 数据库会话
        current_user: 当前用户
        
    Raises:
        HTTPException: 角色或权限不存在时抛出404错误
    """
    role = db.query(Role).filter(Role.id == role_id).first()
    if not role:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="角色不存在"
        )
    
    permission = db.query(Permission).filter(Permission.id == permission_id).first()
    if not permission:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="权限不存在"
        )
    
    # 检查是否已经分配
    if permission in role.permissions:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="权限已经分配给该角色"
        )
    
    role.permissions.append(permission)
    db.commit()


@router.delete("/{role_id}/permissions/{permission_id}", status_code=status.HTTP_204_NO_CONTENT)
async def remove_permission_from_role(
    role_id: int,
    permission_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_permissions(Permissions.ROLE_UPDATE))
):
    """
    从角色中移除权限
    
    Args:
        role_id: 角色ID
        permission_id: 权限ID
        db: 数据库会话
        current_user: 当前用户
        
    Raises:
        HTTPException: 角色或权限不存在时抛出404错误
    """
    role = db.query(Role).filter(Role.id == role_id).first()
    if not role:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="角色不存在"
        )
    
    permission = db.query(Permission).filter(Permission.id == permission_id).first()
    if not permission:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="权限不存在"
        )
    
    # 检查权限是否已分配
    if permission not in role.permissions:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="该权限未分配给此角色"
        )
    
    role.permissions.remove(permission)
    db.commit()


@router.post("/{role_id}/permissions/batch", status_code=status.HTTP_201_CREATED)
async def batch_assign_permissions_to_role(
    role_id: int,
    permission_ids: List[int],
    db: Session = Depends(get_db),
    current_user: User = Depends(require_permissions(Permissions.ROLE_UPDATE))
):
    """
    批量为角色分配权限
    
    Args:
        role_id: 角色ID
        permission_ids: 权限ID列表
        db: 数据库会话
        current_user: 当前用户
        
    Raises:
        HTTPException: 角色不存在时抛出404错误
    """
    role = db.query(Role).filter(Role.id == role_id).first()
    if not role:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="角色不存在"
        )
    
    permissions = db.query(Permission).filter(
        Permission.id.in_(permission_ids)
    ).all()
    
    # 替换所有权限
    role.permissions = permissions
    db.commit()