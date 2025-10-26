"""
Train Model
车次表模型
"""
from sqlalchemy import Column, Integer, String, Time, Numeric, ForeignKey
from sqlalchemy.orm import relationship
from app.db.base_class import Base


class Train(Base):
    """Train model - 车次表"""
    __tablename__ = "trains"
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    train_number = Column(String(10), unique=True, nullable=False, index=True, comment="车次号（如G1234）")
    train_type = Column(String(10), nullable=False, comment="车次类型（高铁/动车/直达）")
    departure_station_id = Column(Integer, ForeignKey("stations.id"), nullable=False, comment="出发站ID")
    arrival_station_id = Column(Integer, ForeignKey("stations.id"), nullable=False, comment="到达站ID")
    departure_time = Column(Time, nullable=False, comment="出发时间")
    arrival_time = Column(Time, nullable=False, comment="到达时间")
    duration_minutes = Column(Integer, nullable=False, comment="历时（分钟）")
    
    # Seat counts
    first_class_seats = Column(Integer, default=0, comment="一等座总数")
    second_class_seats = Column(Integer, default=0, comment="二等座总数")
    soft_sleeper_seats = Column(Integer, default=0, comment="软卧总数")
    hard_sleeper_seats = Column(Integer, default=0, comment="硬卧总数")
    
    # Prices
    first_class_price = Column(Numeric(10, 2), default=0, comment="一等座票价")
    second_class_price = Column(Numeric(10, 2), default=0, comment="二等座票价")
    soft_sleeper_price = Column(Numeric(10, 2), default=0, comment="软卧票价")
    hard_sleeper_price = Column(Numeric(10, 2), default=0, comment="硬卧票价")
    
    # Relationships
    departure_station = relationship("Station", foreign_keys=[departure_station_id], back_populates="departing_trains")
    arrival_station = relationship("Station", foreign_keys=[arrival_station_id], back_populates="arriving_trains")
    seats = relationship("Seat", back_populates="train", cascade="all, delete-orphan")
    orders = relationship("Order", back_populates="train")

