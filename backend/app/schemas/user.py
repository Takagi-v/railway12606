"""
User Schemas
用户相关的Pydantic模型
"""
from datetime import datetime
from typing import Optional
from pydantic import BaseModel, EmailStr, Field, validator
import re
from app.models.enums import IdType, UserType


class UserBase(BaseModel):
    """Base user schema"""
    username: str = Field(..., min_length=6, max_length=30)
    email: EmailStr
    real_name: str = Field(..., min_length=2, max_length=50)
    id_type: IdType
    id_number: str
    phone: str = Field(..., min_length=11, max_length=11)
    user_type: UserType


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
    real_name: Optional[str] = Field(None, min_length=2, max_length=50)
    phone: Optional[str] = Field(None, min_length=11, max_length=11)
    email: Optional[EmailStr] = None
    user_type: Optional[UserType] = None
    
    @validator('phone')
    def phone_valid(cls, v):
        if v and not re.match(r'^1\d{10}$', v):
            raise ValueError('请输入有效的手机号')
        return v
    
    @validator('real_name')
    def real_name_valid(cls, v):
        if v and not re.match(r'^[\u4e00-\u9fa5a-zA-Z\s]+$', v):
            raise ValueError('姓名只能包含中文、英文字母和空格')
        return v


class UserResponse(BaseModel):
    """User response schema"""
    id: int
    username: str  # 移除长度限制，因为响应时不需要验证
    email: EmailStr
    real_name: str
    id_type: str
    id_number: str
    phone: str
    user_type: str
    create_time: datetime
    
    class Config:
        from_attributes = True


class TokenResponse(BaseModel):
    """Token response schema"""
    access_token: str
    token_type: str = "bearer"
    refresh_token: Optional[str] = None
    expires_in: int = 3600  # Token expiry in seconds (default 1 hour)
    user_id: int
    username: str

