from typing import Optional
from fastapi import APIRouter, Header, HTTPException, status
from app.schemas.common import Response


router = APIRouter()


@router.get("", status_code=status.HTTP_200_OK, response_model=Response)
async def get_points(authorization: Optional[str] = Header(None)):
    if authorization is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized")
    return Response(code=200, message="OK", data={"balance": 10000, "currency": "points"})


@router.post("/supplements", status_code=status.HTTP_202_ACCEPTED, response_model=Response)
async def post_points_supplement(
    authorization: Optional[str] = Header(None),
    idempotency_key: Optional[str] = Header(None, alias="Idempotency-Key")
):
    if authorization is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized")
    if not idempotency_key:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Missing Idempotency-Key")
    return Response(code=202, message="Accepted", data={"supplementId": "sp_001", "status": "pending"})