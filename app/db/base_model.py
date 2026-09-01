"""
SQLAlchemy Base model with shared columns.

All ORM models in this project inherit from Base.
Provides:
  - id (UUID v4, server-side generated)
  - created_at (UTC timestamp, set on insert)
  - updated_at (UTC timestamp, updated on every change)

The 'id' is always a UUID to prevent sequential ID enumeration.
All timestamps are stored in UTC (TIMESTAMPTZ in PostgreSQL).
"""

import uuid
from datetime import UTC, datetime

from sqlalchemy import DateTime, text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    """
    Declarative base for all ORM models.

    Every table that inherits from Base automatically gets:
        id          — UUID primary key
        created_at  — set on INSERT
        updated_at  — set on INSERT and every UPDATE
    """

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        server_default=text("gen_random_uuid()"),
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(UTC),
        server_default=text("NOW()"),
        nullable=False,
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(UTC),
        server_default=text("NOW()"),
        onupdate=lambda: datetime.now(UTC),
        nullable=False,
    )
