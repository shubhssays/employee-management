from sqlalchemy.ext.asyncio import AsyncSession

from app.core.dependencies import CurrentUser
from app.core.logging import get_logger
from app.modules.organization.exceptions import OrganizationSlugConflictError, OrganizationNotFoundError, \
    OrganizationValidationError
from app.modules.organization.models import Organization
from app.modules.organization.repository import OrganizationRepository
from app.modules.organization.schemas import OrganizationCreate, OrganizationUpdate, OrganizationGetList, \
    OrganizationListResponse

logger = get_logger(__name__)

import math


class OrganizationService:

    def __init__(self, db: AsyncSession, current_user: CurrentUser) -> None:
        self.db = db
        self.repo = OrganizationRepository(db)
        current_user_dict = {
            "user_id": 1,
            "organization_id": 1,
            "role": "ADMIN"
        }
        self.user = current_user or CurrentUser(**current_user_dict)

    async def create_organization(self, data: OrganizationCreate) -> Organization:
        async with self.db.begin():
            existing = await self.repo.get_by(None, data.slug)
            if existing:
                raise OrganizationSlugConflictError(data.slug)

            org_dict = {
                **data.model_dump(exclude_none=True),
                "created_by": self.user.user_id,
                "is_active": True
            }
            org = Organization(**org_dict)
            new_organization = await self.repo.create(org)
            logger.info("Organization created successfully: %s", new_organization)
            return new_organization

    async def update_organization(self, organization_id: int, data: OrganizationUpdate) -> Organization:
        async with self.db.begin():
            existing = await self.repo.get_by(organization_id, None)
            if not existing:
                raise OrganizationNotFoundError()

            org_dict = data.model_dump(exclude_unset=True, exclude_none=True)

            if not org_dict:
                raise OrganizationValidationError("No data to update")

            org_dict["updated_by"] = self.user.user_id
            updated_organization = await self.repo.update(existing, org_dict)
            logger.info("Organization updated successfully: %s", updated_organization)
            return updated_organization

    async def get_organization(self, params: OrganizationGetList) -> OrganizationListResponse:
        async with self.db.begin():
            if (params.sort_by is None and params.sort_order is not None) or (
                    params.sort_by is not None and params.sort_order is None):
                raise OrganizationValidationError("Provide sort_order and sort_by or None")
            logger.debug("incoming: %s", params)
            organizations, total = await self.repo.get_all(params.model_dump())
            page = params.page or 1
            page_size = params.page_size or 20
            pages = math.ceil(total / page_size) if page_size > 0 else 0

            return OrganizationListResponse(
                items=organizations,
                total=total,
                page=page,
                page_size=page_size,
                pages=pages,
            )

    async def delete_organization(self, organization_id: int) -> None:
        async with self.db.begin():
            existing = await self.repo.get_by(organization_id)
            if not existing:
                raise OrganizationNotFoundError()
            return await self.repo.delete(existing)
