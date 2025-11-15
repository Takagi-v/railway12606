from typing import Optional
from fastapi import APIRouter, Header, HTTPException, status, Query
from app.schemas.common import Response


router = APIRouter()


@router.get("/options", status_code=status.HTTP_200_OK, response_model=Response)
async def get_options(
    authorization: Optional[str] = Header(None),
    from_station: Optional[str] = Query(None, alias="from"),
    to_station: Optional[str] = Query(None, alias="to"),
    date: Optional[str] = Query(None)
):
    if authorization is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized")
    if not from_station or not to_station or not date:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="INVALID_QUERY")
    return Response(code=200, message="OK", data={"options": [{"product": "ticket", "trainNo": "G1234", "class": "second", "pointsCost": 8000, "seatsAvailable": 20}]})


@router.post("/tickets", status_code=status.HTTP_201_CREATED, response_model=Response)
async def redeem_ticket(
    authorization: Optional[str] = Header(None),
    idempotency_key: Optional[str] = Header(None, alias="Idempotency-Key")
):
    if authorization is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized")
    if not idempotency_key:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Missing Idempotency-Key")
    return Response(code=201, message="Created", data={"redemptionId": "r_001", "status": "created", "pointsCost": 8000})
