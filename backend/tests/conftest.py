import pytest
from fastapi import FastAPI, Depends
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session

from app.api.v1.endpoints import password_recovery
from app.db.base import Base
from app.models.user import User
from app.models.enums import IdType, UserType
from app.core.security import get_password_hash


def create_test_session():
    engine = create_engine('sqlite://', connect_args={"check_same_thread": False})
    TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    Base.metadata.create_all(bind=engine)
    return engine, TestingSessionLocal


@pytest.fixture
def app_client():
    engine, TestingSessionLocal = create_test_session()

    def override_get_db() -> Session:
        db = TestingSessionLocal()
        try:
            yield db
        finally:
            db.close()

    app = FastAPI()
    app.include_router(password_recovery.router, prefix='/api')
    app.dependency_overrides[password_recovery.get_db] = override_get_db

    db = TestingSessionLocal()
    u = User(
        username='testuser',
        password=get_password_hash('Pass1234'),
        real_name='测试用户',
        id_type=IdType.ID_CARD.value,
        id_number='11010519491231002X',
        phone='15500000000',
        email='test@example.com',
        user_type=UserType.ADULT.value,
        is_active=1
    )
    db.add(u)
    db.commit()
    db.refresh(u)
    db.close()

    client = TestClient(app)
    return client

