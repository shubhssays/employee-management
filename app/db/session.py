"""
Database engine, session factory, and get_db dependency.

Architecture decisions:
  - Async engine (asyncpg driver) — required for FastAPI's async handlers.
  - One AsyncSession per HTTP request — created by get_db and never shared
    across requests.
  - Transaction boundaries are explicitly controlled by the service layer.
  - Repositories never commit or rollback transactions.
  - Connection pooling is handled by SQLAlchemy in production.
  - Tests can use a different engine/pool configuration.

Transaction ownership:

    Router
      ↓
    Service
      ↓
    async with db.begin():
        ↓
      Repository
      Repository
      Repository
        ↓
    commit / rollback

Usage in route handlers:
    from app.core.dependencies import DbSession

    async def my_route(db: DbSession) -> ...:
        ...

Usage in services:
    class MyService:
        def __init__(self, db: AsyncSession) -> None:
            self.db = db

        async def create_something(self) -> ...:
            async with self.db.begin():
                ...
"""

from collections.abc import AsyncGenerator

from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

from app.core.config import settings

# ---------------------------------------------------------------------------
# Engine
# ---------------------------------------------------------------------------

engine = create_async_engine(
    settings.DATABASE_URL,
    echo=settings.DATABASE_ECHO,
    pool_size=settings.DATABASE_POOL_SIZE,
    max_overflow=settings.DATABASE_MAX_OVERFLOW,
    pool_pre_ping=True,
)

# ---------------------------------------------------------------------------
# Session factory
# ---------------------------------------------------------------------------

AsyncSessionLocal = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autoflush=False,
)

# ---------------------------------------------------------------------------
# FastAPI dependency
# ---------------------------------------------------------------------------


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """
    Provide one AsyncSession for the lifetime of an HTTP request.

    This dependency intentionally does NOT commit or rollback.

    Transaction boundaries belong to the service/business-operation layer.

    Example:

        async def create_organization(
            self,
            data: OrganizationCreate,
        ) -> Organization:
            async with self.db.begin():
                organization = await self.organization_repo.create(data)
                member = await self.member_repo.create(
                    organization_id=organization.id,
                )

            # Transaction has been committed here.

            await send_email()

            return organization

    If an exception occurs inside `db.begin()`, SQLAlchemy automatically
    rolls the transaction back.

    The session itself is always closed when the request finishes.
    """
    async with AsyncSessionLocal() as session:
        yield session