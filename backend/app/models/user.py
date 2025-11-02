"""
User Model
用户表模型
"""
from sqlalchemy import Column, Integer, String, DateTime, func, Enum as SAEnum, UniqueConstraint
from sqlalchemy.orm import relationship
from app.db.base_class import Base
from app.models.enums import IdType, UserType


class User(Base):
    """User model - 用户表"""
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    username = Column(String(30), unique=True, nullable=False, index=True, comment="登录名")
    password = Column(String(255), nullable=False, comment="密码（加密）")
    real_name = Column(String(50), nullable=False, comment="真实姓名")
    id_type = Column(
        SAEnum(IdType, values_callable=lambda x: [e.value for e in x], name="id_type_enum"),
        nullable=False,
        comment="证件类型"
    )
    id_number = Column(String(50), nullable=False, index=True, comment="证件号码")
    phone = Column(String(11), unique=True, nullable=False, index=True, comment="手机号")
    email = Column(String(100), unique=True, nullable=True, comment="邮箱")
    user_type = Column(
        SAEnum(UserType, values_callable=lambda x: [e.value for e in x], name="user_type_enum"),
        nullable=False,
        comment="用户类型（成人/学生）"
    )
    create_time = Column(DateTime(timezone=True), server_default=func.now(), comment="创建时间")
    update_time = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), comment="更新时间")
    
    # Relationships
    passengers = relationship("Passenger", back_populates="user", cascade="all, delete-orphan")
    orders = relationship("Order", back_populates="user", cascade="all, delete-orphan")
    
    # Composite uniqueness: 同类型证件下证件号码唯一
    __table_args__ = (
        UniqueConstraint('id_type', 'id_number', name='uix_user_idtype_idnumber'),
    )

