from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, status
from app.schemas.common import Response
from sqlalchemy.orm import Session
from app.core.security import get_current_user
from app.models.user import User
from app.db.session import get_db


router = APIRouter()


@router.get("", status_code=status.HTTP_200_OK, response_model=Response)
async def list_privileges(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    data = [
        {"code": "priority_service", "name": "优先服务", "levelRequired": "金卡", "description": "会员专享服务说明", "available": True}
    ]
    return Response(code=200, message="OK", data=data)