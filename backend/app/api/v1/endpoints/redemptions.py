from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, status, Query, Header
from app.schemas.common import Response
from sqlalchemy.orm import Session
from app.core.security import get_current_user
from app.models.user import User
from app.db.session import get_db


router = APIRouter()


@router.get("/options", status_code=status.HTTP_200_OK, response_model=Response)
async def get_options(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
    from_station: Optional[str] = Query(None, alias="from"),
    to_station: Optional[str] = Query(None, alias="to"),
    date: Optional[str] = Query(None)
):
    if not from_station or not to_station or not date:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="INVALID_QUERY")
    return Response(code=200, message="OK", data={"options": [{"product": "ticket", "trainNo": "G1234", "class": "second", "pointsCost": 8000, "seatsAvailable": 20}]})


@router.post("/tickets", status_code=status.HTTP_201_CREATED, response_model=Response)
async def redeem_ticket(
    idempotency_key: Optional[str] = Header(None, alias="Idempotency-Key"),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    if not idempotency_key:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Missing Idempotency-Key")
    return Response(code=201, message="Created", data={"redemptionId": "r_001", "status": "created", "pointsCost": 8000})
