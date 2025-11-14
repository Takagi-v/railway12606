"""
Role and Permission Schemas
角色和权限的Pydantic模型
"""
from typing import List, Optional
from pydantic import BaseModel, Field
from datetime import datetime


class PermissionBase(BaseModel):
    """权限基础模型"""
    name: str = Field(..., description="权限名称")
    code: str = Field(..., description="权限代码")
    description: Optional[str] = Field(None, description="权限描述")
    resource: Optional[str] = Field(None, description="资源标识")
    action: Optional[str] = Field(None, description="操作类型")
    is_active: int = Field(1, description="是否激活")


class PermissionCreate(PermissionBase):
    """创建权限模型"""
    pass


class PermissionUpdate(BaseModel):
    """更新权限模型"""
    name: Optional[str] = Field(None, description="权限名称")
    description: Optional[str] = Field(None, description="权限描述")
    resource: Optional[str] = Field(None, description="资源标识")
    action: Optional[str] = Field(None, description="操作类型")
    is_active: Optional[int] = Field(None, description="是否激活")


class PermissionResponse(PermissionBase):
    """权限响应模型"""
    id: int
    create_time: datetime
    update_time: datetime
    
    class Config:
        from_attributes = True


class RoleBase(BaseModel):
    """角色基础模型"""
    name: str = Field(..., description="角色名称")
    description: Optional[str] = Field(None, description="角色描述")
    is_active: int = Field(1, description="是否激活")


class RoleCreate(RoleBase):
    """创建角色模型"""
    permission_ids: Optional[List[int]] = Field([], description="权限ID列表")


class RoleUpdate(BaseModel):
    """更新角色模型"""
    name: Optional[str] = Field(None, description="角色名称")
    description: Optional[str] = Field(None, description="角色描述")
    is_active: Optional[int] = Field(None, description="是否激活")
    permission_ids: Optional[List[int]] = Field(None, description="权限ID列表")


class RoleResponse(RoleBase):
    """角色响应模型"""
    id: int
    create_time: datetime
    update_time: datetime
    permissions: List[PermissionResponse] = []
    
    class Config:
        from_attributes = True


class UserRoleAssign(BaseModel):
    """用户角色分配模型"""
    user_id: int = Field(..., description="用户ID")
    role_ids: List[int] = Field(..., description="角色ID列表")


class UserPermissionCheck(BaseModel):
    """用户权限检查模型"""
    user_id: int = Field(..., description="用户ID")
    permission_code: str = Field(..., description="权限代码")


class UserRoleResponse(BaseModel):
    """用户角色响应模型"""
    user_id: int
    username: str
    roles: List[RoleResponse] = []
    
    class Config:
        from_attributes = True