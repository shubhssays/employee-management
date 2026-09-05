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


from datetime import UTC, datetime

from sqlalchemy import DateTime, Integer, text
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    """
    Declarative base for all ORM models.

    Every table that inherits from Base automatically gets:
        id          — int primary key
        created_at  — set on INSERT
        updated_at  — set on INSERT and every UPDATE
    """

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(UTC),
        server_default=text("NOW()"),
        nullable=False,
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=None,
        server_default=text("NOW()"),
        onupdate=lambda: datetime.now(UTC),
        nullable=False,
    )
