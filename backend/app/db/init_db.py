"""
Database initialization
"""
from loguru import logger
from app.db.base import Base
from app.db.session import engine
from sqlalchemy import inspect
from sqlalchemy.sql import text


def init_db() -> None:
    """
    Initialize database tables
    This should be called on application startup
    """
    try:
        Base.metadata.create_all(bind=engine)
        logger.info("Database tables created successfully")
        # Ensure missing columns exist for legacy SQLite databases
        try:
            inspector = inspect(engine)
            cols = {c['name'] for c in inspector.get_columns('passengers')}
            missing_alters = []
            if 'is_default' not in cols:
                missing_alters.append("ALTER TABLE passengers ADD COLUMN is_default BOOLEAN DEFAULT 0")
            # Apply required ALTER statements
            if missing_alters:
                with engine.begin() as conn:
                    for ddl in missing_alters:
                        conn.exec_driver_sql(ddl)
                logger.info("Applied schema fixes: %s", ", ".join(missing_alters))
        except Exception as ie:
            logger.warning(f"Schema inspection/patch failed: {ie}")
    except Exception as e:
        logger.error(f"Error creating database tables: {e}")
        raise
