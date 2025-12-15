"""
User Endpoints
个人信息管理相关API
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.schemas.user import UserResponse, UserUpdate
from app.schemas.common import Response
from app.models.user import User
from app.api.deps import get_current_user
from app.core.exceptions import ValidationException, NotFoundException

router = APIRouter()


@router.get("/profile", response_model=Response[UserResponse])
async def get_profile(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    获取个人信息
    """
    return Response(
        code=200,
        message="查询成功",
        data=UserResponse.model_validate(current_user)
    )


@router.put("/profile", response_model=Response[UserResponse])
async def update_profile(
    user_update: UserUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    更新个人信息
    
    可编辑字段:
    - **real_name**: 真实姓名
    - **phone**: 手机号
    - **email**: 邮箱
    """
    # Check if phone is being changed and already exists
    if user_update.phone and user_update.phone != current_user.phone:
        if db.query(User).filter(User.phone == user_update.phone).first():
            raise ValidationException("手机号已被使用")
        current_user.phone = user_update.phone
    
    # Check if email is being changed and already exists
    if user_update.email and user_update.email != current_user.email:
        if db.query(User).filter(User.email == user_update.email).first():
            raise ValidationException("邮箱已被使用")
        current_user.email = user_update.email
    
    # Update real_name if provided
    if user_update.real_name:
        current_user.real_name = user_update.real_name

    # Update user_type if provided
    if user_update.user_type:
        current_user.user_type = user_update.user_type
    
    db.commit()
    db.refresh(current_user)
    
    return Response(
        code=200,
        message="更新成功",
        data=UserResponse.model_validate(current_user)
    )

