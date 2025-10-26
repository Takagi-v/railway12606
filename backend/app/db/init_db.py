"""
Database initialization
"""
from loguru import logger
from app.db.base import Base
from app.db.session import engine


def init_db() -> None:
    """
    Initialize database tables
    This should be called on application startup
    """
    try:
        Base.metadata.create_all(bind=engine)
        logger.info("Database tables created successfully")
    except Exception as e:
        logger.error(f"Error creating database tables: {e}")
        raise

