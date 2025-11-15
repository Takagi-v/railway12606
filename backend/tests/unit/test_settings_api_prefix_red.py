from app.core.config import settings


def test_api_prefix_should_be_v1():
    assert settings.API_PREFIX == "/api/v1"