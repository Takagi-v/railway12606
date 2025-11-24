"""
Permission Management API Endpoints
权限管理API端点
"""
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session

from app.api.deps import get_current_active_user
from app.core.permissions import require_permissions, Permissions
from app.db.session import get_db
from app.models.user import User
from app.models.role import Permission
from app.schemas.role import (
    PermissionCreate,
    PermissionUpdate,
    PermissionResponse
)

router = APIRouter()


@router.post("/", response_model=PermissionResponse, status_code=status.HTTP_201_CREATED)
async def create_permission(
    permission_data: PermissionCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_permissions(Permissions.PERMISSION_CREATE))
):
    """
    创建新权限
    
    Args:
        permission_data: 权限创建数据
        db: 数据库会话
        current_user: 当前用户
        
    Returns:
        PermissionResponse: 创建的权限信息
        
    Raises:
        HTTPException: 权限代码已存在时抛出400错误
    """
    # 检查权限代码是否已存在
    existing_permission = db.query(Permission).filter(
        Permission.code == permission_data.code
    ).first()
    
    if existing_permission:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="权限代码已存在"
        )
    
    # 创建新权限
    permission = Permission(
        name=permission_data.name,
        code=permission_data.code,
        description=permission_data.description,
        resource=permission_data.resource,
        action=permission_data.action,
        is_active=permission_data.is_active
    )
    
    db.add(permission)
    db.commit()
    db.refresh(permission)
    
    return permission


@router.get("/", response_model=List[PermissionResponse])
async def get_permissions(
    skip: int = Query(0, ge=0, description="跳过的记录数"),
    limit: int = Query(100, ge=1, le=1000, description="返回的记录数"),
    search: Optional[str] = Query(None, description="搜索关键词"),
    is_active: Optional[int] = Query(None, description="是否激活"),
    db: Session = Depends(get_db),
    current_user: User = Depends(require_permissions(Permissions.PERMISSION_READ))
):
    """
    获取权限列表
    
    Args:
        skip: 跳过的记录数
        limit: 返回的记录数
        search: 搜索关键词
        is_active: 是否激活
        db: 数据库会话
        current_user: 当前用户
        
    Returns:
        List[PermissionResponse]: 权限列表
    """
    query = db.query(Permission)
    
    # 搜索过滤
    if search:
        query = query.filter(
            Permission.name.contains(search) |
            Permission.code.contains(search) |
            Permission.description.contains(search)
        )
    
    # 状态过滤
    if is_active is not None:
        query = query.filter(Permission.is_active == is_active)
    
    # 分页
    permissions = query.offset(skip).limit(limit).all()
    
    return permissions


@router.get("/{permission_id}", response_model=PermissionResponse)
async def get_permission(
    permission_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_permissions(Permissions.PERMISSION_READ))
):
    """
    获取指定权限信息
    
    Args:
        permission_id: 权限ID
        db: 数据库会话
        current_user: 当前用户
        
    Returns:
        PermissionResponse: 权限信息
        
    Raises:
        HTTPException: 权限不存在时抛出404错误
    """
    permission = db.query(Permission).filter(Permission.id == permission_id).first()
    
    if not permission:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="权限不存在"
        )
    
    return permission


@router.put("/{permission_id}", response_model=PermissionResponse)
async def update_permission(
    permission_id: int,
    permission_data: PermissionUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_permissions(Permissions.PERMISSION_UPDATE))
):
    """
    更新权限信息
    
    Args:
        permission_id: 权限ID
        permission_data: 权限更新数据
        db: 数据库会话
        current_user: 当前用户
        
    Returns:
        PermissionResponse: 更新后的权限信息
        
    Raises:
        HTTPException: 权限不存在时抛出404错误
    """
    permission = db.query(Permission).filter(Permission.id == permission_id).first()
    
    if not permission:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="权限不存在"
        )
    
    # 更新权限信息
    update_data = permission_data.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(permission, field, value)
    
    db.commit()
    db.refresh(permission)
    
    return permission


@router.delete("/{permission_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_permission(
    permission_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_permissions(Permissions.PERMISSION_DELETE))
):
    """
    删除权限
    
    Args:
        permission_id: 权限ID
        db: 数据库会话
        current_user: 当前用户
        
    Raises:
        HTTPException: 权限不存在时抛出404错误
    """
    permission = db.query(Permission).filter(Permission.id == permission_id).first()
    
    if not permission:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="权限不存在"
        )
    
    # 检查是否有角色正在使用此权限
    if permission.roles:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="无法删除正在使用的权限，请先从相关角色中移除"
        )
    
    db.delete(permission)
    db.commit()


@router.get("/search/by-resource", response_model=List[PermissionResponse])
async def search_permissions_by_resource(
    resource: str = Query(..., description="资源标识"),
    db: Session = Depends(get_db),
    current_user: User = Depends(require_permissions(Permissions.PERMISSION_READ))
):
    """
    根据资源标识搜索权限
    
    Args:
        resource: 资源标识
        db: 数据库会话
        current_user: 当前用户
        
    Returns:
        List[PermissionResponse]: 权限列表
    """
    permissions = db.query(Permission).filter(
        Permission.resource == resource,
        Permission.is_active == 1
    ).all()
    
    return permissions


@router.get("/search/by-action", response_model=List[PermissionResponse])
async def search_permissions_by_action(
    action: str = Query(..., description="操作类型"),
    db: Session = Depends(get_db),
    current_user: User = Depends(require_permissions(Permissions.PERMISSION_READ))
):
    """
    根据操作类型搜索权限
    
    Args:
        action: 操作类型
        db: 数据库会话
        current_user: 当前用户
        
    Returns:
        List[PermissionResponse]: 权限列表
    """
    permissions = db.query(Permission).filter(
        Permission.action == action,
        Permission.is_active == 1
    ).all()
    
    return permissions