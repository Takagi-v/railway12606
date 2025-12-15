"""
Password Recovery Schemas
找回密码相关的Pydantic模型
"""
from datetime import datetime
from typing import Optional
from pydantic import BaseModel, EmailStr, Field, ConfigDict


class BaseRecoveryRequest(BaseModel):
    """共用的身份校验字段"""
    model_config = ConfigDict(populate_by_name=True, extra="ignore")
    id_type: str = Field(..., description="证件类型", alias="idType")
    id_number: str = Field(..., description="证件号码", alias="idNumber")


class FaceRecoveryRequest(BaseRecoveryRequest):
    """人脸找回请求"""
    email: EmailStr


class PhoneRecoveryRequest(BaseRecoveryRequest):
    """手机找回请求"""
    phone: str = Field(..., min_length=11, max_length=11, description="手机号")


class EmailRecoveryRequest(BaseRecoveryRequest):
    """邮箱找回请求"""
    email: EmailStr


class RecoveryVerifyRequest(BaseModel):
    """验证码验证请求"""
    model_config = ConfigDict(populate_by_name=True, extra="ignore")
    token: str
    verification_code: str = Field(..., alias="verificationCode")
    type: str = Field(..., description="找回类型：face | phone | email")


class RecoveryResendRequest(BaseModel):
    """重发验证码请求"""
    token: str


class PasswordResetRequest(BaseModel):
    """重置密码请求"""
    model_config = ConfigDict(populate_by_name=True, extra="ignore")
    token: str
    new_password: str = Field(..., min_length=6, max_length=20, alias="newPassword")
    confirm_password: str = Field(..., min_length=6, max_length=20, alias="confirmPassword")


class RecoveryTokenResponse(BaseModel):
    """返回的恢复token"""
    token: str
    expire_time: datetime
