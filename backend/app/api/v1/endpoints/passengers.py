"""
Passenger Endpoints
乘客管理相关API
"""
from typing import List

from fastapi import APIRouter, Depends, HTTPException, Path, status
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.api.deps import get_current_user
from app.core.exceptions import (
    BusinessException,
    NotFoundException,
    ValidationException,
)
from app.core.validators import UserValidator
from app.db.session import get_db
from app.models.enums import PassengerType
from app.models.order import OrderPassenger
from app.models.passenger import Passenger
from app.models.user import User
from app.schemas.common import Response
from app.schemas.passenger import PassengerCreate, PassengerResponse, PassengerUpdate

router = APIRouter()


@router.get("", response_model=Response[List[PassengerResponse]])
async def get_passengers(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    获取当前用户的所有乘客
    默认乘客（用户本人）会排在最前面
    """
    passengers = db.query(Passenger).filter(
        Passenger.user_id == current_user.id
    ).order_by(Passenger.is_default.desc(), Passenger.create_time.asc()).all()
    
    return Response(
        code=200,
        message="查询成功",
        data=[PassengerResponse.model_validate(p) for p in passengers]
    )


@router.post("/sync-default", response_model=Response[PassengerResponse])
async def sync_default_passenger(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    同步/创建默认乘客（用户本人）
    
    如果默认乘客不存在，则根据用户信息创建；
    如果存在，则更新信息与用户保持一致
    """
    # Check if default passenger already exists
    default_passenger = db.query(Passenger).filter(
        Passenger.user_id == current_user.id,
        Passenger.is_default == True
    ).first()
    
    # Map user_type to passenger_type
    passenger_type_map = {
        "成人": PassengerType.ADULT,
        "学生": PassengerType.STUDENT
    }
    passenger_type = passenger_type_map.get(current_user.user_type.value, PassengerType.ADULT)
    
    if default_passenger:
        # Update existing default passenger with current user info
        default_passenger.name = current_user.real_name
        default_passenger.id_type = current_user.id_type
        default_passenger.id_number = current_user.id_number
        default_passenger.phone = current_user.phone
        default_passenger.passenger_type = passenger_type
        default_passenger.verified = True  # User's own info is considered verified
        
        db.commit()
        db.refresh(default_passenger)
        
        return Response(
            code=200,
            message="默认乘客信息已同步",
            data=PassengerResponse.model_validate(default_passenger)
        )
    else:
        # Create new default passenger from user info
        new_default_passenger = Passenger(
            user_id=current_user.id,
            name=current_user.real_name,
            id_type=current_user.id_type,
            id_number=current_user.id_number,
            phone=current_user.phone,
            passenger_type=passenger_type,
            verified=True,
            is_default=True
        )
        
        db.add(new_default_passenger)
        try:
            db.commit()
            db.refresh(new_default_passenger)
        except IntegrityError:
            db.rollback()
            raise ValidationException("无法创建默认乘客，可能已存在相同证件号的乘客")
        
        return Response(
            code=201,
            message="默认乘客已创建",
            data=PassengerResponse.model_validate(new_default_passenger)
        )


@router.post("", response_model=Response[PassengerResponse], status_code=status.HTTP_201_CREATED)
async def create_passenger(
    passenger_data: PassengerCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    添加乘客
    
    - **name**: 姓名
    - **id_type**: 证件类型
    - **id_number**: 证件号码
    - **phone**: 手机号
    - **passenger_type**: 旅客类型（成人/学生/儿童）
    """
    # Check if passenger with same (id_type, id_number) already exists for this user
    existing = db.query(Passenger).filter(
        Passenger.user_id == current_user.id,
        Passenger.id_type == passenger_data.id_type,
        Passenger.id_number == passenger_data.id_number
    ).first()
    
    if existing:
        raise ValidationException("该证件号的乘客已存在")
    
    # Create new passenger
    new_passenger = Passenger(
        user_id=current_user.id,
        **passenger_data.model_dump()
    )
    
    db.add(new_passenger)
    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="该证件已存在"
        )
    db.refresh(new_passenger)
    
    return Response(
        code=200,
        message="添加成功",
        data=PassengerResponse.model_validate(new_passenger)
    )


@router.put("/{passenger_id}", response_model=Response[PassengerResponse])
async def update_passenger(
    passenger_data: PassengerUpdate,
    passenger_id: int = Path(..., gt=0, description="乘客ID"),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    编辑乘客信息
    """
    # 验证更新的乘客数据
    if passenger_data.name:
        UserValidator.validate_real_name(passenger_data.name)
    if passenger_data.phone:
        UserValidator.validate_phone(passenger_data.phone)
    if passenger_data.id_number:
        UserValidator.validate_id_number(passenger_data.id_number)
    
    passenger = db.query(Passenger).filter(
        Passenger.id == passenger_id,
        Passenger.user_id == current_user.id
    ).first()
    
    if not passenger:
        raise NotFoundException("乘客不存在")
    
    # Update passenger fields
    update_data = passenger_data.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(passenger, field, value)
    
    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="该证件已存在"
        )
    db.refresh(passenger)
    
    return Response(
        code=200,
        message="修改成功",
        data=PassengerResponse.model_validate(passenger)
    )


@router.post("/batch-delete", response_model=Response)
async def batch_delete_passengers(
    passenger_ids: List[int],
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    批量删除乘客
    """
    if not passenger_ids:
        raise ValidationException("请选择要删除的乘客")

    # 1. Verify all passengers exist and belong to user
    passengers = db.query(Passenger).filter(
        Passenger.id.in_(passenger_ids),
        Passenger.user_id == current_user.id
    ).all()
    
    if len(passengers) != len(set(passenger_ids)):
        # Some IDs were not found or don't belong to user
        raise ValidationException("部分乘客不存在或无法操作")
        
    # 2. Check for default passenger
    for p in passengers:
        if p.is_default:
            raise BusinessException(f"乘客 {p.name} 是默认乘客，不允许删除")
            
    # 3. Check for orders
    # Get all passenger IDs that have orders
    passengers_with_orders = db.query(OrderPassenger.passenger_id).filter(
        OrderPassenger.passenger_id.in_(passenger_ids)
    ).all()
    
    if passengers_with_orders:
        # Find names for error message
        p_ids_with_orders = {p[0] for p in passengers_with_orders}
        names = [p.name for p in passengers if p.id in p_ids_with_orders]
        raise BusinessException(f"乘客 {', '.join(names)} 已有购票记录，无法删除")
        
    # 4. Delete all
    for p in passengers:
        db.delete(p)
    db.commit()
    
    return Response(code=200, message="批量删除成功")


@router.delete("/{passenger_id}", response_model=Response)
async def delete_passenger(
    passenger_id: int = Path(..., gt=0, description="乘客ID"),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    删除乘客
    注意：默认乘客（用户本人）不允许删除
    """
    passenger = db.query(Passenger).filter(
        Passenger.id == passenger_id,
        Passenger.user_id == current_user.id
    ).first()
    
    if not passenger:
        raise NotFoundException("乘客不存在")
    
    # Prevent deletion of default passenger
    if passenger.is_default:
        raise BusinessException("默认乘客（用户本人）不允许删除")
    
    # Check if passenger has any associated orders
    has_orders = db.query(OrderPassenger).filter(
        OrderPassenger.passenger_id == passenger_id
    ).first()
    
    if has_orders:
        raise BusinessException("该乘客已有购票记录，无法删除")
    
    db.delete(passenger)
    db.commit()
    
    return Response(code=200, message="删除成功")

