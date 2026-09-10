from datetime import datetime

from sqlalchemy import Integer, ForeignKey, Uuid, Boolean, DateTime
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base_model import Base


class ResetToken(Base):
    __tablename__ = "reset_token"

    emp_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("employees.id", ondelete="CASCADE"),
        nullable=False,
        comment="Id of the employee"
    )

    token: Mapped[str] = mapped_column(
        Uuid,
        nullable=False,
        comment="Unique code for password reset request"
    )

    is_active: Mapped[str] = mapped_column(
        Boolean,
        nullable=False,
        default=True,
        comment="Flags row as active or inactive"
    )

    used_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
    )

    expiry_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
    )
