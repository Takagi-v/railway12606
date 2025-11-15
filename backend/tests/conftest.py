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


@pytest.fixture(scope="session")
def client():
    return TestClient(app)