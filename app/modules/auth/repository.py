from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.modules.auth.models import Admin
from app.modules.employees.models import Employee


class AuthRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_admin(self, email: str | None, id: int | None) -> Admin | None:
        if email is not None and id is not None:
            raise ValueError("Provide either email or id, not both")

        if email is None and id is None:
            raise ValueError("Provide either email or id, anyone of them")

        condition = Admin.id == id

        if email is not None:
            condition = Admin.email == email

        result = await self.db.execute(
            select(
                Admin.id,
                Admin.email,
                Admin.name,
                Admin.password_hash,
                Admin.is_active,
            ).where(condition)
        )
        return result.mappings().one_or_none()

    async def get_emp_or_mng(self, email: str | None, id: int | None) -> Employee | None:

        if email is None and id is None:
            raise ValueError("Provide either email or id, anyone of them")

        if email is not None and id is not None:
            raise ValueError("Provide either email or id, not both")

        condition = Employee.id == id

        if email is not None:
            condition = Employee.email == email

        result = await self.db.execute(select(Employee).where(condition))

        return result.scalar_one_or_none()
