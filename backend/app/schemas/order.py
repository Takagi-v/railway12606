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
    train_id: int
    travel_date: date
    passengers: List[OrderPassengerCreate]


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
