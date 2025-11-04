"""
Passenger Schemas
乘客相关的Pydantic模型
"""
from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field
from app.models.enums import IdType, PassengerType


class PassengerBase(BaseModel):
    """Base passenger schema"""
    name: str = Field(..., min_length=2, max_length=50)
    id_type: IdType
    id_number: str
    phone: str = Field(..., min_length=11, max_length=11)
    passenger_type: PassengerType = Field(..., description="成人/学生/儿童")


class PassengerCreate(PassengerBase):
    """Create passenger schema"""
    pass


class PassengerUpdate(PassengerBase):
    """Update passenger schema"""
    pass


class PassengerResponse(PassengerBase):
    """Passenger response schema"""
    id: int
    user_id: int
    verified: bool
    create_time: datetime
    
    class Config:
        from_attributes = True

