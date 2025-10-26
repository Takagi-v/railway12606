"""
User Schemas
用户相关的Pydantic模型
"""
from datetime import datetime
from typing import Optional
from pydantic import BaseModel, EmailStr, Field, validator
import re


class UserBase(BaseModel):
    """Base user schema"""
    username: str = Field(..., min_length=6, max_length=30)
    email: EmailStr
    real_name: str = Field(..., min_length=2, max_length=50)
    id_type: str
    id_number: str
    phone: str = Field(..., min_length=11, max_length=11)
    user_type: str


class UserRegister(UserBase):
    """User registration schema"""
    password: str = Field(..., min_length=6, max_length=20)
    
    @validator('username')
    def username_alphanumeric(cls, v):
        if not re.match(r'^[a-zA-Z0-9]+$', v):
            raise ValueError('用户名只能包含字母和数字')
        return v
    
    @validator('password')
    def password_complexity(cls, v):
        if not re.search(r'[a-zA-Z]', v) or not re.search(r'\d', v):
            raise ValueError('密码必须包含字母和数字')
        return v
    
    @validator('phone')
    def phone_valid(cls, v):
        if not re.match(r'^1\d{10}$', v):
            raise ValueError('请输入有效的手机号')
        return v


class UserLogin(BaseModel):
    """User login schema"""
    username: str
    password: str
    captcha: Optional[str] = None


class UserUpdate(BaseModel):
    """User update schema"""
    real_name: Optional[str] = None
    phone: Optional[str] = None
    email: Optional[EmailStr] = None


class UserResponse(UserBase):
    """User response schema"""
    id: int
    create_time: datetime
    
    class Config:
        from_attributes = True


class TokenResponse(BaseModel):
    """Token response schema"""
    access_token: str
    token_type: str = "bearer"
    user_id: int
    username: str

