"""
Order Schemas
订单相关的Pydantic模型
"""
from datetime import datetime, date
from typing import List, Optional
from decimal import Decimal
from pydantic import BaseModel, Field, validator
from app.core.exceptions import ValidationException


class OrderPassengerCreate(BaseModel):
    """Order passenger create schema"""
    passenger_id: int = Field(..., gt=0, description="乘客ID必须大于0")
    ticket_type: str = Field(..., min_length=1, max_length=20, description="票种类型")
    seat_type: str = Field(..., min_length=1, max_length=20, description="座位类型")
    
    @validator('ticket_type')
    def validate_ticket_type(cls, v):
        """验证票种类型"""
        valid_types = ['成人票', '学生票', '儿童票']
        if v not in valid_types:
            raise ValidationException(f"票种类型必须是: {', '.join(valid_types)}")
        return v
    
    @validator('seat_type')
    def validate_seat_type(cls, v):
        """验证座位类型"""
        valid_types = ['一等座', '二等座', '商务座', '软卧', '硬卧', '硬座']
        if v not in valid_types:
            raise ValidationException(f"座位类型必须是: {', '.join(valid_types)}")
        return v


class OrderCreate(BaseModel):
    """Create order schema"""
    train_id: int = Field(..., gt=0, description="车次ID必须大于0")
    travel_date: date = Field(..., description="乘车日期")
    passengers: List[OrderPassengerCreate] = Field(..., min_items=1, max_items=6, description="乘客列表，最多6人")
    
    @validator('travel_date')
    def validate_travel_date(cls, v):
        """验证乘车日期"""
        from datetime import date, timedelta
        today = date.today()
        max_date = today + timedelta(days=30)  # 最多提前30天购票
        
        if v < today:
            raise ValidationException("乘车日期不能早于今天")
        if v > max_date:
            raise ValidationException("最多只能提前30天购票")
        return v
    
    @validator('passengers')
    def validate_passengers(cls, v):
        """验证乘客列表"""
        if not v:
            raise ValidationException("至少需要一名乘客")
        
        # 检查乘客ID是否重复
        passenger_ids = [p.passenger_id for p in v]
        if len(passenger_ids) != len(set(passenger_ids)):
            raise ValidationException("乘客ID不能重复")
        
        return v


class OrderPassengerResponse(BaseModel):
    """Order passenger response"""
    name: str
    id_number: str
    seat_type: str
    seat_number: Optional[str]
    ticket_type: str
    price: Decimal
    refund_status: str
    
    class Config:
        from_attributes = True


class OrderResponse(BaseModel):
    """Order response schema"""
    id: int
    order_number: str
    train_number: str
    departure_station: str
    arrival_station: str
    travel_date: date
    departure_time: str
    total_price: Decimal
    status: str
    passenger_count: int
    create_time: datetime
    
    class Config:
        from_attributes = True


class OrderDetailResponse(BaseModel):
    """Order detail response"""
    id: int
    order_number: str
    train_number: str
    departure_station: str
    arrival_station: str
    departure_time: str
    arrival_time: str
    travel_date: date
    passengers: List[OrderPassengerResponse]
    total_price: Decimal
    status: str
    create_time: datetime
    pay_time: Optional[datetime]
    cancel_time: Optional[datetime]
    
    class Config:
        from_attributes = True


class RefundRequest(BaseModel):
    """Refund request schema"""
    passenger_ids: List[int] = Field(default=[], description="要退票的乘客ID列表，空列表表示全部退票")
    
    @validator('passenger_ids')
    def validate_passenger_ids(cls, v):
        """验证乘客ID列表"""
        if v is None:
            return []
        
        # 检查ID是否都大于0
        for passenger_id in v:
            if passenger_id <= 0:
                raise ValidationException("乘客ID必须大于0")
        
        # 检查是否有重复ID
        if len(v) != len(set(v)):
            raise ValidationException("乘客ID不能重复")
        
        return v

