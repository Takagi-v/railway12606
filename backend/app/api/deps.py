"""
Authentication Dependencies
认证依赖模块，提供用户认证和权限验证的依赖函数
"""
from typing import Optional, List
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from jose import JWTError, jwt

from app.core.config import settings
from app.core.security import decode_token
from app.db.session import get_db
from app.models.user import User

# JWT Bearer token
security = HTTPBearer()


async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
) -> User:
    """
    获取当前认证用户
    
    Args:
        credentials: JWT Bearer token
        db: 数据库会话
        
    Returns:
        User: 当前用户对象
        
    Raises:
        HTTPException: 认证失败时抛出401错误
    """
    try:
        token = credentials.credentials
        payload = decode_token(token)
        user_id_str: str = payload.get("sub")
        
        if user_id_str is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="无效的认证凭据",
                headers={"WWW-Authenticate": "Bearer"},
            )
        
        try:
            user_id = int(user_id_str)
        except (ValueError, TypeError):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="无效的用户ID",
                headers={"WWW-Authenticate": "Bearer"},
            )
        
        user = db.query(User).filter(User.id == user_id).first()
        if user is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="用户不存在",
                headers={"WWW-Authenticate": "Bearer"},
            )
        
        return user
        
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="无效的认证凭据",
            headers={"WWW-Authenticate": "Bearer"},
        )


async def get_current_active_user(
    current_user: User = Depends(get_current_user)
) -> User:
    """
    获取当前活跃用户
    
    Args:
        current_user: 当前用户
        
    Returns:
        User: 活跃用户对象
        
    Raises:
        HTTPException: 用户被禁用时抛出400错误
    """
    # 这里可以添加用户状态检查逻辑
    # 例如检查用户是否被禁用、是否需要验证邮箱等
    return current_user


async def get_optional_current_user(
    credentials: Optional[HTTPAuthorizationCredentials] = Depends(security),
    db: Session = Depends(get_db)
) -> Optional[User]:
    """
    获取可选的当前用户（允许匿名访问）
    
    Args:
        credentials: 可选的JWT Bearer token
        db: 数据库会话
        
    Returns:
        Optional[User]: 用户对象或None
    """
    if not credentials:
        return None
    
    try:
        token = credentials.credentials
        payload = decode_token(token)
        user_id: int = payload.get("sub")
        
        if user_id is None:
            return None
        
        user = db.query(User).filter(User.id == user_id).first()
        return user
        
    except JWTError:
        return None


def require_roles(allowed_roles: List[str]):
    """
    角色权限装饰器工厂
    
    Args:
        allowed_roles: 允许的角色列表
        
    Returns:
        依赖函数
    """
    async def role_checker(
        current_user: User = Depends(get_current_active_user)
    ) -> User:
        """
        检查用户角色权限
        
        Args:
            current_user: 当前用户
            
        Returns:
            User: 有权限的用户对象
            
        Raises:
            HTTPException: 权限不足时抛出403错误
        """
        # 检查用户是否具有任一允许的角色
        has_role = False
        for role_name in allowed_roles:
            if current_user.has_role(role_name):
                has_role = True
                break
        
        # 如果没有角色系统，回退到user_type检查
        if not has_role and current_user.user_type in allowed_roles:
            has_role = True
        
        if not has_role:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="权限不足"
            )
        
        return current_user
    
    return role_checker


def require_permissions(required_permissions: List[str]):
    """
    权限检查装饰器工厂
    
    Args:
        required_permissions: 需要的权限代码列表
        
    Returns:
        依赖函数
    """
    async def permission_checker(
        current_user: User = Depends(get_current_active_user)
    ) -> User:
        """
        检查用户权限
        
        Args:
            current_user: 当前用户
            
        Returns:
            User: 有权限的用户对象
            
        Raises:
            HTTPException: 权限不足时抛出403错误
        """
        # 检查用户是否具有所有必需的权限
        for permission_code in required_permissions:
            if not current_user.has_permission(permission_code):
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail=f"缺少权限: {permission_code}"
                )
        
        return current_user
    
    return permission_checker


def require_admin():
    """
    要求管理员权限的依赖
    
    Returns:
        依赖函数
    """
    return require_roles(["admin", "管理员", "super_admin"])


def require_user():
    """
    要求普通用户权限的依赖
    
    Returns:
        依赖函数
    """
    return require_roles(["user", "admin", "成人", "学生", "管理员"])


async def validate_token(
    credentials: HTTPAuthorizationCredentials = Depends(security)
) -> dict:
    """
    验证JWT令牌
    
    Args:
        credentials: JWT Bearer token
        
    Returns:
        dict: 令牌载荷
        
    Raises:
        HTTPException: 令牌无效时抛出401错误
    """
    try:
        token = credentials.credentials
        payload = decode_token(token)
        return payload
        
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="无效的令牌",
            headers={"WWW-Authenticate": "Bearer"},
        )


async def get_user_by_id(
    user_id: int,
    db: Session = Depends(get_db)
) -> Optional[User]:
    """
    根据用户ID获取用户
    
    Args:
        user_id: 用户ID
        db: 数据库会话
        
    Returns:
        Optional[User]: 用户对象或None
    """
    return db.query(User).filter(User.id == user_id).first()