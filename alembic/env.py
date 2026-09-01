"""
Alembic migration environment.

This module is invoked by every Alembic command.

Key responsibilities:
  1. Load the database URL from app settings (never from alembic.ini directly).
  2. Import all ORM models via app/db/base.py so autogenerate can detect schema changes.
  3. Support both online (direct DB) and offline (SQL script generation) migration modes.
  4. Use async engine to match the application's async SQLAlchemy setup.

Adding a new model:
  → Import it in app/db/base.py (not here).
  → Run: uv run alembic revision --autogenerate -m "describe_change"
  → Review the generated file in alembic/versions/
  → Apply: uv run alembic upgrade head
"""

import asyncio
from logging.config import fileConfig

from alembic import context
from sqlalchemy.ext.asyncio import create_async_engine

# ---------------------------------------------------------------------------
# Load application settings (database URL, etc.)
# ---------------------------------------------------------------------------
from app.core.config import settings

# ---------------------------------------------------------------------------
# Import all models via the registry so autogenerate sees the full schema.
# DO NOT import models directly here — add them to app/db/base.py instead.
# ---------------------------------------------------------------------------
from app.db.base import Base  # noqa: F401 — side-effect import registers all models

# ---------------------------------------------------------------------------
# Alembic Config object (gives access to alembic.ini values)
# ---------------------------------------------------------------------------
config = context.config

# Configure Python logging from the alembic.ini [loggers] section
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# The metadata object used by autogenerate to compare against the live DB
target_metadata = Base.metadata


# ---------------------------------------------------------------------------
# Offline migration mode
# (generates SQL scripts without connecting to the database)
# ---------------------------------------------------------------------------

def run_migrations_offline() -> None:
    """
    Run migrations in 'offline' mode.

    Generates SQL scripts without a live database connection.
    Useful for reviewing migrations before applying or for air-gapped deployments.
    """
    context.configure(
        url=settings.DATABASE_URL,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
        compare_type=True,
    )

    with context.begin_transaction():
        context.run_migrations()


# ---------------------------------------------------------------------------
# Online migration mode (connects to PostgreSQL and applies migrations)
# ---------------------------------------------------------------------------

def do_run_migrations(connection: object) -> None:
    context.configure(
        connection=connection,  # type: ignore[arg-type]
        target_metadata=target_metadata,
        compare_type=True,
    )
    with context.begin_transaction():
        context.run_migrations()


async def run_async_migrations() -> None:
    """Create an async engine and run migrations using a sync connection wrapper."""
    connectable = create_async_engine(settings.DATABASE_URL, echo=False)

    async with connectable.connect() as connection:
        await connection.run_sync(do_run_migrations)

    await connectable.dispose()


def run_migrations_online() -> None:
    """Entry point for online migration mode."""
    asyncio.run(run_async_migrations())


# ---------------------------------------------------------------------------
# Dispatch to offline or online mode
# ---------------------------------------------------------------------------
if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
