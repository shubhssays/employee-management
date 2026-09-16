from sqlalchemy.ext.asyncio import (
    create_async_engine,
)

from app.core.config import settings

worker_db_engine = create_async_engine(
    settings.DATABASE_URL,
    pool_size=3,
    max_overflow=5,
    pool_pre_ping=True,
    pool_recycle=180,  # 3 mins ideal timeout
)
