"""
Order Models
订单表和订单乘客表模型
"""
from sqlalchemy import Column, Integer, String, Date, DateTime, Numeric, ForeignKey, func, Enum as SAEnum, Index, CheckConstraint
from sqlalchemy.orm import relationship
from app.db.base_class import Base
from app.models.enums import OrderStatus, RefundStatus, SeatType, PassengerType


class Order(Base):
    """Order model - 订单表"""
    __tablename__ = "orders"
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    order_number = Column(String(50), unique=True, nullable=False, index=True, comment="订单号（唯一标识）")
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True, comment="用户ID")
    train_id = Column(Integer, ForeignKey("trains.id"), nullable=False, comment="车次ID")
    travel_date = Column(Date, nullable=False, comment="乘车日期")
    total_price = Column(Numeric(10, 2), nullable=False, comment="订单总价")
    status = Column(
        SAEnum(
            OrderStatus,
            values_callable=lambda x: [e.value for e in x],
            name="order_status_enum",
            validate_strings=True
        ),
        nullable=False,
        comment="订单状态"
    )
    create_time = Column(DateTime(timezone=True), server_default=func.now(), comment="创建时间")
    pay_time = Column(DateTime(timezone=True), nullable=True, comment="支付时间")
    cancel_time = Column(DateTime(timezone=True), nullable=True, comment="取消时间")
    
    # Relationships
    user = relationship("User", back_populates="orders")
    train = relationship("Train", back_populates="orders")
    order_passengers = relationship("OrderPassenger", back_populates="order", cascade="all, delete-orphan")

    __table_args__ = (
        Index('ix_orders_user_status_date', 'user_id', 'status', 'create_time'),
        CheckConstraint('total_price >= 0', name='ck_order_total_price_nonnegative'),
    )


class OrderPassenger(Base):
    """OrderPassenger model - 订单乘客表"""
    __tablename__ = "order_passengers"
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    order_id = Column(Integer, ForeignKey("orders.id", ondelete="CASCADE"), nullable=False, index=True, comment="订单ID")
    passenger_id = Column(Integer, ForeignKey("passengers.id"), nullable=False, comment="乘客ID")
    seat_id = Column(Integer, ForeignKey("seats.id"), nullable=False, comment="座位ID")
    ticket_type = Column(
        SAEnum(
            PassengerType,
            values_callable=lambda x: [e.value for e in x],
            name="passenger_type_enum",
            validate_strings=True
        ),
        nullable=False,
        comment="票种（成人票/学生票/儿童票）"
    )
    seat_type = Column(
        SAEnum(
            SeatType,
            values_callable=lambda x: [e.value for e in x],
            name="seat_type_enum",
            validate_strings=True
        ),
        nullable=False,
        comment="席别（一等座/二等座/软卧/硬卧）"
    )
    price = Column(Numeric(10, 2), nullable=False, comment="票价")
    refund_status = Column(
        SAEnum(
            RefundStatus,
            values_callable=lambda x: [e.value for e in x],
            name="refund_status_enum",
            validate_strings=True
        ),
        default="未退票",
        comment="退票状态（未退票/已退票）"
    )
    refund_time = Column(DateTime(timezone=True), nullable=True, comment="退票时间")
    refund_amount = Column(Numeric(10, 2), nullable=True, comment="退款金额")
    
    # Relationships
    order = relationship("Order", back_populates="order_passengers")
    passenger = relationship("Passenger", back_populates="order_passengers")
    seat = relationship("Seat", back_populates="order_passengers")

    __table_args__ = (
        CheckConstraint('price >= 0', name='ck_order_passenger_price_nonnegative'),
        Index('ix_order_passenger_order', 'order_id'),
    )

