from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.modules.roles.models import Roles


class RolesRepository:
    def __init__(self, db: AsyncSession) -> None:
        self.db = db

    async def get_by_slug(self, role_slugs: list[str]) -> list[Roles] | None:
        result = await self.db.execute(select(Roles).where(Roles.slug.in_(role_slugs)))
        return list(result.scalars().all())
