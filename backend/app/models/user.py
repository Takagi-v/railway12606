"""
User Model
用户表模型
"""
from sqlalchemy import Column, Integer, String, DateTime, func
from sqlalchemy.orm import relationship
from app.db.base_class import Base


class User(Base):
    """User model - 用户表"""
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    username = Column(String(30), unique=True, nullable=False, index=True, comment="登录名")
    password = Column(String(255), nullable=False, comment="密码（加密）")
    real_name = Column(String(50), nullable=False, comment="真实姓名")
    id_type = Column(String(20), nullable=False, comment="证件类型")
    id_number = Column(String(50), unique=True, nullable=False, index=True, comment="证件号码")
    phone = Column(String(11), unique=True, nullable=False, index=True, comment="手机号")
    email = Column(String(100), unique=True, nullable=True, comment="邮箱")
    user_type = Column(String(20), nullable=False, comment="用户类型（成人/学生）")
    is_active = Column(Integer, default=1, comment="是否激活（1:激活，0:禁用）")
    create_time = Column(DateTime(timezone=True), server_default=func.now(), comment="创建时间")
    update_time = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), comment="更新时间")
    
    # Relationships
    passengers = relationship("Passenger", back_populates="user", cascade="all, delete-orphan")
    orders = relationship("Order", back_populates="user", cascade="all, delete-orphan")
    roles = relationship("Role", secondary="user_roles", back_populates="users")
    
    def has_permission(self, permission_code: str) -> bool:
        """检查用户是否具有指定权限"""
        for role in self.roles:
            if role.is_active:
                for permission in role.permissions:
                    if permission.is_active and permission.code == permission_code:
                        return True
        return False
    
    def has_role(self, role_name: str) -> bool:
        """检查用户是否具有指定角色"""
        for role in self.roles:
            if role.is_active and role.name == role_name:
                return True
        return False

