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
from app.core.exceptions import ValidationException, NotFoundException
from app.core.validators import TrainValidator, CommonValidator

router = APIRouter()


@router.get("/search", response_model=Response[List[TrainSearchResponse]])
async def search_trains(
    departure_city: str = Query(..., min_length=1, max_length=50, description="出发地"),
    arrival_city: str = Query(..., min_length=1, max_length=50, description="到达地"),
    travel_date: date = Query(..., description="出发日期"),
    db: Session = Depends(get_db)
):
    """
    查询车次
    
    - **departure_city**: 出发地（城市或车站名）
    - **arrival_city**: 到达地（城市或车站名）
    - **travel_date**: 出发日期（YYYY-MM-DD）
    
    实现车次查询逻辑:
    - 验证查询参数
    - 根据出发地和目的地查询车次
    - 计算余票数
    - 返回车次列表
    """
    # 验证查询参数
    CommonValidator.validate_non_empty_string(departure_city, "出发地")
    CommonValidator.validate_non_empty_string(arrival_city, "到达地")
    
    # 验证出发地和到达地不能相同
    if departure_city.strip() == arrival_city.strip():
        raise ValidationException("出发地和到达地不能相同")
    
    # 验证出发日期
    from datetime import date, timedelta
    today = date.today()
    max_date = today + timedelta(days=30)
    
    if travel_date < today:
        raise ValidationException("出发日期不能早于今天")
    if travel_date > max_date:
        raise ValidationException("最多只能查询30天内的车次")
    
    # TODO: 实现车次查询逻辑
    # - 查询车站信息
    # - 查询车次信息
    # - 计算余票数
    # - 构建响应数据
    
    # 临时返回空列表
    return Response(
        code=200,
        message="查询成功",
        data=[]
    )

