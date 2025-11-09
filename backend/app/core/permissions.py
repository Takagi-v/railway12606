"""
Permission verification decorators and middleware
权限验证装饰器和中间件
"""
import logging
from functools import wraps
from typing import List, Union, Callable, Any
from fastapi import Depends, HTTPException, status, Request
from sqlalchemy.orm import Session

from app.api.deps import get_current_active_user
from app.models.user import User
from app.db.session import get_db

# 设置日志
logger = logging.getLogger(__name__)


class PermissionChecker:
    """权限检查器类"""
    
    def __init__(self, permissions: Union[str, List[str]], logic: str = "AND"):
        """
        初始化权限检查器
        
        Args:
            permissions: 权限代码或权限代码列表
            logic: 逻辑操作符，"AND"表示需要所有权限，"OR"表示需要任一权限
        """
        if isinstance(permissions, str):
            self.permissions = [permissions]
        else:
            self.permissions = permissions
        self.logic = logic.upper()
    
    def __call__(self, current_user: User = Depends(get_current_active_user)) -> User:
        """
        检查用户权限
        
        Args:
            current_user: 当前用户
            
        Returns:
            User: 有权限的用户对象
            
        Raises:
            HTTPException: 权限不足时抛出403错误
        """
        if not self.permissions:
            return current_user
        
        # 记录权限验证日志
        logger.info(f"用户 {current_user.username} 尝试访问需要权限: {self.permissions}")
        
        if self.logic == "AND":
            # 需要所有权限
            for permission_code in self.permissions:
                if not current_user.has_permission(permission_code):
                    logger.warning(f"用户 {current_user.username} 缺少权限: {permission_code}")
                    raise HTTPException(
                        status_code=status.HTTP_403_FORBIDDEN,
                        detail=f"缺少权限: {permission_code}"
                    )
        elif self.logic == "OR":
            # 需要任一权限
            has_permission = False
            for permission_code in self.permissions:
                if current_user.has_permission(permission_code):
                    has_permission = True
                    break
            
            if not has_permission:
                logger.warning(f"用户 {current_user.username} 缺少权限: {self.permissions}")
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail=f"缺少以下任一权限: {', '.join(self.permissions)}"
                )
        
        logger.info(f"用户 {current_user.username} 权限验证通过")
        return current_user


def require_permissions(permissions: Union[str, List[str]], logic: str = "AND"):
    """
    权限验证装饰器工厂
    
    Args:
        permissions: 权限代码或权限代码列表
        logic: 逻辑操作符，"AND"表示需要所有权限，"OR"表示需要任一权限
        
    Returns:
        权限检查器实例
    """
    return PermissionChecker(permissions, logic)


class RoleChecker:
    """角色检查器类"""
    
    def __init__(self, roles: Union[str, List[str]], logic: str = "OR"):
        """
        初始化角色检查器
        
        Args:
            roles: 角色名称或角色名称列表
            logic: 逻辑操作符，"AND"表示需要所有角色，"OR"表示需要任一角色
        """
        if isinstance(roles, str):
            self.roles = [roles]
        else:
            self.roles = roles
        self.logic = logic.upper()
    
    def __call__(self, current_user: User = Depends(get_current_active_user)) -> User:
        """
        检查用户角色
        
        Args:
            current_user: 当前用户
            
        Returns:
            User: 有权限的用户对象
            
        Raises:
            HTTPException: 权限不足时抛出403错误
        """
        if not self.roles:
            return current_user
        
        # 记录角色验证日志
        logger.info(f"用户 {current_user.username} 尝试访问需要角色: {self.roles}")
        
        if self.logic == "AND":
            # 需要所有角色
            for role_name in self.roles:
                if not current_user.has_role(role_name):
                    logger.warning(f"用户 {current_user.username} 缺少角色: {role_name}")
                    raise HTTPException(
                        status_code=status.HTTP_403_FORBIDDEN,
                        detail=f"缺少角色: {role_name}"
                    )
        elif self.logic == "OR":
            # 需要任一角色
            has_role = False
            for role_name in self.roles:
                if current_user.has_role(role_name):
                    has_role = True
                    break
            
            if not has_role:
                logger.warning(f"用户 {current_user.username} 缺少角色: {self.roles}")
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail=f"缺少以下任一角色: {', '.join(self.roles)}"
                )
        
        logger.info(f"用户 {current_user.username} 角色验证通过")
        return current_user


def require_roles(roles: Union[str, List[str]], logic: str = "OR"):
    """
    角色验证装饰器工厂
    
    Args:
        roles: 角色名称或角色名称列表
        logic: 逻辑操作符，"AND"表示需要所有角色，"OR"表示需要任一角色
        
    Returns:
        角色检查器实例
    """
    return RoleChecker(roles, logic)


# 预定义的权限检查器
require_admin = require_roles(["admin", "系统管理员"])
require_staff = require_roles(["staff", "工作人员", "admin", "系统管理员"])
require_vip = require_roles(["vip", "VIP用户", "admin", "系统管理员"])
require_user = require_roles(["user", "普通用户", "vip", "VIP用户", "staff", "工作人员", "admin", "系统管理员"])

# 预定义的权限检查器
require_user_manage = require_permissions("user:manage")
require_order_manage = require_permissions("order:manage")
require_ticket_view = require_permissions("ticket:view")
require_ticket_book = require_permissions("ticket:book")
require_ticket_priority = require_permissions("ticket:priority")


def permission_middleware(request: Request, call_next):
    """
    权限验证中间件
    
    Args:
        request: HTTP请求对象
        call_next: 下一个中间件或路由处理器
        
    Returns:
        响应对象
    """
    # 这里可以添加全局权限检查逻辑
    # 例如：检查IP白名单、请求频率限制等
    
    # 记录访问日志
    logger.info(f"访问路径: {request.url.path}, 方法: {request.method}")
    
    # 继续处理请求
    response = call_next(request)
    return response


class PermissionValidator:
    """权限验证器工具类"""
    
    @staticmethod
    def validate_user_permission(user: User, permission_code: str) -> bool:
        """
        验证用户是否具有指定权限
        
        Args:
            user: 用户对象
            permission_code: 权限代码
            
        Returns:
            bool: 是否具有权限
        """
        return user.has_permission(permission_code)
    
    @staticmethod
    def validate_user_role(user: User, role_name: str) -> bool:
        """
        验证用户是否具有指定角色
        
        Args:
            user: 用户对象
            role_name: 角色名称
            
        Returns:
            bool: 是否具有角色
        """
        return user.has_role(role_name)
    
    @staticmethod
    def get_user_permissions(user: User) -> List[str]:
        """
        获取用户所有权限代码
        
        Args:
            user: 用户对象
            
        Returns:
            List[str]: 权限代码列表
        """
        permissions = []
        for role in user.roles:
            if role.is_active:
                for permission in role.permissions:
                    if permission.is_active and permission.code not in permissions:
                        permissions.append(permission.code)
        return permissions
    
    @staticmethod
    def get_user_roles(user: User) -> List[str]:
        """
        获取用户所有角色名称
        
        Args:
            user: 用户对象
            
        Returns:
            List[str]: 角色名称列表
        """
        roles = []
        for role in user.roles:
            if role.is_active and role.name not in roles:
                roles.append(role.name)
        return roles


# 权限常量定义
class Permissions:
    """权限常量类"""
    
    # 用户管理权限
    USER_CREATE = "user:create"
    USER_READ = "user:read"
    USER_UPDATE = "user:update"
    USER_DELETE = "user:delete"
    USER_MANAGE = "user:manage"
    
    # 订单管理权限
    ORDER_CREATE = "order:create"
    ORDER_READ = "order:read"
    ORDER_UPDATE = "order:update"
    ORDER_DELETE = "order:delete"
    ORDER_MANAGE = "order:manage"
    
    # 车票权限
    TICKET_VIEW = "ticket:view"
    TICKET_BOOK = "ticket:book"
    TICKET_CANCEL = "ticket:cancel"
    TICKET_PRIORITY = "ticket:priority"
    
    # 系统管理权限
    SYSTEM_CONFIG = "system:config"
    SYSTEM_LOG = "system:log"
    SYSTEM_MONITOR = "system:monitor"
    
    # 角色权限管理
    ROLE_CREATE = "role:create"
    ROLE_READ = "role:read"
    ROLE_UPDATE = "role:update"
    ROLE_DELETE = "role:delete"
    ROLE_MANAGE = "role:manage"
    
    # 权限管理
    PERMISSION_CREATE = "permission:create"
    PERMISSION_READ = "permission:read"
    PERMISSION_UPDATE = "permission:update"
    PERMISSION_DELETE = "permission:delete"
    PERMISSION_MANAGE = "permission:manage"
    
    # 车次管理权限
    TRAIN_CREATE = "train:create"
    TRAIN_READ = "train:read"
    TRAIN_UPDATE = "train:update"
    TRAIN_DELETE = "train:delete"
    TRAIN_MANAGE = "train:manage"
    
    # 系统管理权限
    SYSTEM_ADMIN = "system:admin"
    SYSTEM_MANAGE = "system:manage"


# 角色常量定义
class Roles:
    """角色常量类"""
    
    ADMIN = "admin"
    STAFF = "staff"
    VIP = "vip"
    USER = "user"
    
    SYSTEM_ADMIN = "系统管理员"
    STAFF_MEMBER = "工作人员"
    VIP_USER = "VIP用户"
    NORMAL_USER = "普通用户"
    
    # 新增角色
    SUPER_ADMIN = "super_admin"
    MANAGER = "manager"
    GUEST = "guest"