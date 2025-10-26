"""
Passenger Endpoints
乘客管理相关API
"""
from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.schemas.passenger import PassengerCreate, PassengerUpdate, PassengerResponse
from app.schemas.common import Response
from app.models.user import User
from app.models.passenger import Passenger
from app.core.security import get_current_user

router = APIRouter()


@router.get("", response_model=Response[List[PassengerResponse]])
async def get_passengers(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    获取当前用户的所有乘客
    """
    passengers = db.query(Passenger).filter(
        Passenger.user_id == current_user.id
    ).all()
    
    return Response(
        code=200,
        message="查询成功",
        data=[PassengerResponse.model_validate(p) for p in passengers]
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
    # Check if passenger with same id_number already exists for this user
    existing = db.query(Passenger).filter(
        Passenger.user_id == current_user.id,
        Passenger.id_number == passenger_data.id_number
    ).first()
    
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="该证件号的乘客已存在"
        )
    
    # Create new passenger
    new_passenger = Passenger(
        user_id=current_user.id,
        **passenger_data.model_dump()
    )
    
    db.add(new_passenger)
    db.commit()
    db.refresh(new_passenger)
    
    return Response(
        code=200,
        message="添加成功",
        data=PassengerResponse.model_validate(new_passenger)
    )


@router.put("/{passenger_id}", response_model=Response[PassengerResponse])
async def update_passenger(
    passenger_id: int,
    passenger_data: PassengerUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    编辑乘客信息
    """
    passenger = db.query(Passenger).filter(
        Passenger.id == passenger_id,
        Passenger.user_id == current_user.id
    ).first()
    
    if not passenger:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="乘客不存在"
        )
    
    # Update passenger fields
    for field, value in passenger_data.model_dump().items():
        setattr(passenger, field, value)
    
    db.commit()
    db.refresh(passenger)
    
    return Response(
        code=200,
        message="修改成功",
        data=PassengerResponse.model_validate(passenger)
    )


@router.delete("/{passenger_id}", response_model=Response)
async def delete_passenger(
    passenger_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    删除乘客
    """
    passenger = db.query(Passenger).filter(
        Passenger.id == passenger_id,
        Passenger.user_id == current_user.id
    ).first()
    
    if not passenger:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="乘客不存在"
        )
    
    # TODO: Check if passenger has uncompleted orders
    # For now, just delete
    
    db.delete(passenger)
    db.commit()
    
    return Response(code=200, message="删除成功")

