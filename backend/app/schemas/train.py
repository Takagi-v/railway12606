"""
Train and Station Schemas
车次和车站相关的Pydantic模型
"""
from datetime import date, time
from typing import Optional
from decimal import Decimal
from pydantic import BaseModel


class StationBase(BaseModel):
    """Base station schema"""
    station_name: str
    city: str
    pinyin: str
    short_pinyin: str


class StationResponse(StationBase):
    """Station response schema"""
    id: int
    
    class Config:
        from_attributes = True


class SeatAvailability(BaseModel):
    """Seat availability info"""
    available: int
    price: Decimal


class TrainSearchResponse(BaseModel):
    """Train search response"""
    train_id: int
    train_number: str
    train_type: str
    departure_station: str
    arrival_station: str
    departure_time: str
    arrival_time: str
    arrival_day_offset: int
    duration: str
    first_class: SeatAvailability
    second_class: SeatAvailability
    soft_sleeper: SeatAvailability
    hard_sleeper: SeatAvailability


class TrainDetailResponse(BaseModel):
    """Train detail response"""
    id: int
    train_number: str
    train_type: str
    departure_station_id: int
    arrival_station_id: int
    departure_time: time
    arrival_time: time
    duration_minutes: int
    first_class_seats: int
    second_class_seats: int
    soft_sleeper_seats: int
    hard_sleeper_seats: int
    first_class_price: Decimal
    second_class_price: Decimal
    soft_sleeper_price: Decimal
    hard_sleeper_price: Decimal
    
    class Config:
        from_attributes = True


class TrainAvailabilityResponse(BaseModel):
    """Train availability response for a given date"""
    first_class: SeatAvailability
    second_class: SeatAvailability
    soft_sleeper: SeatAvailability
    hard_sleeper: SeatAvailability

