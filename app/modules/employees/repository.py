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

    async def get_by(self, id: int | None, email_mob: str | None) -> Employee | None:

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

        result = await self.db.execute(select(Employee).where(or_(
            *conditions
        )))
        return result.scalar_one_or_none()

    def _employee_detail_query(self):
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
        )

        return query

    async def get_by_detailed(self, id: int | None, email_mob: str | None) -> EmployeeDetailResponse | None:

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

        query = self._employee_detail_query().where(
            or_(*conditions)
        )

        result = await self.db.execute(query)
        row = result.one_or_none()

        if row is None:
            return None

        return EmployeeDetailResponse(**row._mapping)

    async def update(self, emp: Employee, data: dict) -> Employee:
        for field, value in data.items():
            setattr(emp, field, value)
        await self.db.flush()
        # await self.db.refresh(emp) # we don't need because on service we are already refetching the data
        return emp

    async def delete(self, emp: Employee) -> None:
        await self.db.delete(emp)
        await self.db.flush()
        return None

    async def get_list(self, params: dict) -> dict:
        ids: list[int] | None = params["ids"]
        organization_ids: list[int] | None = params["organization_ids"]
        departments: list[str] | None = params["departments"]
        email: str | None = params["email"]
        mobile: str | None = params["mobile"]
        first_name: str | None = params["first_name"]
        last_name: str | None = params["last_name"]
        page: int = params["page"]
        page_size: int = params["page_size"]
        sort_by: str = params["sort_by"]
        sort_order: str = params["sort_order"]

        conditions = []

        if ids:
            conditions.append(Employee.id.in_(ids))

        if organization_ids:
            conditions.append(Employee.organization_id.in_(organization_ids))

        if departments:
            conditions.append(Employee.department.in_(departments))

        if email is not None:
            conditions.append(Employee.email == email)

        if mobile is not None:
            conditions.append(Employee.mobile == mobile)

        if first_name is not None:
            conditions.append(Employee.first_name == first_name)

        if last_name is not None:
            conditions.append(Employee.last_name == last_name)

        sort_columns = {
            "id": Employee.id,
            "organization_id": Employee.organization_id,
            "department": Employee.department,
            "first_name": Employee.first_name,
            "last_name": Employee.last_name,
            "created_at": Employee.created_at,
            "updated_at": Employee.updated_at,
        }

        sort_by_column = sort_columns.get(sort_by, Employee.created_at)
        order_clause = sort_by_column.asc()

        if sort_order is not None:
            order_clause = sort_by_column.asc() if sort_order == "asc" else sort_by_column.desc()

        offset = (page - 1) * page_size

        stmt = (
            self._employee_detail_query()
            .where(*conditions)
            .order_by(order_clause)
            .offset(offset).limit(page_size)
        )

        result = await self.db.execute(stmt)
        rows = result.all()
        employees = [
            EmployeeDetailResponse(**row._mapping)
            for row in rows
        ]

        count_stmt = (
            select(func.count())
            .select_from(Employee)
            .where(*conditions)
        )
        total_count_result = await self.db.execute(count_stmt)
        total = total_count_result.scalar_one()
        return employees, total
