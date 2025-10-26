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
    create_time = Column(DateTime(timezone=True), server_default=func.now(), comment="创建时间")
    update_time = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), comment="更新时间")
    
    # Relationships
    passengers = relationship("Passenger", back_populates="user", cascade="all, delete-orphan")
    orders = relationship("Order", back_populates="user", cascade="all, delete-orphan")

