"""
Order Models
订单表和订单乘客表模型
"""
from sqlalchemy import Column, Integer, String, Date, DateTime, Numeric, ForeignKey, func
from sqlalchemy.orm import relationship
from app.db.base_class import Base


class Order(Base):
    """Order model - 订单表"""
    __tablename__ = "orders"
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    order_number = Column(String(50), unique=True, nullable=False, index=True, comment="订单号（唯一标识）")
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True, comment="用户ID")
    train_id = Column(Integer, ForeignKey("trains.id"), nullable=False, comment="车次ID")
    travel_date = Column(Date, nullable=False, comment="乘车日期")
    total_price = Column(Numeric(10, 2), nullable=False, comment="订单总价")
    status = Column(String(20), nullable=False, comment="订单状态")
    create_time = Column(DateTime(timezone=True), server_default=func.now(), comment="创建时间")
    pay_time = Column(DateTime(timezone=True), nullable=True, comment="支付时间")
    cancel_time = Column(DateTime(timezone=True), nullable=True, comment="取消时间")
    
    # Relationships
    user = relationship("User", back_populates="orders")
    train = relationship("Train", back_populates="orders")
    order_passengers = relationship("OrderPassenger", back_populates="order", cascade="all, delete-orphan")


class OrderPassenger(Base):
    """OrderPassenger model - 订单乘客表"""
    __tablename__ = "order_passengers"
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    order_id = Column(Integer, ForeignKey("orders.id", ondelete="CASCADE"), nullable=False, index=True, comment="订单ID")
    passenger_id = Column(Integer, ForeignKey("passengers.id"), nullable=False, comment="乘客ID")
    seat_id = Column(Integer, ForeignKey("seats.id"), nullable=False, comment="座位ID")
    ticket_type = Column(String(20), nullable=False, comment="票种（成人票/学生票/儿童票）")
    seat_type = Column(String(20), nullable=False, comment="席别（一等座/二等座/软卧/硬卧）")
    price = Column(Numeric(10, 2), nullable=False, comment="票价")
    refund_status = Column(String(20), default="未退票", comment="退票状态（未退票/已退票）")
    refund_time = Column(DateTime(timezone=True), nullable=True, comment="退票时间")
    refund_amount = Column(Numeric(10, 2), nullable=True, comment="退款金额")
    
    # Relationships
    order = relationship("Order", back_populates="order_passengers")
    passenger = relationship("Passenger", back_populates="order_passengers")
    seat = relationship("Seat", back_populates="order_passengers")

