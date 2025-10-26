"""
Station Model
车站表模型
"""
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from app.db.base_class import Base


class Station(Base):
    """Station model - 车站表"""
    __tablename__ = "stations"
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    station_name = Column(String(50), unique=True, nullable=False, comment="车站名称")
    city = Column(String(50), nullable=False, comment="所属城市")
    pinyin = Column(String(50), nullable=False, comment="拼音（用于搜索）")
    short_pinyin = Column(String(10), nullable=False, comment="简拼（用于搜索）")
    
    # Relationships
    departing_trains = relationship("Train", foreign_keys="Train.departure_station_id", back_populates="departure_station")
    arriving_trains = relationship("Train", foreign_keys="Train.arrival_station_id", back_populates="arrival_station")

