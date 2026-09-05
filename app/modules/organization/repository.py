from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.modules.organization.models import Organization


class OrganizationRepository:
    def __init__(self, db: AsyncSession) -> None:
        self.db = db

    async def create(self, org: Organization) -> Organization:
        self.db.add(org)
        await self.db.flush()
        await self.db.refresh(org)
        return org

    async def update(self, org: Organization, data: dict) -> Organization | None:
        for field, value in data.items():
            setattr(org, field, value)
        await self.db.flush()
        await self.db.refresh(org)
        return org

    async def delete(self, org: Organization) -> None:
        await self.db.delete(org)
        await self.db.flush()
        return None

    async def get_by(self, id: int | None = None, slug: str | None = None) -> Organization | None:
        if id is not None and slug is not None:
            raise ValueError("Provide id or slug, not both")

        if id is None and slug is None:
            raise ValueError("Provide id or slug, anyone one of them")

        where_clause = None

        if id is not None:
            condition = Organization.id == id
        else:
            condition = Organization.slug == slug

        result = await self.db.execute(select(Organization).where(condition))
        return result.scalar_one_or_none()

    async def get_all(self, params: dict) -> dict:
        page: int = params["page"]
        page_size: int = params["page_size"]
        ids: list[int] | None = params["ids"]
        slugs: list[str] | None = params["slugs"]
        sort_by: str = params["sort_by"]
        sort_order: str = params["sort_order"]

        conditions = []

        if ids:
            conditions.append(Organization.id.in_(ids))

        if slugs:
            conditions.append(Organization.slug.in_(slugs))

        sort_columns = {
            "id": Organization.id,
            "name": Organization.name,
            "slug": Organization.slug,
            "created_at": Organization.created_at,
            "updated_at": Organization.updated_at,
        }

        sort_by_column = sort_columns.get(sort_by, Organization.created_at)
        order_clause = sort_by_column.desc()
        if sort_order is not None:
            order_clause = sort_by_column.asc() if sort_order == "asc" else sort_by_column.desc()

        offset = (page - 1) * page_size
        stmt = (select(Organization).where(*conditions).order_by(order_clause).offset(offset).limit(page_size))
        result = await self.db.execute(stmt)
        organizations = list(result.scalars().all())
        total_count_result = await self.db.execute(select(func.count()).select_from(Organization).where(*conditions))
        total = total_count_result.scalar_one()
        return organizations, total
