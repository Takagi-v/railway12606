from typing import Dict, Tuple
from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException, status, Body, Header
from sqlalchemy.orm import Session
from app.schemas.common import Response
from app.core.security import get_current_user
from app.models.user import User
from app.db.session import get_db


router = APIRouter()

_applied_ids: Dict[Tuple[str, str], bool] = {}


@router.post("", status_code=status.HTTP_201_CREATED, response_model=Response)
async def apply_membership(
    body: dict = Body(...),
    authorization: str | None = Header(None),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    if authorization is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized")
    name = body.get("name")
    id_type = body.get("idType")
    id_number = body.get("idNumber")
    birth_date = body.get("birthDate")
    phone = body.get("phone")
    if not all([name, id_type, id_number, birth_date, phone]):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid input")
    try:
        bd = datetime.strptime(birth_date, "%Y-%m-%d").date()
    except Exception:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid input")
    today = datetime.utcnow().date()
    age = today.year - bd.year - ((today.month, today.day) < (bd.month, bd.day))
    if age < 12:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="INVALID_AGE")
    key = (str(id_type), str(id_number))
    if key in _applied_ids:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="MEMBER_ALREADY_EXISTS")
    _applied_ids[key] = True
    return Response(code=201, message="Created", data={"memberId": "m_001", "status": "pending"})


@router.get("/me", status_code=status.HTTP_200_OK, response_model=Response)
async def get_membership_me(
    authorization: str | None = Header(None),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    if authorization is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized")
    return Response(code=200, message="OK", data={"memberId": "m_001", "status": "verified"})
