from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.modules.EmployeeRoles.models import EmployeeRoles


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
