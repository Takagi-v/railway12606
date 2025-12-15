"""
Password Recovery Endpoints
找回密码相关API
"""
from datetime import datetime, timedelta
import secrets
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from loguru import logger

from app.db.session import get_db
from app.schemas.common import Response
from app.schemas.password_recovery import (
    FaceRecoveryRequest,
    PhoneRecoveryRequest,
    EmailRecoveryRequest,
    RecoveryVerifyRequest,
    RecoveryResendRequest,
    PasswordResetRequest,
    RecoveryTokenResponse
)
from app.models.user import User
from app.core.security import get_password_hash
from app.core.validators import UserValidator
from app.core.exceptions import ValidationException
from app.core.config import settings

router = APIRouter(prefix="/auth/password/recovery", tags=["认证"])

# 简易的内存存储，用于演示验证码/恢复token
RECOVERY_STORE = {}
# 默认验证码和token有效期（分钟）
DEFAULT_EXPIRE_MINUTES = 10


def _generate_code() -> str:
    """生成6位数字验证码"""
    return f"{secrets.randbelow(10**6):06d}"


def _generate_token() -> str:
    """生成恢复token"""
    return secrets.token_urlsafe(32)


def _find_user_by_identity(db: Session, *, email: str | None = None, phone: str | None = None,
                           id_type: str, id_number: str) -> User:
    """根据身份信息查找用户"""
    # 兼容"身份证"和"居民身份证"
    if id_type in ("身份证", "居民身份证"):
        # 数据库Enum中目前仅包含"身份证"，查询时统一使用"身份证"避免报错
        query = db.query(User).filter(User.id_type == "身份证", User.id_number == id_number)
    else:
        query = db.query(User).filter(User.id_type == id_type, User.id_number == id_number)
        
    if email:
        query = query.filter(User.email == email)
    if phone:
        query = query.filter(User.phone == phone)
    return query.first()


def _create_recovery_record(user_id: int, recovery_type: str) -> RecoveryTokenResponse:
    """创建恢复记录并返回token"""
    token = _generate_token()
    code = _generate_code()
    expire_time = datetime.utcnow() + timedelta(minutes=DEFAULT_EXPIRE_MINUTES)
    RECOVERY_STORE[token] = {
        "user_id": user_id,
        "code": code,
        "expire": expire_time,
        "type": recovery_type,
        "verified": False
    }
    # 发送验证码的逻辑（短信/邮件）在此简化为日志输出
    logger.info(f"[PasswordRecovery] send code={code} to user_id={user_id} via {recovery_type}")
    print(f"====== [DEBUG] Password Recovery Code: {code} ======")
    return RecoveryTokenResponse(token=token, expire_time=expire_time)


@router.post("/face", response_model=Response[RecoveryTokenResponse], status_code=status.HTTP_200_OK)
async def submit_face_recovery(payload: FaceRecoveryRequest, db: Session = Depends(get_db)):
    """
    人脸找回密码：校验邮箱+证件信息后生成恢复token与验证码
    """
    UserValidator.validate_email(payload.email)
    UserValidator.validate_id_number(payload.id_number, payload.id_type)
    user = _find_user_by_identity(db, email=payload.email, id_type=payload.id_type, id_number=payload.id_number)
    if not user:
        raise ValidationException("用户信息不匹配")

    token_info = _create_recovery_record(user.id, "face")
    return Response(code=200, message="验证信息已提交，验证码已发送", data=token_info)


@router.post("/phone", response_model=Response[RecoveryTokenResponse], status_code=status.HTTP_200_OK)
async def submit_phone_recovery(payload: PhoneRecoveryRequest, db: Session = Depends(get_db)):
    """
    手机找回密码：校验手机+证件信息后生成恢复token与验证码
    """
    UserValidator.validate_phone(payload.phone)
    UserValidator.validate_id_number(payload.id_number, payload.id_type)
    user = _find_user_by_identity(db, phone=payload.phone, id_type=payload.id_type, id_number=payload.id_number)
    if not user:
        raise ValidationException("用户信息不匹配")

    token_info = _create_recovery_record(user.id, "phone")
    return Response(code=200, message="验证码已发送到手机", data=token_info)


@router.post("/email", response_model=Response[RecoveryTokenResponse], status_code=status.HTTP_200_OK)
async def submit_email_recovery(payload: EmailRecoveryRequest, db: Session = Depends(get_db)):
    """
    邮箱找回密码：校验邮箱+证件信息后生成恢复token与验证码
    """
    UserValidator.validate_email(payload.email)
    UserValidator.validate_id_number(payload.id_number, payload.id_type)
    user = _find_user_by_identity(db, email=payload.email, id_type=payload.id_type, id_number=payload.id_number)
    if not user:
        raise ValidationException("用户信息不匹配")

    token_info = _create_recovery_record(user.id, "email")
    return Response(code=200, message="验证码已发送到邮箱", data=token_info)


@router.post("/verify", response_model=Response, status_code=status.HTTP_200_OK)
async def verify_recovery_code(payload: RecoveryVerifyRequest):
    """
    校验验证码
    """
    record = RECOVERY_STORE.get(payload.token)
    if not record:
        raise ValidationException("恢复凭证无效，请重新提交")
    if record["expire"] < datetime.utcnow():
        RECOVERY_STORE.pop(payload.token, None)
        raise ValidationException("验证码已过期，请重新获取")
    
    # 严格校验验证码
    if record["code"] != payload.verification_code:
        raise ValidationException("验证码错误")

    if record["type"] != payload.type:
        raise ValidationException("恢复类型不匹配")

    record["verified"] = True
    return Response(code=200, message="验证码验证成功")


@router.post("/resend", response_model=Response, status_code=status.HTTP_200_OK)
async def resend_recovery_code(payload: RecoveryResendRequest):
    """
    重发验证码
    """
    record = RECOVERY_STORE.get(payload.token)
    if not record:
        raise ValidationException("恢复凭证无效，请重新提交")
        
    # Generate new code
    code = _generate_code()
    expire_time = datetime.utcnow() + timedelta(minutes=DEFAULT_EXPIRE_MINUTES)
    
    # Update record
    record["code"] = code
    record["expire"] = expire_time
    record["verified"] = False  # Reset verification status
    
    # Log sending (simulated)
    user_id = record["user_id"]
    recovery_type = record["type"]
    logger.info(f"[PasswordRecovery] Resend code={code} to user_id={user_id} via {recovery_type}")
    print(f"====== [DEBUG] Resent Password Recovery Code: {code} ======")
    
    return Response(code=200, message="验证码已重新发送")


@router.post("/reset", response_model=Response, status_code=status.HTTP_200_OK)
async def reset_password(payload: PasswordResetRequest, db: Session = Depends(get_db)):
    """
    重置密码：需先通过验证码验证
    """
    record = RECOVERY_STORE.get(payload.token)
    if not record:
        raise ValidationException("恢复凭证无效，请重新提交")
    if record["expire"] < datetime.utcnow():
        RECOVERY_STORE.pop(payload.token, None)
        raise ValidationException("验证码已过期，请重新获取")
    if not record.get("verified"):
        raise ValidationException("请先完成验证码验证")
    if payload.new_password != payload.confirm_password:
        raise ValidationException("两次密码输入不一致")

    # 更新密码
    user = db.query(User).filter(User.id == record["user_id"]).first()
    if not user:
        RECOVERY_STORE.pop(payload.token, None)
        raise ValidationException("用户不存在")

    UserValidator.validate_password(payload.new_password)
    user.password = get_password_hash(payload.new_password)
    db.commit()
    db.refresh(user)
    # 清理token
    RECOVERY_STORE.pop(payload.token, None)

    return Response(code=200, message="密码重置成功")
