"""
Generate demo data for Railway 12306 backend
创建演示数据：站点、车次、指定天数的日历座位

Usage:
    source .venv/bin/activate
    python backend/scripts/generate_demo_data.py --days 14

Options:
    --days N        生成从今天起 N 天的座位数据（默认 7）
    --start YYYY-MM-DD  指定开始日期（默认今天）

该脚本幂等：
- 站点按名称存在即跳过
- 车次按车次号存在即更新基础信息
- 座位按 (train_id, travel_date, seat_type) 已存在则跳过生成
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path
from datetime import date, datetime, timedelta, time
from typing import List, Tuple

from sqlalchemy.orm import Session

# Ensure `backend` directory is on sys.path no matter where the script is launched.
BACKEND_DIR = Path(__file__).resolve().parents[1]
if str(BACKEND_DIR) not in sys.path:
    sys.path.insert(0, str(BACKEND_DIR))

from app.db.session import SessionLocal
from app.models.station import Station
from app.models.train import Train
from app.models.seat import Seat
from app.models.enums import TrainType, SeatType, SeatStatus


def ensure_station(db: Session, name: str, city: str, pinyin: str, short_pinyin: str) -> Station:
    st = db.query(Station).filter(Station.station_name == name).first()
    if st:
        return st
    st = Station(station_name=name, city=city, pinyin=pinyin, short_pinyin=short_pinyin)
    db.add(st)
    db.commit()
    db.refresh(st)
    return st


def ensure_train(
    db: Session,
    train_number: str,
    train_type: TrainType,
    depart_station: Station,
    arrive_station: Station,
    depart_time: time,
    arrive_time: time,
    duration_minutes: int,
    first_count: int,
    second_count: int,
    soft_count: int,
    hard_count: int,
    first_price: float,
    second_price: float,
    soft_price: float,
    hard_price: float,
) -> Train:
    tr = db.query(Train).filter(Train.train_number == train_number).first()
    if tr:
        # 更新基础信息（幂等）
        tr.train_type = train_type
        tr.departure_station_id = depart_station.id
        tr.arrival_station_id = arrive_station.id
        tr.departure_time = depart_time
        tr.arrival_time = arrive_time
        tr.duration_minutes = duration_minutes
        tr.first_class_seats = first_count
        tr.second_class_seats = second_count
        tr.soft_sleeper_seats = soft_count
        tr.hard_sleeper_seats = hard_count
        tr.first_class_price = first_price
        tr.second_class_price = second_price
        tr.soft_sleeper_price = soft_price
        tr.hard_sleeper_price = hard_price
        db.commit()
        db.refresh(tr)
        return tr

    tr = Train(
        train_number=train_number,
        train_type=train_type,
        departure_station_id=depart_station.id,
        arrival_station_id=arrive_station.id,
        departure_time=depart_time,
        arrival_time=arrive_time,
        duration_minutes=duration_minutes,
        first_class_seats=first_count,
        second_class_seats=second_count,
        soft_sleeper_seats=soft_count,
        hard_sleeper_seats=hard_count,
        first_class_price=first_price,
        second_class_price=second_price,
        soft_sleeper_price=soft_price,
        hard_sleeper_price=hard_price,
    )
    db.add(tr)
    db.commit()
    db.refresh(tr)
    return tr


def seats_exist_for(db: Session, train_id: int, d: date) -> bool:
    return db.query(Seat.id).filter(Seat.train_id == train_id, Seat.travel_date == d).first() is not None


def gen_seat_numbers(prefix: str, count: int) -> List[str]:
    # 简单生成座位号：车厢-座位序号，如 01-001
    numbers: List[str] = []
    carriage_capacity = 60  # 每车厢约 60 个座位
    carriage = 1
    idx_in_carriage = 1
    for i in range(count):
        numbers.append(f"{carriage:02d}-{idx_in_carriage:03d}")
        idx_in_carriage += 1
        if idx_in_carriage > carriage_capacity:
            carriage += 1
            idx_in_carriage = 1
    return numbers


def create_daily_seats(db: Session, train: Train, d: date) -> None:
    if seats_exist_for(db, train.id, d):
        return

    # 生成各席别座位
    def add_seats(seat_type: SeatType, count: int):
        if count <= 0:
            return
        for seat_no in gen_seat_numbers(seat_type.name[:1], count):
            db.add(
                Seat(
                    train_id=train.id,
                    travel_date=d,
                    seat_type=seat_type,
                    seat_number=seat_no,
                    status=SeatStatus.AVAILABLE,
                    locked_until=None,
                )
            )

    add_seats(SeatType.FIRST_CLASS, train.first_class_seats or 0)
    add_seats(SeatType.SECOND_CLASS, train.second_class_seats or 0)
    add_seats(SeatType.SOFT_SLEEPER, train.soft_sleeper_seats or 0)
    add_seats(SeatType.HARD_SLEEPER, train.hard_sleeper_seats or 0)
    db.commit()


def main():
    parser = argparse.ArgumentParser(description="Generate demo data for stations, trains, and seats")
    parser.add_argument("--days", type=int, default=7, help="生成多少天的座位数据")
    parser.add_argument("--start", type=str, default=date.today().isoformat(), help="开始日期 YYYY-MM-DD")
    args = parser.parse_args()

    start_date = datetime.strptime(args.start, "%Y-%m-%d").date()
    days = max(1, args.days)

    db: Session = SessionLocal()
    try:
        # === 站点 ===
        bj_nan = ensure_station(db, "北京南", "北京", "beijingnan", "bjn")
        sh_hq = ensure_station(db, "上海虹桥", "上海", "shanghaihongqiao", "shhq")
        nj_nan = ensure_station(db, "南京南", "南京", "nanjingnan", "njn")
        hz_dong = ensure_station(db, "杭州东", "杭州", "hangzhoudong", "hzd")
        gz_nan = ensure_station(db, "广州南", "广州", "guangzhounan", "gzn")
        sz_bei = ensure_station(db, "深圳北", "深圳", "shenzhenbei", "szb")

        # === 车次 ===
        g1234 = ensure_train(
            db,
            train_number="G1234",
            train_type=TrainType.HIGH_SPEED,
            depart_station=bj_nan,
            arrive_station=sh_hq,
            depart_time=time(8, 0),
            arrive_time=time(12, 30),
            duration_minutes=270,
            first_count=40,
            second_count=200,
            soft_count=32,
            hard_count=60,
            first_price=560.0,
            second_price=350.0,
            soft_price=650.0,
            hard_price=480.0,
        )

        d5678 = ensure_train(
            db,
            train_number="D5678",
            train_type=TrainType.BULLET,
            depart_station=bj_nan,
            arrive_station=nj_nan,
            depart_time=time(9, 15),
            arrive_time=time(12, 0),
            duration_minutes=165,
            first_count=30,
            second_count=180,
            soft_count=20,
            hard_count=40,
            first_price=420.0,
            second_price=260.0,
            soft_price=520.0,
            hard_price=360.0,
        )

        g2345 = ensure_train(
            db,
            train_number="G2345",
            train_type=TrainType.HIGH_SPEED,
            depart_station=sh_hq,
            arrive_station=hz_dong,
            depart_time=time(10, 30),
            arrive_time=time(11, 40),
            duration_minutes=70,
            first_count=24,
            second_count=100,
            soft_count=16,
            hard_count=30,
            first_price=220.0,
            second_price=120.0,
            soft_price=280.0,
            hard_price=200.0,
        )

        # 实验车次（广州南-深圳北）
        x9012 = ensure_train(
            db,
            train_number="X9012",
            train_type=TrainType.BULLET,
            depart_station=gz_nan,
            arrive_station=sz_bei,
            depart_time=time(7, 45),
            arrive_time=time(9, 10),
            duration_minutes=85,
            first_count=50,
            second_count=220,
            soft_count=30,
            hard_count=50,
            first_price=320.0,
            second_price=180.0,
            soft_price=380.0,
            hard_price=260.0,
        )

        # === 日历座位 ===
        trains: List[Train] = [g1234, d5678, g2345, x9012]
        for i in range(days):
            d = start_date + timedelta(days=i)
            for tr in trains:
                create_daily_seats(db, tr, d)

        print(f"✅ Demo data generated: stations={4}, trains={len(trains)}, days={days}")
    finally:
        db.close()


if __name__ == "__main__":
    main()