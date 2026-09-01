"""
Database engine, session factory, and get_db dependency.

Architecture decisions:
  - Async engine (asyncpg driver) — required for FastAPI's async handlers.
  - One session per HTTP request — created by get_db, committed/rolled
    back by the context manager, never shared across requests.
  - Connection pooling via SQLAlchemy's NullPool in tests and QueuePool
    in production (configured via DATABASE_POOL_SIZE).

Usage in route handlers:
    from app.core.dependencies import DbSession

    async def my_route(db: DbSession) -> ...:
        ...

Usage in services (passed from router via dependency injection):
    class MyService:
        def __init__(self, db: AsyncSession) -> None:
            self.db = db
"""

from collections.abc import AsyncGenerator

from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

from app.core.config import settings
from app.core.logging import get_logger

logger = get_logger(__name__)

# ---------------------------------------------------------------------------
# Engine
# ---------------------------------------------------------------------------

engine = create_async_engine(
    settings.DATABASE_URL,
    echo=settings.DATABASE_ECHO,
    pool_size=settings.DATABASE_POOL_SIZE,
    max_overflow=settings.DATABASE_MAX_OVERFLOW,
    pool_pre_ping=True,  # Verify connections are alive before using them
)

# ---------------------------------------------------------------------------
# Session factory
# ---------------------------------------------------------------------------

AsyncSessionLocal = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,  # Objects remain usable after commit (no lazy-load surprises)
    autocommit=False,
    autoflush=False,
)

# ---------------------------------------------------------------------------
# FastAPI dependency
# ---------------------------------------------------------------------------


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """
    Yield an async database session for the duration of one HTTP request.

    Commits on success; rolls back on any exception.
    Always closes the session when the request is done.

    Inject into route handlers via:
        from app.core.dependencies import DbSession
    """
    async with AsyncSessionLocal() as session:
        try:
            yield session
            await session.commit()
        except SQLAlchemyError as exc:
            await session.rollback()
            logger.error("Database error — rolling back transaction", exc_info=exc)
            raise
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()
