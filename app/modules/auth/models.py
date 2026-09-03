"""
Admin and Auth ORM models.
"""

from sqlalchemy import Boolean, Index, String
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base_model import Base


class Admin(Base):
    __tablename__ = "admins"

    name: Mapped[str] = mapped_column(String(100), nullable=False)
    email: Mapped[str] = mapped_column(String(80), unique=True, nullable=False, index=True)
    password_hash: Mapped[str] = mapped_column(String(200), nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)

    __table_args__ = (Index("idx_admins_email", "email"),)

    def __repr__(self) -> str:
        return f"<Admin id={self.id} email={self.email!r}>"
