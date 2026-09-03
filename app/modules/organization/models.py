
from sqlalchemy import Boolean, ForeignKey, Index, String
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base_model import Base
from app.modules.auth.models import Admin  # noqa: F401


class Organization(Base):

    __tablename__ = "organizations"

    name: Mapped[str] = mapped_column(
        String(200),
        nullable=False,
        comment="Name of the organization.",
    )

    slug: Mapped[str] = mapped_column(
        String(200),
        nullable=False,
        comment="Slug of the organization",
    )

    is_active: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        default=True,
        comment="Status of the organization",
    )

    created_by: Mapped[int] = mapped_column(
        ForeignKey("admins.id"),
        nullable=False,
        comment="ID of the admin who created the organization",
    )

    updated_by: Mapped[int] = mapped_column(
        ForeignKey("admins.id"),
        nullable=True,
        comment="ID of the admin who updated the organization",
    )

    # Composite index on (status, created_at) — useful for queries like
    # "show me all TODO organizations ordered by oldest first".
    __table_args__ = (Index("idx_organizations_slug", "slug"),)

    def __repr__(self) -> str:
        return f"<Organizations id={self.id!s} name={self.name!r} slug={self.slug!r} is_active={self.is_active}>"
