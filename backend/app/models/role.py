"""
Role and Permission Models
角色和权限模型
"""
from sqlalchemy import Column, Integer, String, DateTime, func, ForeignKey, Table
from sqlalchemy.orm import relationship
from app.db.base_class import Base

# 用户角色关联表
user_roles = Table(
    'user_roles',
    Base.metadata,
    Column('user_id', Integer, ForeignKey('users.id'), primary_key=True),
    Column('role_id', Integer, ForeignKey('roles.id'), primary_key=True),
    Column('created_at', DateTime(timezone=True), server_default=func.now())
)

# 角色权限关联表
role_permissions = Table(
    'role_permissions',
    Base.metadata,
    Column('role_id', Integer, ForeignKey('roles.id'), primary_key=True),
    Column('permission_id', Integer, ForeignKey('permissions.id'), primary_key=True),
    Column('created_at', DateTime(timezone=True), server_default=func.now())
)


class Role(Base):
    """Role model - 角色表"""
    __tablename__ = "roles"
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String(50), unique=True, nullable=False, index=True, comment="角色名称")
    description = Column(String(200), nullable=True, comment="角色描述")
    is_active = Column(Integer, default=1, comment="是否激活（1:激活，0:禁用）")
    create_time = Column(DateTime(timezone=True), server_default=func.now(), comment="创建时间")
    update_time = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), comment="更新时间")
    
    # Relationships
    users = relationship("User", secondary=user_roles, back_populates="roles")
    permissions = relationship("Permission", secondary=role_permissions, back_populates="roles")


class Permission(Base):
    """Permission model - 权限表"""
    __tablename__ = "permissions"
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String(50), unique=True, nullable=False, index=True, comment="权限名称")
    code = Column(String(100), unique=True, nullable=False, index=True, comment="权限代码")
    description = Column(String(200), nullable=True, comment="权限描述")
    resource = Column(String(100), nullable=True, comment="资源标识")
    action = Column(String(50), nullable=True, comment="操作类型")
    is_active = Column(Integer, default=1, comment="是否激活（1:激活，0:禁用）")
    create_time = Column(DateTime(timezone=True), server_default=func.now(), comment="创建时间")
    update_time = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), comment="更新时间")
    
    # Relationships
    roles = relationship("Role", secondary=role_permissions, back_populates="permissions")