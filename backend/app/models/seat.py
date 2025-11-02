"""
Seat Model
座位表模型
"""
from sqlalchemy import Column, Integer, String, Date, DateTime, ForeignKey, Index, UniqueConstraint, Enum as SAEnum
from sqlalchemy.orm import relationship
from app.db.base_class import Base
from app.models.enums import SeatType, SeatStatus


class Seat(Base):
    """Seat model - 座位表"""
    __tablename__ = "seats"
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    train_id = Column(Integer, ForeignKey("trains.id", ondelete="CASCADE"), nullable=False, comment="车次ID")
    travel_date = Column(Date, nullable=False, comment="乘车日期")
    seat_type = Column(
        SAEnum(SeatType, values_callable=lambda x: [e.value for e in x], name="seat_type_enum"),
        nullable=False,
        comment="座位类型（一等座/二等座/软卧/硬卧）"
    )
    seat_number = Column(String(10), nullable=False, comment="座位号（如1车01A）")
    status = Column(
        SAEnum(SeatStatus, values_callable=lambda x: [e.value for e in x], name="seat_status_enum"),
        nullable=False,
        default="可售",
        comment="状态（可售/已售/已锁定）"
    )
    locked_until = Column(DateTime(timezone=True), nullable=True, comment="锁定截止时间（订单未支付时锁定）")
    
    # Relationships
    train = relationship("Train", back_populates="seats")
    order_passengers = relationship("OrderPassenger", back_populates="seat")
    
    # Composite index for fast availability queries
    __table_args__ = (
        Index('ix_seat_availability', 'train_id', 'travel_date', 'seat_type', 'status'),
        UniqueConstraint('train_id', 'travel_date', 'seat_type', 'seat_number', name='uix_seat_unique'),
    )

