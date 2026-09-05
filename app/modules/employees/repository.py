from sqlalchemy import or_, func
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import aliased

from app.modules.auth.models import Admin
from app.modules.employees.models import Employee
from app.modules.employees.schemas import EmployeeDetailResponse
from app.modules.organization.models import Organization


class EmployeeRepository:
    def __init__(self, db: AsyncSession) -> None:
        self.db = db

    async def create(self, emp: Employee) -> Employee:
        self.db.add(emp)
        await self.db.flush()
        await self.db.refresh(emp)
        return emp

    async def get_by(self, id: int | None, email_mob: str | None) -> EmployeeDetailResponse | None:

        if id is not None and email_mob is not None:
            raise ValueError("Provide either id or email_mob, not both")

        if id is None and email_mob is None:
            raise ValueError("Provide anyone of them - id or email_mob")

        conditions = []

        if id is not None:
            conditions.append(Employee.id == id)

        if email_mob is not None:
            conditions.append(
                or_(Employee.email == email_mob, Employee.mobile == email_mob)
            )

        created_admin = aliased(Admin, name="created_admin")
        updated_admin = aliased(Admin, name="updated_admin")

        created_employee = aliased(Employee, name="created_employee")
        updated_employee = aliased(Employee, name="updated_employee")

        employee_columns = (
            Employee.id,
            Employee.first_name,
            Employee.last_name,
            Employee.password_hash,
            Employee.email,
            Employee.mobile,
            Employee.address,
            Employee.department,
            Employee.organization_id,
            Employee.is_active,
            Employee.created_at,
            Employee.updated_at
        )
        organization_columns = (
            Organization.name.label("organization_name"),
        )
        selected_columns = (
            created_admin.name.label("created_by_admin_name"),
            updated_admin.name.label("updated_by_admin_name"),
            func.concat_ws(" ", created_employee.first_name, created_employee.last_name).label(
                "created_by_employee_name"),
            func.concat_ws(" ", updated_employee.first_name, updated_employee.last_name).label(
                "updated_by_employee_name")
        )

        query = (
            select(
                *employee_columns,
                *organization_columns,
                *selected_columns
            )
            .join(
                Organization,
                Employee.organization_id == Organization.id
            )
            .outerjoin(
                created_admin,
                Employee.created_by_admin == created_admin.id
            )
            .outerjoin(
                updated_admin,
                Employee.updated_by_admin == updated_admin.id
            )
            .outerjoin(
                created_employee,
                Employee.created_by_emp == created_employee.id
            )
            .outerjoin(
                updated_employee,
                Employee.updated_by_emp == updated_employee.id
            )
            .where(
                or_(
                    *conditions
                )
            )
        )

        result = await self.db.execute(query)
        row = result.one_or_none()

        if row is None:
            return None

        return EmployeeDetailResponse(**row._mapping)
