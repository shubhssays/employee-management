from sqlalchemy.ext.asyncio import AsyncSession

from app.core.logging import get_logger
from app.modules.organization.models import Organization
from app.modules.organization.repository import OrganizationRepository
from app.modules.organization.exceptions import OrganizationSlugConflictError

logger = get_logger(__name__)

class OrganizationService:
    def __init__(self, db: AsyncSession):
        self.repo = OrganizationRepository(db)

    async def create(self, data: Organization):
         existing = await self.repo.get_by(None, data.slug)
         logger.debug("Existing organization:", existing)

         if existing and existing.slug == data.slug:
             raise OrganizationSlugConflictError(data.slug)

         result = await self.repo.create(data)

