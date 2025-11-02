"""
Authentication Endpoints
用户认证相关API
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.schemas.user import UserRegister, UserLogin, TokenResponse, UserResponse
from app.schemas.common import Response
from app.models.user import User
from app.core.security import verify_password, get_password_hash, create_access_token

router = APIRouter()


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
    # Check if username exists
    if db.query(User).filter(User.username == user_data.username).first():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="用户名已存在"
        )
    
    # Check if email exists
    if db.query(User).filter(User.email == user_data.email).first():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="邮箱已注册"
        )
    
    # Check if phone exists
    if db.query(User).filter(User.phone == user_data.phone).first():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="手机号已注册"
        )
    
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
    """
    # Find user by username or phone
    user = db.query(User).filter(
        (User.username == login_data.username) | 
        (User.phone == login_data.username)
    ).first()
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="用户名或密码错误"
        )
    
    if not verify_password(login_data.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="用户名或密码错误"
        )
    
    # Create access token
    access_token = create_access_token(data={"sub": user.id})
    
    return Response(
        code=200,
        message="登录成功",
        data=TokenResponse(
            access_token=access_token,
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

