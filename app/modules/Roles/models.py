from sqlalchemy import String, Index, Boolean
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base_model import Base


class Roles(Base):
    __tablename__ = "roles"

    slug: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
        comment="Slug of role. Should be in snake case, all small"
    )

    name: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
        comment="Name of role."
    )

    description: Mapped[str] = mapped_column(
        String(50),
        nullable=True,
        comment="Description of role"
    )

    is_active: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        default=True,
        comment="Flags the roles as active or inactive"
    )

    __table_args__ = (Index("idx_roles_slug", "slug"), Index("idx_roles_name", "name"))


def __repr__(self) -> str:
    return f"<Roles id:{self.id}  slug={self.slug!s} name={self.name!s}>"
