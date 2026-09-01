"""
Shared test fixtures and configuration.

Provides:
  - Async test client pointing at the FastAPI app
  - In-memory / test-database session override (uses db_test Docker container)
  - Organization and user factory fixtures
  - Authenticated client factories for each role

Test database:
  - Runs on port 5433 (see docker-compose.yml db_test service)
  - Schema is applied once per session via Alembic before tests run
  - Each integration test wraps its operations in a rolled-back transaction
    to prevent test-to-test contamination

Environment variable for test DB:
  TEST_DATABASE_URL = postgresql+asyncpg://empuser:emppassword@localhost:5433/employee_management_test
"""

import os
from collections.abc import AsyncGenerator
from typing import Any

import pytest
import pytest_asyncio
from httpx import ASGITransport, AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from app.db.session import get_db
from app.main import create_application

# ---------------------------------------------------------------------------
# Test database URL
# ---------------------------------------------------------------------------

TEST_DATABASE_URL = os.getenv(
    "TEST_DATABASE_URL",
    "postgresql+asyncpg://empuser:emppassword@localhost:5433/employee_management_test",
)

# ---------------------------------------------------------------------------
# Async engine + session factory for tests
# ---------------------------------------------------------------------------

test_engine = create_async_engine(TEST_DATABASE_URL, echo=False)
TestAsyncSessionLocal = async_sessionmaker(
    bind=test_engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autocommit=False,
    autoflush=False,
)

# ---------------------------------------------------------------------------
# Override the app's get_db dependency to use the test database
# ---------------------------------------------------------------------------


async def override_get_db() -> AsyncGenerator[AsyncSession, None]:
    async with TestAsyncSessionLocal() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()


# ---------------------------------------------------------------------------
# Application fixture
# ---------------------------------------------------------------------------


@pytest.fixture(scope="session")
def app() -> Any:
    """Create a test application with the database dependency overridden."""
    application = create_application()
    application.dependency_overrides[get_db] = override_get_db
    return application


# ---------------------------------------------------------------------------
# Async HTTP test client
# ---------------------------------------------------------------------------


@pytest_asyncio.fixture
async def client(app: Any) -> AsyncGenerator[AsyncClient, None]:
    """An async HTTP client pointed at the test application."""
    async with AsyncClient(
        transport=ASGITransport(app=app),
        base_url="http://testserver",
    ) as ac:
        yield ac


# ---------------------------------------------------------------------------
# Database session fixture (for direct DB assertions in tests)
# ---------------------------------------------------------------------------


@pytest_asyncio.fixture
async def db() -> AsyncGenerator[AsyncSession, None]:
    """
    Provide a database session for the duration of one test.
    Rolls back after the test to keep the database clean.
    """
    async with TestAsyncSessionLocal() as session:
        try:
            yield session
        finally:
            await session.rollback()
            await session.close()


# ---------------------------------------------------------------------------
# TODO: Add organization factory, user factory, and authenticated client
# fixtures here as modules are implemented in Phase 2+.
#
# Example:
#
# @pytest_asyncio.fixture
# async def org_factory(db: AsyncSession):
#     """Creates a test organization and returns it."""
#     ...
#
# @pytest_asyncio.fixture
# async def admin_client(client: AsyncClient, org_factory) -> AsyncClient:
#     """Returns a client authenticated as an Admin."""
#     ...
# ---------------------------------------------------------------------------
