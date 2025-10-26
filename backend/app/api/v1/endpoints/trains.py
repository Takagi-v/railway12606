"""
Train Endpoints
车次查询相关API
"""
from typing import List
from datetime import date
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.schemas.train import TrainSearchResponse
from app.schemas.common import Response

router = APIRouter()


@router.get("/search", response_model=Response[List[TrainSearchResponse]])
async def search_trains(
    departure_city: str = Query(..., description="出发地"),
    arrival_city: str = Query(..., description="到达地"),
    travel_date: date = Query(..., description="出发日期"),
    db: Session = Depends(get_db)
):
    """
    查询车次
    
    - **departure_city**: 出发地（城市或车站名）
    - **arrival_city**: 到达地（城市或车站名）
    - **travel_date**: 出发日期（YYYY-MM-DD）
    
    TODO: 实现车次查询逻辑
    - 根据出发地和目的地查询车次
    - 计算余票数
    - 返回车次列表
    """
    # TODO: Implement train search logic
    # This is a placeholder response
    return Response(
        code=200,
        message="查询成功",
        data=[]
    )

