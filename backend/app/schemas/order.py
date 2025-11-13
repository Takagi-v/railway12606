"""
Order Schemas
订单相关的Pydantic模型
"""
from datetime import datetime, date
from typing import List, Optional
from decimal import Decimal
from pydantic import BaseModel, field_validator
from app.models.enums import PassengerType, SeatType, OrderStatus, RefundStatus


class OrderPassengerCreate(BaseModel):
    """Order passenger create schema"""
    passenger_id: int
    ticket_type: PassengerType
    seat_type: SeatType


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
    seat_type: SeatType
    seat_number: Optional[str]
    ticket_type: PassengerType
    price: Decimal
    refund_status: RefundStatus

    @field_validator('price')
    @classmethod
    def price_nonnegative(cls, v: Decimal):
        if v < 0:
            raise ValueError('票价必须为非负数')
        return v
    
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
    status: OrderStatus
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
    status: OrderStatus
    create_time: datetime
    pay_time: Optional[datetime]
    cancel_time: Optional[datetime]
    
    class Config:
        from_attributes = True


class RefundRequest(BaseModel):
    """Refund request schema"""
    passenger_ids: List[int] = []  # Empty list means refund all
