import os
import pytest
from fastapi.testclient import TestClient


# Minimal environment for Settings
os.environ.setdefault("DATABASE_URL", "postgresql://user:pass@localhost:5432/db")
os.environ.setdefault("POSTGRES_USER", "user")
os.environ.setdefault("POSTGRES_PASSWORD", "pass")
os.environ.setdefault("POSTGRES_DB", "db")
os.environ.setdefault("SECRET_KEY", "test-secret-key")
os.environ.setdefault("API_PREFIX", "/api/v1")


from app.main import app
from app.core.security import get_current_user


@pytest.fixture(scope="session")
def client():
    return TestClient(app)


@pytest.fixture(scope="session", autouse=True)
def _override_auth():
    def fake_current_user():
        class U:
            id = 1
            username = "tester"
            real_name = "测试用户"
            phone = "13800138000"
            email = "user@example.com"
        return U()
    app.dependency_overrides[get_current_user] = fake_current_user
    yield
    app.dependency_overrides.clear()