"""
Order Endpoints
订单管理相关API
"""
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status, Path, Query
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.schemas.order import OrderCreate, OrderResponse, OrderDetailResponse, RefundRequest
from app.schemas.common import Response
from app.models.user import User
from app.core.security import get_current_user
from app.models.enums import OrderStatus
from app.core.exceptions import BusinessException, ValidationException, NotFoundException

router = APIRouter()


@router.post("/create", response_model=Response[OrderResponse], status_code=status.HTTP_201_CREATED)
async def create_order(
    order_data: OrderCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    创建订单
    
    - **train_id**: 车次ID
    - **travel_date**: 乘车日期
    - **passengers**: 乘客列表，每个乘客包含:
        - passenger_id: 乘客ID
        - ticket_type: 票种（成人票/学生票/儿童票）
        - seat_type: 席别（一等座/二等座/软卧/硬卧）
    
    实现订单创建逻辑:
    - 检查车次和日期有效性
    - 检查乘客信息
    - 锁定座位（45分钟）
    - 生成订单号
    - 计算总价
    """
    # 验证订单数据 (已通过Pydantic模型验证)
    # OrderValidator.validate_travel_date(order_data.travel_date)
    # OrderValidator.validate_passenger_count(len(order_data.passengers))
    
    # 检查车次是否存在
    from app.models.train import Train
    train = db.query(Train).filter(Train.id == order_data.train_id).first()
    if not train:
        raise NotFoundException("车次不存在")
    
    # 检查乘客是否都属于当前用户
    from app.models.passenger import Passenger
    passenger_ids = [p.passenger_id for p in order_data.passengers]
    passengers_db = db.query(Passenger).filter(
        Passenger.id.in_(passenger_ids),
        Passenger.user_id == current_user.id
    ).all()
    
    if len(passengers_db) != len(passenger_ids):
        raise ValidationException("部分乘客信息不存在或不属于当前用户")
    
    # 建立乘客ID到乘客对象的映射，方便后续获取信息
    passenger_map = {p.id: p for p in passengers_db}
    
    # 准备数据
    from app.models.seat import Seat
    from app.models.order import Order, OrderPassenger
    from app.models.enums import SeatStatus, SeatType
    from datetime import datetime, timedelta
    import random
    
    total_price = 0
    order_passengers_data = []
    seats_to_update = []
    
    # 开始事务处理
    try:
        for p_req in order_data.passengers:
            # 1. 确定票价
            price = 0
            if p_req.seat_type == SeatType.FIRST_CLASS:
                price = train.first_class_price
            elif p_req.seat_type == SeatType.SECOND_CLASS:
                price = train.second_class_price
            elif p_req.seat_type == SeatType.SOFT_SLEEPER:
                price = train.soft_sleeper_price
            elif p_req.seat_type == SeatType.HARD_SLEEPER:
                price = train.hard_sleeper_price
                
            if not price:
                raise ValidationException(f"该车次不支持{p_req.seat_type.value}")
                
            # 2. 查找可用座位 (使用悲观锁防止超卖)
            seat = db.query(Seat).filter(
                Seat.train_id == train.id,
                Seat.travel_date == order_data.travel_date,
                Seat.seat_type == p_req.seat_type,
                Seat.status == SeatStatus.AVAILABLE
            ).with_for_update(skip_locked=True).first()
            
            if not seat:
                raise BusinessException(f"{p_req.seat_type.value}余票不足")
                
            # 3. 锁定座位
            seat.status = SeatStatus.LOCKED
            seat.locked_until = datetime.now() + timedelta(minutes=45)
            seats_to_update.append(seat)
            
            # 4. 准备订单乘客数据
            total_price += price
            order_passengers_data.append({
                "passenger_id": p_req.passenger_id,
                "seat_id": seat.id,
                "ticket_type": p_req.ticket_type,
                "seat_type": p_req.seat_type,
                "price": price
            })
            
        # 5. 生成订单号 (时间戳 + 用户ID后4位 + 4位随机数)
        timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
        user_suffix = str(current_user.id).zfill(4)[-4:]
        random_suffix = str(random.randint(1000, 9999))
        order_number = f"{timestamp}{user_suffix}{random_suffix}"
        
        # 6. 创建订单
        new_order = Order(
            order_number=order_number,
            user_id=current_user.id,
            train_id=train.id,
            travel_date=order_data.travel_date,
            total_price=total_price,
            status=OrderStatus.PENDING
        )
        db.add(new_order)
        db.flush()  # 获取订单ID
        
        # 7. 创建订单乘客记录
        for op_data in order_passengers_data:
            order_passenger = OrderPassenger(
                order_id=new_order.id,
                passenger_id=op_data["passenger_id"],
                seat_id=op_data["seat_id"],
                ticket_type=op_data["ticket_type"],
                seat_type=op_data["seat_type"],
                price=op_data["price"]
            )
            db.add(order_passenger)
            
        db.commit()
        db.refresh(new_order)
        
        return Response(
            code=201,
            message="订单创建成功",
            data=OrderResponse.model_validate(new_order)
        )
        
    except Exception as e:
        db.rollback()
        raise e


@router.get("", response_model=Response[List[OrderResponse]])
async def get_orders(
    status: Optional[OrderStatus] = Query(None, description="订单状态筛选"),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    查询订单列表
    
    - **status**: 订单状态（可选）- 待支付/已支付/已取消/已退票（枚举）
    """
    from app.models.order import Order
    
    query = db.query(Order).filter(Order.user_id == current_user.id)
    
    if status:
        query = query.filter(Order.status == status)
        
    orders = query.order_by(Order.create_time.desc()).all()
    
    return Response(
        code=200,
        message="查询成功",
        data=[OrderResponse.model_validate(order) for order in orders]
    )


@router.get("/{order_id}", response_model=Response[OrderDetailResponse])
async def get_order_detail(
    order_id: int = Path(..., gt=0, description="订单ID"),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    查询订单详情
    """
    # 查询订单是否存在且属于当前用户
    from app.models.order import Order
    order = db.query(Order).filter(
        Order.id == order_id,
        Order.user_id == current_user.id
    ).first()
    
    if not order:
        from app.core.exceptions import NotFoundException
        raise NotFoundException("订单不存在")
    
    return Response(
        code=200,
        message="查询成功",
        data=OrderDetailResponse.model_validate(order)
    )


@router.post("/{order_id}/pay", response_model=Response)
async def pay_order(
    order_id: int = Path(..., gt=0, description="订单ID"),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    支付订单（简化实现）
    
    实现支付逻辑:
    - 检查订单状态
    - 更新订单状态为已支付
    - 确认座位占用
    - 记录支付时间
    """
    # 查询订单
    from app.models.order import Order
    order = db.query(Order).filter(
        Order.id == order_id,
        Order.user_id == current_user.id
    ).first()
    
    if not order:
        raise NotFoundException("订单不存在")
    
    # 检查订单状态
    if order.status != OrderStatus.PENDING:
        raise BusinessException(f"订单状态不允许支付: {order.status.value}")
    
    from datetime import datetime
    from app.models.enums import SeatStatus
    from app.models.seat import Seat

    try:
        # 更新订单状态
        order.status = OrderStatus.PAID
        order.pay_time = datetime.now()

        # 获取所有关联座位并更新状态为已售
        seat_ids = [op.seat_id for op in order.order_passengers]
        if seat_ids:
            db.query(Seat).filter(Seat.id.in_(seat_ids)).update(
                {Seat.status: SeatStatus.SOLD}, 
                synchronize_session=False
            )

        db.commit()
        db.refresh(order)

        return Response(
            code=200,
            message="支付成功",
            data={}
        )

    except Exception as e:
        db.rollback()
        raise e


@router.post("/{order_id}/cancel", response_model=Response)
async def cancel_order(
    order_id: int = Path(..., gt=0, description="订单ID"),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    取消订单
    
    实现取消订单逻辑:
    - 检查订单状态（只能取消待支付订单）
    - 释放座位
    - 更新订单状态
    """
    # 查询订单
    from app.models.order import Order
    order = db.query(Order).filter(
        Order.id == order_id,
        Order.user_id == current_user.id
    ).first()
    
    if not order:
        raise NotFoundException("订单不存在")
    
    # 检查订单状态
    if order.status != OrderStatus.PENDING:
        raise BusinessException("只能取消待支付的订单")
    
    from app.models.enums import SeatStatus
    from app.models.seat import Seat

    try:
        # 释放座位
        seat_ids = [op.seat_id for op in order.order_passengers]
        if seat_ids:
            # 将座位状态重置为可售，并清除锁定时间
            db.query(Seat).filter(Seat.id.in_(seat_ids)).update(
                {
                    Seat.status: SeatStatus.AVAILABLE,
                    Seat.locked_until: None
                }, 
                synchronize_session=False
            )
        
        # 删除订单 (级联删除 OrderPassenger)
        db.delete(order)
        db.commit()

        return Response(
            code=200,
            message="订单已取消",
            data={}
        )

    except Exception as e:
        db.rollback()
        raise e


@router.post("/{order_id}/refund", response_model=Response)
async def refund_order(
    order_id: int = Path(..., gt=0, description="订单ID"),
    refund_data: RefundRequest = RefundRequest(),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    退票
    
    - **passenger_ids**: 要退票的乘客ID列表（空列表表示全部退票）
    
    实现退票逻辑:
    - 检查订单状态
    - 验证乘客信息
    - 计算退票手续费
    - 释放座位
    - 更新订单状态
    - 记录退款信息
    """
    # 查询订单
    from app.models.order import Order, OrderPassenger
    from app.models.seat import Seat
    from app.models.enums import OrderStatus, RefundStatus, SeatStatus
    from datetime import datetime

    # Use pessimistic locking to prevent race conditions
    order = db.query(Order).filter(
        Order.id == order_id,
        Order.user_id == current_user.id
    ).with_for_update().first()
    
    if not order:
        raise NotFoundException("订单不存在")
    
    # 检查订单状态
    allowed_statuses = [OrderStatus.PAID, OrderStatus.PARTIALLY_REFUNDED]
    allowed_status_values = [s.value for s in allowed_statuses]
    
    # Allow matching either Enum member or string value
    if order.status not in allowed_statuses and order.status not in allowed_status_values:
        raise BusinessException("订单状态不允许退票")
    
    # 确定要退票的乘客
    passengers_to_refund = []
    
    if not refund_data.passenger_ids:
        # 如果未指定乘客ID，默认退该订单下所有未退票的乘客
        passengers_to_refund = [
            p for p in order.order_passengers 
            if p.refund_status == RefundStatus.NOT_REFUNDED or p.refund_status == RefundStatus.NOT_REFUNDED.value
        ]
    else:
        # 验证并筛选指定的乘客
        requested_ids = set(refund_data.passenger_ids)
        # Assuming refund_data.passenger_ids refers to the Passenger table IDs (p.passenger_id)
        # logic: find OrderPassenger entries where passenger_id matches
        
        found_count = 0
        for p in order.order_passengers:
            if p.passenger_id in requested_ids:
                found_count += 1
                if p.refund_status != RefundStatus.NOT_REFUNDED and p.refund_status != RefundStatus.NOT_REFUNDED.value:
                    raise BusinessException(f"乘客 {p.passenger.name} 已退票")
                passengers_to_refund.append(p)
        
        if found_count != len(requested_ids):
             # Some requested IDs were not found in this order
             raise ValidationException("部分乘客ID无效或不属于该订单")
    
    if not passengers_to_refund:
        raise BusinessException("没有可退票的乘客")

    try:
        current_time = datetime.now()
        total_refund_amount = 0.0
        
        for p in passengers_to_refund:
            # 1. 释放座位
            if p.seat_id:
                seat = db.query(Seat).get(p.seat_id)
                if seat:
                    seat.status = SeatStatus.AVAILABLE
                    seat.locked_until = None
            
            # 2. 计算退款金额 (模拟逻辑: 收取5%手续费)
            # p.price is Decimal
            ticket_price = float(p.price) if p.price else 0.0
            refund_amount = round(ticket_price * 0.95, 2)
            total_refund_amount += refund_amount
            
            # 3. 更新乘客退票信息
            p.refund_status = RefundStatus.REFUNDED
            p.refund_time = current_time
            p.refund_amount = refund_amount
            
        # 4. 更新订单状态
        # 检查是否所有乘客都已退票
        all_refunded = all(
            (p.refund_status == RefundStatus.REFUNDED or p.refund_status == RefundStatus.REFUNDED.value)
            for p in order.order_passengers
        )
        
        if all_refunded:
            order.status = OrderStatus.REFUNDED
        else:
            order.status = OrderStatus.PARTIALLY_REFUNDED
            
        db.commit()
        
        return Response(
            code=200,
            message=f"退票成功，共退款 {total_refund_amount} 元",
            data={
                "order_id": order.id,
                "refund_amount": total_refund_amount,
                "refunded_passengers": len(passengers_to_refund),
                "order_status": order.status.value if hasattr(order.status, 'value') else order.status
            }
        )
        
    except Exception as e:
        db.rollback()
        raise e

