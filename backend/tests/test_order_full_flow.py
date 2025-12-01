import pytest
from datetime import date, time, datetime
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from decimal import Decimal

from app.main import app
from app.db.base import Base
from app.api.deps import get_db, get_current_active_user
from app.models.user import User
from app.models.station import Station
from app.models.train import Train
from app.models.seat import Seat
from app.models.passenger import Passenger
from app.models.order import Order, OrderPassenger
from app.models.enums import (
    IdType, UserType, TrainType, SeatType, SeatStatus, PassengerType
)
from app.core.security import get_password_hash

from sqlalchemy.pool import StaticPool

# Setup test DB
SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"

@pytest.fixture(scope="module")
def test_db():
    engine = create_engine(
        SQLALCHEMY_DATABASE_URL, 
        connect_args={"check_same_thread": False},
        poolclass=StaticPool
    )
    TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    
    Base.metadata.create_all(bind=engine)
    
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()
        Base.metadata.drop_all(bind=engine)

@pytest.fixture(scope="module")
def client(test_db):
    def override_get_db():
        try:
            yield test_db
        finally:
            pass
            
    # Create test user
    user = User(
        username="test_user",
        password=get_password_hash("password"),
        real_name="Test User",
        id_type=IdType.ID_CARD.value,
        id_number="123456789012345678",
        phone="13800138000",
        user_type=UserType.ADULT.value
    )
    test_db.add(user)
    
    # Create test stations
    station_a = Station(station_name="Beijing", city="Beijing", pinyin="beijing", short_pinyin="bj")
    station_b = Station(station_name="Shanghai", city="Shanghai", pinyin="shanghai", short_pinyin="sh")
    test_db.add(station_a)
    test_db.add(station_b)
    test_db.commit() # Commit to get IDs
    
    # Create test train
    train = Train(
        train_number="G1",
        train_type=TrainType.HIGH_SPEED.value,
        departure_station_id=station_a.id,
        arrival_station_id=station_b.id,
        departure_time=time(8, 0),
        arrival_time=time(12, 0),
        duration_minutes=240,
        first_class_seats=10,
        second_class_seats=10,
        first_class_price=Decimal("100.00"),
        second_class_price=Decimal("50.00")
    )
    test_db.add(train)
    test_db.commit()
    
    # Create test seats
    for i in range(10):
        seat = Seat(
            train_id=train.id,
            travel_date=date.today(),
            seat_type=SeatType.SECOND_CLASS.value,
            seat_number=f"2-{i+1}A",
            status=SeatStatus.AVAILABLE.value
        )
        test_db.add(seat)
    test_db.commit()
    
    # Create test passenger
    passenger = Passenger(
        user_id=user.id,
        name="Passenger 1",
        id_type=IdType.ID_CARD.value,
        id_number="987654321098765432",
        phone="13900139000",
        passenger_type=PassengerType.ADULT.value
    )
    test_db.add(passenger)
    test_db.commit()
    
    from app.core.security import get_current_user
    from app.api.deps import get_db

    def override_get_current_user():
        return user

    app.dependency_overrides[get_db] = override_get_db
    app.dependency_overrides[get_current_user] = override_get_current_user
    
    from fastapi.responses import JSONResponse
    
    async def printing_handler(request, exc):
        print(f"CAUGHT EXCEPTION: {exc}")
        import traceback
        traceback.print_exc()
        return JSONResponse(status_code=500, content={"message": str(exc)})

    app.add_exception_handler(Exception, printing_handler)
    
    with TestClient(app) as c:
        yield c
    
    app.dependency_overrides.clear()

def test_create_and_get_order(client, test_db):
    # Prepare order data
    # We need the passenger ID
    passenger = test_db.query(Passenger).first()
    train = test_db.query(Train).first()
    
    order_data = {
        "train_id": train.id,
        "travel_date": str(date.today()),
        "passengers": [
            {
                "passenger_id": passenger.id,
                "ticket_type": PassengerType.ADULT.value,
                "seat_type": SeatType.SECOND_CLASS.value
            }
        ]
    }
    
    # 1. Create Order
    response = client.post("/api/orders/create", json=order_data)
    assert response.status_code == 201, f"Response: {response.text}"
    data = response.json()
    assert data["code"] == 201
    assert data["data"]["status"] == "待支付"
    order_id = data["data"]["id"]
    
    # 2. Get Order List
    response = client.get("/api/orders/")
    assert response.status_code == 200
    data = response.json()
    assert data["code"] == 200
    orders = data["data"]
    assert len(orders) >= 1
    found = False
    for order in orders:
        if order["id"] == order_id:
            found = True
            # Verify fix: check if station names are present
            assert order["departure_station"] == "Beijing"
            assert order["arrival_station"] == "Shanghai"
            break
    assert found
    
    # 3. Get Order Detail
    response = client.get(f"/api/orders/{order_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["code"] == 200
    order_detail = data["data"]
    assert order_detail["id"] == order_id
    # Verify fix again
    assert order_detail["departure_station"] == "Beijing"
    assert order_detail["arrival_station"] == "Shanghai"

def test_pay_and_cancel_order(client, test_db):
    # Setup: Create a new order first
    passenger = test_db.query(Passenger).first()
    train = test_db.query(Train).first()
    
    order_data = {
        "train_id": train.id,
        "travel_date": str(date.today()),
        "passengers": [
            {
                "passenger_id": passenger.id,
                "ticket_type": PassengerType.ADULT.value,
                "seat_type": SeatType.SECOND_CLASS.value
            }
        ]
    }
    
    # 1. Create Order for Payment
    response = client.post("/api/orders/create", json=order_data)
    assert response.status_code == 201
    order_id = response.json()["data"]["id"]
    
    # Pay Order
    response = client.post(f"/api/orders/{order_id}/pay", json={})
    assert response.status_code == 200
    assert response.json()["code"] == 200
    
    # Verify Status
    response = client.get(f"/api/orders/{order_id}")
    assert response.json()["data"]["status"] == "已支付"
    
    # 2. Create another order for Cancellation
    # We need another seat or reuse logic? 
    # The train has 10 seats. We used 2 so far (one in prev test, one above). 8 left.
    response = client.post("/api/orders/create", json=order_data)
    assert response.status_code == 201
    cancel_order_id = response.json()["data"]["id"]
    
    # Cancel Order
    response = client.post(f"/api/orders/{cancel_order_id}/cancel", json={})
    assert response.status_code == 200
    assert response.json()["code"] == 200
    
    # Verify Deletion - Expecting 404
    response = client.get(f"/api/orders/{cancel_order_id}")
    # Note: Depending on exception handler implementation, it might be 404 or 200 with code 404 in body.
    # Our NotFoundException sets self.code = 404.
    # If the handler returns JSONResponse(status_code=exc.code...), then it is 404.
    # Let's check logic: NotFoundException(404) -> business_exception_handler
    # If business_exception_handler uses exc.code as status_code, it is 404.
    # If it returns 200 OK with code=404 in body, then check body.
    # Based on http_exception_handler, it seems likely to follow status code.
    
    if response.status_code == 404:
        pass
    else:
        # If it returns 200, check the code in body
        assert response.json()["code"] == 404

def test_refund_order(client, test_db):
    # Setup: Create a new order
    passenger = test_db.query(Passenger).first()
    train = test_db.query(Train).first()
    
    order_data = {
        "train_id": train.id,
        "travel_date": str(date.today()),
        "passengers": [
            {
                "passenger_id": passenger.id,
                "ticket_type": PassengerType.ADULT.value,
                "seat_type": SeatType.SECOND_CLASS.value
            }
        ]
    }
    
    # 1. Create Order
    response = client.post("/api/orders/create", json=order_data)
    assert response.status_code == 201
    order_id = response.json()["data"]["id"]
    
    # 2. Pay Order
    response = client.post(f"/api/orders/{order_id}/pay", json={})
    assert response.status_code == 200
    
    # 3. Refund Order (All)
    response = client.post(f"/api/orders/{order_id}/refund", json={"passenger_ids": []})
    assert response.status_code == 200, f"Refund failed: {response.text}"
    data = response.json()
    assert data["code"] == 200
    assert data["data"]["order_status"] == "已退票"
    assert data["data"]["refunded_passengers"] == 1
    
    # Verify Status in DB
    response = client.get(f"/api/orders/{order_id}")
    assert response.json()["data"]["status"] == "已退票"
    # OrderDetailResponse returns passengers list, check refund_status
    passengers = response.json()["data"]["passengers"]
    assert passengers[0]["refund_status"] == "已退票"

def test_partial_refund_order(client, test_db):
    # Setup: Create an order with 2 passengers
    # We need another passenger
    user = test_db.query(User).filter(User.username == "test_user").first()
    
    # Check if passenger 2 exists
    passenger2 = test_db.query(Passenger).filter(Passenger.name == "Passenger 2").first()
    if not passenger2:
        passenger2 = Passenger(
            user_id=user.id,
            name="Passenger 2",
            id_type=IdType.ID_CARD.value,
            id_number="111111111111111111",
            phone="13900139002",
            passenger_type=PassengerType.ADULT.value
        )
        test_db.add(passenger2)
        test_db.commit()
    
    train = test_db.query(Train).first()
    passenger1 = test_db.query(Passenger).filter(Passenger.name == "Passenger 1").first()
    
    order_data = {
        "train_id": train.id,
        "travel_date": str(date.today()),
        "passengers": [
            {
                "passenger_id": passenger1.id,
                "ticket_type": PassengerType.ADULT.value,
                "seat_type": SeatType.SECOND_CLASS.value
            },
            {
                "passenger_id": passenger2.id,
                "ticket_type": PassengerType.ADULT.value,
                "seat_type": SeatType.SECOND_CLASS.value
            }
        ]
    }
    
    # 1. Create Order
    response = client.post("/api/orders/create", json=order_data)
    assert response.status_code == 201
    order_id = response.json()["data"]["id"]
    
    # 2. Pay Order
    response = client.post(f"/api/orders/{order_id}/pay", json={})
    assert response.status_code == 200
    
    # 3. Partial Refund (Passenger 1)
    response = client.post(f"/api/orders/{order_id}/refund", json={"passenger_ids": [passenger1.id]})
    assert response.status_code == 200, f"Partial refund failed: {response.text}"
    data = response.json()
    assert data["code"] == 200
    assert data["data"]["order_status"] == "部分退票"
    assert data["data"]["refunded_passengers"] == 1
    
    # Verify Status in DB
    response = client.get(f"/api/orders/{order_id}")
    order_detail = response.json()["data"]
    assert order_detail["status"] == "部分退票"
    
    # Check passenger statuses
    p1_status = next(p["refund_status"] for p in order_detail["passengers"] if p["id_number"] == passenger1.id_number)
    p2_status = next(p["refund_status"] for p in order_detail["passengers"] if p["id_number"] == passenger2.id_number)
    
    assert p1_status == "已退票"
    assert p2_status == "未退票"

