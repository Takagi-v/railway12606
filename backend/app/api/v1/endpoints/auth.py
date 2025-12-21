"""Authentication Endpoints
用户认证相关API
"""
from fastapi import APIRouter, Depends, HTTPException, status, Body
from sqlalchemy.orm import Session
from datetime import timedelta
import random

from app.db.session import get_db
from app.schemas.user import UserRegister, UserLogin, UserResponse, TokenResponse
from app.schemas.common import Response
from app.models.user import User
from app.models.role import Role
from app.models.passenger import Passenger
from app.models.enums import PassengerType
from app.core.security import verify_password, get_password_hash, create_access_token, create_refresh_token
from app.core.config import settings
from app.api.deps import get_current_user
from app.core.exceptions import ValidationException, AuthenticationException
from app.core.validators import UserValidator
from pydantic import BaseModel

router = APIRouter()

# Simple in-memory storage for verification codes (for demonstration)
VERIFY_CODES = {}

class VerifyCodeRequest(BaseModel):
    username: str
    id_last_4: str

@router.post("/login/verify-code", response_model=Response)
async def send_verify_code(req: VerifyCodeRequest, db: Session = Depends(get_db)):
    """
    发送登录验证码
    验证用户名和证件号后4位，如果匹配则生成4位验证码
    """
    # Find user
    user = db.query(User).filter(
        (User.username == req.username) | 
        (User.phone == req.username)
    ).first()
    
    if not user:
        # Avoid user enumeration, but for this specific logic we need to match info
        raise ValidationException("用户信息不匹配")
        
    # Check ID last 4 digits
    if not user.id_number or len(user.id_number) < 4:
         raise ValidationException("用户信息不完整")
         
    real_last_4 = user.id_number[-4:]
    if real_last_4 != req.id_last_4:
        raise ValidationException("证件号后4位不匹配")
        
    # Generate 4-digit code
    code = str(random.randint(1000, 9999))
    print(f"====== [DEBUG] Generated Verification Code for user [{user.username}]: {code} ======")
    VERIFY_CODES[user.username] = code
    # Also store by phone if username is phone, or whatever was used to login
    VERIFY_CODES[req.username] = code
    if user.phone:
        VERIFY_CODES[user.phone] = code
        
    # In a real app, send via SMS. Here return it as requested.
    return Response(
        code=200,
        message="验证码已生成",
        data={"code": code}
    )


def _sync_default_passenger(db: Session, user: User):
    """
    Ensure default passenger exists for the user
    """
    try:
        # Check if default passenger already exists
        default_passenger = db.query(Passenger).filter(
            Passenger.user_id == user.id,
            Passenger.is_default == True
        ).first()
        
        # Map user_type to passenger_type
        # user.user_type is an Enum
        user_type_val = user.user_type.value if hasattr(user.user_type, 'value') else str(user.user_type)
        
        passenger_type_map = {
            "成人": PassengerType.ADULT,
            "学生": PassengerType.STUDENT,
            "儿童": PassengerType.CHILD,
            "残疾军人": PassengerType.DISABILITY_SOLDIER
        }
        passenger_type = passenger_type_map.get(user_type_val, PassengerType.ADULT)
        
        if default_passenger:
            # Update existing default passenger with current user info
            default_passenger.name = user.real_name
            default_passenger.id_type = user.id_type
            default_passenger.id_number = user.id_number
            default_passenger.phone = user.phone
            default_passenger.passenger_type = passenger_type
            default_passenger.verified = True
            
            db.commit()
            db.refresh(default_passenger)
        else:
            # Create new default passenger from user info
            new_default_passenger = Passenger(
                user_id=user.id,
                name=user.real_name,
                id_type=user.id_type,
                id_number=user.id_number,
                phone=user.phone,
                passenger_type=passenger_type,
                verified=True,
                is_default=True
            )
            
            db.add(new_default_passenger)
            db.commit()
            db.refresh(new_default_passenger)
    except Exception as e:
        # Log error but don't fail the main operation
        print(f"Failed to sync default passenger: {str(e)}")
        db.rollback()


@router.post("/register", response_model=Response[UserResponse], status_code=status.HTTP_201_CREATED)
async def register(user_data: UserRegister, db: Session = Depends(get_db)):
    """
    用户注册
    
    - **username**: 登录名（6-30位字母或数字）
    - **password**: 密码（6-20位，包含字母和数字）
    - **real_name**: 真实姓名
    - **id_type**: 证件类型
    - **id_number**: 证件号码
    - **phone**: 手机号
    - **email**: 邮箱
    - **user_type**: 用户类型（成人/学生）
    """
    # Validate user data using validators
    UserValidator.validate_username(user_data.username)
    UserValidator.validate_password(user_data.password)
    UserValidator.validate_phone(user_data.phone)
    UserValidator.validate_email(user_data.email)
    UserValidator.validate_real_name(user_data.real_name)
    UserValidator.validate_id_number(user_data.id_number, user_data.id_type)
    
    # Check if username exists
    if db.query(User).filter(User.username == user_data.username).first():
        raise ValidationException("用户名已存在")
    
    # Check if email exists
    if db.query(User).filter(User.email == user_data.email).first():
        raise ValidationException("邮箱已注册")
    
    # Check if phone exists
    if db.query(User).filter(User.phone == user_data.phone).first():
        raise ValidationException("手机号已注册")
    
    # Check if id_type + id_number exists
    if db.query(User).filter(
        User.id_type == user_data.id_type,
        User.id_number == user_data.id_number
    ).first():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="证件号码已注册"
        )
    
    # Create new user
    hashed_password = get_password_hash(user_data.password)
    new_user = User(
        username=user_data.username,
        password=hashed_password,
        real_name=user_data.real_name,
        id_type=user_data.id_type,
        id_number=user_data.id_number,
        phone=user_data.phone,
        email=user_data.email,
        user_type=user_data.user_type
    )
    
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    # 默认分配普通用户角色
    default_role = db.query(Role).filter(Role.name == "user", Role.is_active == 1).first()
    if default_role:
        new_user.roles.append(default_role)
        db.commit()
    
    # Sync default passenger
    _sync_default_passenger(db, new_user)
    
    return Response(
        code=200,
        message="注册成功",
        data=UserResponse.model_validate(new_user)
    )


@router.post("/login", response_model=Response[TokenResponse])
async def login(login_data: UserLogin, db: Session = Depends(get_db)):
    """
    用户登录
    
    - **username**: 用户名或手机号
    - **password**: 密码
    - **captcha**: 验证码（可选）
    - **id_last_4**: 证件号后4位（可选，特定验证流程需要）
    - **sms_code**: 短信验证码（可选，特定验证流程需要）
    """
    # Find user by username or phone
    user = db.query(User).filter(
        (User.username == login_data.username) | 
        (User.phone == login_data.username)
    ).first()
    
    if not user:
        raise AuthenticationException("用户名或密码错误")
    
    if not verify_password(login_data.password, user.password):
        raise AuthenticationException("用户名或密码错误")

    # Check for additional verification if provided
    if login_data.id_last_4 and login_data.sms_code:
        # Verify ID last 4
        if not user.id_number or user.id_number[-4:] != login_data.id_last_4:
            raise AuthenticationException("证件号后4位不匹配")
            
        # Verify SMS Code
        stored_code = VERIFY_CODES.get(login_data.username) or VERIFY_CODES.get(user.username) or VERIFY_CODES.get(user.phone)
        if not stored_code or stored_code != login_data.sms_code:
             raise AuthenticationException("验证码错误或已过期")
             
        # Clear code after successful use (optional but good practice)
        if login_data.username in VERIFY_CODES:
            del VERIFY_CODES[login_data.username]
    
    # Sync default passenger
    _sync_default_passenger(db, user)
    
    # Create access token and refresh token
    access_token = create_access_token(data={"sub": str(user.id)})
    refresh_token = create_refresh_token(data={"sub": str(user.id)})
    
    return Response(
        code=200,
        message="登录成功",
        data=TokenResponse(
            access_token=access_token,
            refresh_token=refresh_token,
            expires_in=3600,  # 1 hour in seconds
            user_id=user.id,
            username=user.username
        )
    )


@router.post("/logout", response_model=Response)
async def logout():
    """
    退出登录
    注意: JWT是无状态的，客户端需要删除本地token
    """
    return Response(code=200, message="退出成功")


@router.get("/test-token", response_model=Response[UserResponse])
async def test_token(current_user: User = Depends(get_current_user)):
    """
    测试令牌有效性
    
    验证当前用户的JWT令牌是否有效，并返回用户信息
    """
    return Response(
        code=200,
        message="令牌有效",
        data=UserResponse.model_validate(current_user)
    )


@router.post("/refresh", response_model=Response[TokenResponse])
async def refresh_token(current_user: User = Depends(get_current_user)):
    """
    刷新访问令牌
    
    使用当前有效的令牌获取新的访问令牌
    """
    # 创建新的访问令牌
    new_access_token = create_access_token(data={"sub": str(current_user.id)})
    
    return Response(
        code=200,
        message="令牌刷新成功",
        data=TokenResponse(
            access_token=new_access_token,
            user_id=current_user.id,
            username=current_user.username
        )
    )

