"""
Order Schemas
订单相关的Pydantic模型
"""
from datetime import datetime, date
from typing import List, Optional
from decimal import Decimal
from pydantic import BaseModel, field_validator, Field, model_validator
from app.models.enums import PassengerType, SeatType, OrderStatus, RefundStatus
from app.core.exceptions import ValidationException


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
    seat_selection: Optional[List[str]] = Field(None, description="选座偏好，如 ['A', 'B', 'C']")
    
    @field_validator('travel_date')
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
    
    @field_validator('passengers')
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
    passenger_id: int
    name: str
    id_type: Optional[str] = None
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
    
    @model_validator(mode='before')
    @classmethod
    def flatten_passenger(cls, v):
        # Handle ORM object
        if hasattr(v, 'passenger') and hasattr(v, 'seat'):
            return {
                "passenger_id": v.passenger_id,
                "name": v.passenger.name,
                "id_type": v.passenger.id_type.value if hasattr(v.passenger.id_type, 'value') else v.passenger.id_type,
                "id_number": v.passenger.id_number,
                "seat_type": v.seat_type,
                "seat_number": v.seat.seat_number,
                "ticket_type": v.ticket_type,
                "price": v.price,
                "refund_status": v.refund_status
            }
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
    passengers: List[OrderPassengerResponse] = []
    create_time: datetime
    
    @model_validator(mode='before')
    @classmethod
    def flatten_order(cls, v):
        # Handle ORM object
        if hasattr(v, 'train'):
            return {
                "id": v.id,
                "order_number": v.order_number,
                "train_number": v.train.train_number,
                "departure_station": v.train.departure_station.station_name,
                "arrival_station": v.train.arrival_station.station_name,
                "travel_date": v.travel_date,
                "departure_time": str(v.train.departure_time),
                "total_price": v.total_price,
                "status": v.status,
                "passenger_count": len(v.order_passengers),
                "passengers": v.order_passengers,
                "create_time": v.create_time
            }
        return v

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
    
    @model_validator(mode='before')
    @classmethod
    def flatten_order_detail(cls, v):
        # Handle ORM object
        if hasattr(v, 'train'):
            return {
                "id": v.id,
                "order_number": v.order_number,
                "train_number": v.train.train_number,
                "departure_station": v.train.departure_station.station_name,
                "arrival_station": v.train.arrival_station.station_name,
                "departure_time": str(v.train.departure_time),
                "arrival_time": str(v.train.arrival_time),
                "travel_date": v.travel_date,
                "passengers": v.order_passengers, # List of OrderPassenger objects, will be handled by OrderPassengerResponse validator
                "total_price": v.total_price,
                "status": v.status,
                "create_time": v.create_time,
                "pay_time": v.pay_time,
                "cancel_time": v.cancel_time
            }
        return v

    class Config:
        from_attributes = True


class RefundRequest(BaseModel):
    """Refund request schema"""
    passenger_ids: List[int] = []  # Empty list means refund all
