from sqlalchemy import select, delete
from sqlalchemy.ext.asyncio import AsyncSession

from app.modules.EmployeeRoles.models import EmployeeRoles
from app.modules.Roles.models import Roles


class EmployeeRolesRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_by(self, emp_id: int, role_id) -> EmployeeRoles | None:
        if emp_id is None or role_id is None:
            raise ValueError("Both emp_id and role_id are required")

        conditions = [EmployeeRoles.emp_id == emp_id, EmployeeRoles.role_id == role_id]

        result = await self.db.execute(select(EmployeeRoles).where(*conditions))
        return result.scalar_one_or_none()

    async def create(self, emp_roles: EmployeeRoles) -> None:
        self.db.add(emp_roles)
        await self.db.flush()
        return None

    async def delete_by(self, emp_id: int, role_ids: list[int] | None) -> None:

        conditions = [EmployeeRoles.emp_id == emp_id]

        if role_ids:
            conditions.append(EmployeeRoles.role_id.in_(role_ids))

        stmt = delete(EmployeeRoles).where(*conditions)

        await self.db.execute(stmt)
        return None

    async def get_emp_roles(self, emp_id: int) -> list[str]:
        stmt = (
            select(
                Roles.slug,
            )
            .select_from(EmployeeRoles)
            .join(
                Roles,
                EmployeeRoles.role_id == Roles.id
            )
            .where(
                EmployeeRoles.emp_id == emp_id
            )
        )

        result = await self.db.execute(stmt)
        return result.scalars().all()
