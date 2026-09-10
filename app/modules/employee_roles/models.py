from sqlalchemy import Index, Integer, Boolean, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base_model import Base


class EmployeeRoles(Base):
    __tablename__ = "employee_roles"

    emp_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("employees.id", ondelete="CASCADE"),
        nullable=False,
        comment="Id of the employee"
    )

    role_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("roles.id", ondelete="RESTRICT"),
        nullable=False,
        comment="Id of the role"
    )

    is_active: Mapped[str] = mapped_column(
        Boolean,
        nullable=False,
        default=True,
        comment="Flags row as active or inactive"
    )

    __table_args__ = (Index("idx_employee_roles_emp_id_role_id", "emp_id", "role_id"),)


def __repr__(self) -> str:
    return f"<Emp_Id id:{self.emp_id}  Role_Id={self.role_id}>"
