from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, status, Body
from app.schemas.common import Response
from sqlalchemy.orm import Session
from app.core.security import get_current_user
from app.models.user import User
from app.db.session import get_db


router = APIRouter()


@router.post("", status_code=status.HTTP_201_CREATED, response_model=Response)
async def add_beneficiary(
    body: dict = Body(...),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    name = body.get("name")
    id_type = body.get("idType")
    id_number = body.get("idNumber")
    if not all([name, id_type, id_number]):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="INVALID_INPUT")
    return Response(code=201, message="Created", data={"id": "b_001", "verified": False})
