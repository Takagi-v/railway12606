from typing import Optional
from fastapi import APIRouter, Header, HTTPException, status, Body
from app.schemas.common import Response


router = APIRouter()


@router.post("", status_code=status.HTTP_201_CREATED, response_model=Response)
async def add_beneficiary(
    authorization: Optional[str] = Header(None),
    body: dict = Body(...)
):
    if authorization is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized")
    name = body.get("name")
    id_type = body.get("idType")
    id_number = body.get("idNumber")
    if not all([name, id_type, id_number]):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="INVALID_INPUT")
    return Response(code=201, message="Created", data={"id": "b_001", "verified": False})
