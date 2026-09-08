from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.modules.Roles.models import Roles


class RolesRepository:
    def __init__(self, db: AsyncSession) -> None:
        self.db = db

    async def get_by_slug(self, role_slug: str) -> Roles | None:
        result = await self.db.execute(select(Roles).where(Roles.slug == role_slug))
        return result.scalar_one_or_none()
