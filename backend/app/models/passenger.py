"""
Passenger Model
乘客表模型
"""
from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, func, UniqueConstraint, Enum as SAEnum
from sqlalchemy.orm import relationship
from app.db.base_class import Base
from app.models.enums import IdType, PassengerType


class Passenger(Base):
    """Passenger model - 乘客表"""
    __tablename__ = "passengers"
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True, comment="关联用户ID")
    name = Column(String(50), nullable=False, comment="姓名")
    id_type = Column(
        SAEnum(
            IdType,
            values_callable=lambda x: [e.value for e in x],
            name="id_type_enum",
            validate_strings=True
        ),
        nullable=False,
        comment="证件类型"
    )
    id_number = Column(String(50), nullable=False, comment="证件号码")
    phone = Column(String(11), nullable=False, comment="手机号")
    passenger_type = Column(
        SAEnum(
            PassengerType,
            values_callable=lambda x: [e.value for e in x],
            name="passenger_type_enum",
            validate_strings=True
        ),
        nullable=False,
        comment="旅客类型（成人/学生/儿童）"
    )
    verified = Column(Boolean, default=False, comment="是否已验证")
    create_time = Column(DateTime(timezone=True), server_default=func.now(), comment="创建时间")
    
    # Relationships
    user = relationship("User", back_populates="passengers")
    order_passengers = relationship("OrderPassenger", back_populates="passenger")
    
    # Constraints: 同一用户不能添加重复证件号的乘客
    __table_args__ = (
        UniqueConstraint('user_id', 'id_type', 'id_number', name='uix_user_passenger'),
    )

