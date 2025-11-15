from typing import Optional, Dict
from fastapi import APIRouter, Depends, HTTPException, status, Header
from fastapi.responses import JSONResponse
from app.schemas.common import Response
from sqlalchemy.orm import Session
from app.core.security import get_current_user
from app.models.user import User
from app.db.session import get_db


router = APIRouter()
_supplement_store: Dict[str, dict] = {}


@router.get("", status_code=status.HTTP_200_OK, response_model=Response)
async def get_points(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    return Response(code=200, message="OK", data={"balance": 10000, "currency": "points"})


@router.post("/supplements", response_model=Response)
async def post_points_supplement(
    idempotency_key: Optional[str] = Header(None, alias="Idempotency-Key"),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    if not idempotency_key:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Missing Idempotency-Key")
    if idempotency_key in _supplement_store:
        return JSONResponse(status_code=200, content=Response(code=200, message="OK", data=_supplement_store[idempotency_key]).model_dump())
    data = {"supplementId": f"sp_{idempotency_key}", "status": "pending"}
    _supplement_store[idempotency_key] = data
    return JSONResponse(status_code=202, content=Response(code=202, message="Accepted", data=data).model_dump())


@router.get("/exclusions", status_code=status.HTTP_200_OK, response_model=Response)
async def get_points_exclusions(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    items = [
        {"type": "redeemed_ticket", "description": "积分兑换车票不参与累积"},
        {"type": "substitute_ticket", "description": "代用票不参与累积"},
        {"type": "onboard_supplement", "description": "列车补票不参与累积"},
        {"type": "arrival_supplement", "description": "到站补票不参与累积"},
        {"type": "non_realname", "description": "非实名制车票不参与累积"},
    ]
    return Response(code=200, message="OK", data={"items": items})