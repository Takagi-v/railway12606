"""
Train Endpoints
车次查询相关API
"""
from typing import List, Dict, Optional
from datetime import date, datetime
from fastapi import APIRouter, Depends, Query, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import or_, func

from app.db.session import get_db
from app.schemas.train import TrainSearchResponse, TrainDetailResponse, SeatAvailability, TrainAvailabilityResponse
from app.schemas.common import Response
from app.models.station import Station
from app.models.train import Train
from app.models.seat import Seat
from app.models.enums import SeatType, SeatStatus

router = APIRouter()


def _format_duration(minutes: int) -> str:
    hours = minutes // 60
    mins = minutes % 60
    if hours and mins:
        return f"{hours}小时{mins}分"
    if hours:
        return f"{hours}小时"
    return f"{mins}分"


def _seat_availability_by_type(db: Session, train_id: int, travel_date: date) -> Dict[SeatType, int]:
    """Return available seat counts per type for a given train and date."""
    counts: Dict[SeatType, int] = {}
    for st in [
        SeatType.FIRST_CLASS,
        SeatType.SECOND_CLASS,
        SeatType.SOFT_SLEEPER,
        SeatType.HARD_SLEEPER,
    ]:
        cnt = (
            db.query(func.count(Seat.id))
            .filter(
                Seat.train_id == train_id,
                Seat.travel_date == travel_date,
                Seat.seat_type == st,
                Seat.status == SeatStatus.AVAILABLE,
            )
            .scalar()
        )
        counts[st] = int(cnt or 0)
    return counts


@router.get("/search", response_model=Response[List[TrainSearchResponse]])
async def search_trains(
    departure_city: str = Query(..., description="出发地（城市或车站名/拼音）"),
    arrival_city: str = Query(..., description="到达地（城市或车站名/拼音）"),
    travel_date: date = Query(..., description="出发日期"),
    # 筛选项
    train_type: Optional[str] = Query(None, description="车次类型：高铁/动车/直达"),
    min_departure_time: Optional[str] = Query(None, description="最早出发时间 HH:MM"),
    max_departure_time: Optional[str] = Query(None, description="最晚出发时间 HH:MM"),
    min_duration_minutes: Optional[int] = Query(None, description="最短历时（分钟）"),
    max_duration_minutes: Optional[int] = Query(None, description="最长历时（分钟）"),
    max_price: Optional[float] = Query(None, description="最高票价（按二等座或最低价格）"),
    # 排序项：departure_time/duration/price，asc/desc
    sort_by: Optional[str] = Query(None, description="排序字段：departure_time/duration/price"),
    sort_order: Optional[str] = Query("asc", description="排序方向：asc/desc"),
    db: Session = Depends(get_db),
):
    """
    查询车次

    - **departure_city**: 出发地（城市或车站名/拼音/简拼，模糊匹配）
    - **arrival_city**: 到达地（城市或车站名/拼音/简拼，模糊匹配）
    - **travel_date**: 出发日期（YYYY-MM-DD）
    """
    # 查找匹配的出发/到达站
    departure_stations = (
        db.query(Station)
        .filter(
            or_(
                Station.station_name.ilike(f"%{departure_city}%"),
                Station.city.ilike(f"%{departure_city}%"),
                Station.pinyin.ilike(f"%{departure_city}%"),
                Station.short_pinyin.ilike(f"%{departure_city}%"),
            )
        )
        .all()
    )
    arrival_stations = (
        db.query(Station)
        .filter(
            or_(
                Station.station_name.ilike(f"%{arrival_city}%"),
                Station.city.ilike(f"%{arrival_city}%"),
                Station.pinyin.ilike(f"%{arrival_city}%"),
                Station.short_pinyin.ilike(f"%{arrival_city}%"),
            )
        )
        .all()
    )

    if not departure_stations or not arrival_stations:
        return Response(code=200, message="查询成功", data=[])

    departure_ids = [s.id for s in departure_stations]
    arrival_ids = [s.id for s in arrival_stations]

    # 查找符合路线的车次
    query = (
        db.query(Train)
        .filter(
            Train.departure_station_id.in_(departure_ids),
            Train.arrival_station_id.in_(arrival_ids),
        )
    )

    # 过滤：车次类型
    if train_type:
        query = query.filter(Train.train_type == train_type)

    # 过滤：出发时间范围
    if min_departure_time:
        try:
            min_time = datetime.strptime(min_departure_time, "%H:%M").time()
            query = query.filter(Train.departure_time >= min_time)
        except ValueError:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="min_departure_time 格式应为 HH:MM")
    if max_departure_time:
        try:
            max_time = datetime.strptime(max_departure_time, "%H:%M").time()
            query = query.filter(Train.departure_time <= max_time)
        except ValueError:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="max_departure_time 格式应为 HH:MM")

    # 过滤：历时范围
    if min_duration_minutes is not None:
        query = query.filter(Train.duration_minutes >= min_duration_minutes)
    if max_duration_minutes is not None:
        query = query.filter(Train.duration_minutes <= max_duration_minutes)

    trains = query.all()

    results: List[TrainSearchResponse] = []
    for t in trains:
        # 计算各席别余票
        avail = _seat_availability_by_type(db, t.id, travel_date)

        # train_type 统一转为字符串
        train_type_str = getattr(t.train_type, "value", str(t.train_type))

        results.append(
            TrainSearchResponse(
                train_id=t.id,
                train_number=t.train_number,
                train_type=train_type_str,
                departure_station=t.departure_station.station_name,
                arrival_station=t.arrival_station.station_name,
                departure_time=t.departure_time.strftime("%H:%M"),
                arrival_time=t.arrival_time.strftime("%H:%M"),
                duration=_format_duration(t.duration_minutes),
                first_class=SeatAvailability(
                    available=avail[SeatType.FIRST_CLASS],
                    price=t.first_class_price,
                ),
                second_class=SeatAvailability(
                    available=avail[SeatType.SECOND_CLASS],
                    price=t.second_class_price,
                ),
                soft_sleeper=SeatAvailability(
                    available=avail[SeatType.SOFT_SLEEPER],
                    price=t.soft_sleeper_price,
                ),
                hard_sleeper=SeatAvailability(
                    available=avail[SeatType.HARD_SLEEPER],
                    price=t.hard_sleeper_price,
                ),
            )
        )

    # 价格过滤与排序相关准备：选用最低价格（四种席别中的最低值）
    def lowest_price(t: Train):
        return min(
            [
                float(t.first_class_price or 0),
                float(t.second_class_price or 0),
                float(t.soft_sleeper_price or 0),
                float(t.hard_sleeper_price or 0),
            ]
        )

    if max_price is not None:
        results = [r for r in results if lowest_price(next(t for t in trains if t.id == r.train_id)) <= max_price]

    if sort_by in {"departure_time", "duration", "price"}:
        reverse = (sort_order or "asc").lower() == "desc"
        if sort_by == "departure_time":
            results.sort(key=lambda r: r.departure_time, reverse=reverse)
        elif sort_by == "duration":
            # 将“X小时Y分”转为分钟以排序
            def duration_to_minutes(s: str) -> int:
                h, m = 0, 0
                if "小时" in s:
                    parts = s.split("小时")
                    h = int(parts[0])
                    if "分" in parts[1]:
                        m = int(parts[1].replace("分", ""))
                else:
                    m = int(s.replace("分", ""))
                return h * 60 + m
            results.sort(key=lambda r: duration_to_minutes(r.duration), reverse=reverse)
        elif sort_by == "price":
            results.sort(
                key=lambda r: min([
                    float(r.first_class.price or 0),
                    float(r.second_class.price or 0),
                    float(r.soft_sleeper.price or 0),
                    float(r.hard_sleeper.price or 0),
                ]),
                reverse=reverse,
            )

    return Response(code=200, message="查询成功", data=results)


@router.get("/{train_number}", response_model=Response[TrainDetailResponse])
async def get_train_detail(train_number: str, db: Session = Depends(get_db)):
    """根据车次号获取车次详情"""
    train = db.query(Train).filter(Train.train_number == train_number).first()
    if not train:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="车次不存在")

    # 统一 train_type 为字符串以便展示
    # 使用 Pydantic 的 from_attributes 直接序列化
    detail = TrainDetailResponse.model_validate(train)

    # 将 Enum 显示为字符串（如果需要）
    detail.train_type = getattr(train.train_type, "value", str(train.train_type))

    return Response(code=200, message="查询成功", data=detail)


@router.get("/{train_number}/availability", response_model=Response[TrainAvailabilityResponse])
async def get_train_availability(
    train_number: str,
    date: date = Query(..., description="乘车日期 YYYY-MM-DD"),
    db: Session = Depends(get_db),
):
    """按日期返回车次各席别余票与价格"""
    train = db.query(Train).filter(Train.train_number == train_number).first()
    if not train:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="车次不存在")

    avail = _seat_availability_by_type(db, train.id, date)
    resp = TrainAvailabilityResponse(
        first_class=SeatAvailability(available=avail[SeatType.FIRST_CLASS], price=train.first_class_price),
        second_class=SeatAvailability(available=avail[SeatType.SECOND_CLASS], price=train.second_class_price),
        soft_sleeper=SeatAvailability(available=avail[SeatType.SOFT_SLEEPER], price=train.soft_sleeper_price),
        hard_sleeper=SeatAvailability(available=avail[SeatType.HARD_SLEEPER], price=train.hard_sleeper_price),
    )
    return Response(code=200, message="查询成功", data=resp)

