from sqlalchemy import Boolean, ForeignKey, Index, Integer, String
from sqlalchemy import Enum as SAEnum
from sqlalchemy.orm import Mapped, mapped_column

from app.core.enums import DepartmentType
from app.db.base_model import Base


class Employee(Base):
    __tablename__ = "employees"

    first_name: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
        comment="First name of the employee"
    )

    last_name: Mapped[str] = mapped_column(
        String(50),
        nullable=True,
        comment="Last name of the employee"
    )

    email: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
        comment="Email of the employee"
    )

    mobile: Mapped[str] = mapped_column(
        String(20),
        nullable=True,
        comment="Mobile of the employee"
    )

    password_hash: Mapped[str] = mapped_column(
        String(80),
        nullable=False,
        comment="Encrypted password of the employee"
    )

    address: Mapped[str] = mapped_column(
        String(200),
        nullable=False,
        comment="Address of the employee"
    )

    department: Mapped[DepartmentType] = mapped_column(
        SAEnum(DepartmentType, name="department_enum", native_enum=True),
        nullable=False,
        comment="Department of the employee"
    )

    organization_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("organizations.id"),
        nullable=False,
        comment="Organization to which employee belongs too"
    )

    is_active: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        default=True,
        comment="Flags if employee is active or not"
    )

    created_by_emp: Mapped[int] = mapped_column(
        ForeignKey("employees.id"),
        nullable=True,
        comment="Tells if employee is created by another employee (possibly manager) itself"
    )

    created_by_admin: Mapped[int] = mapped_column(
        ForeignKey("admins.id"),
        nullable=True,
        comment="Tells if employee is created by admin"
    )

    updated_by_emp: Mapped[int] = mapped_column(
        ForeignKey("employees.id"),
        nullable=True,
        comment="Tells if employee is updated by another employee (possibly manager) itself"
    )

    updated_by_admin: Mapped[int] = mapped_column(
        ForeignKey("admins.id"),
        nullable=True,
        comment="Tells if employee is updated by admin"
    )

    __table_args__ = (Index("idx_employees_email", "email"), Index("idx_employees_mobile", "mobile"),)

    def __repr__(self) -> str:
        return f"<Employees id={self.id} first_name={self.first_name!s} last_name={self.last_name!s} email={self.email!s} mobile={self.mobile!s} organization_id={self.organization_id!s} is_active={self.is_active!s}>"
