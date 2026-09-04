from typing import Annotated

from fastapi import APIRouter, status, Query
from pydantic import Field

from app.core.dependencies import DbSession, AdminDep
from app.modules.organization.schemas import OrganizationResponse, OrganizationCreate, OrganizationUpdate, \
    OrganizationGetList, OrganizationListResponse
from app.modules.organization.service import OrganizationService

router = APIRouter(tags=["Organization"])


@router.post(
    "/",
    response_model=OrganizationResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create Organization",
    description=(
            "Create a new Organization. Slug must be unique."
            "Status defaults to active."
    ),
)
async def create_organization(
        current_user: AdminDep,
        body: OrganizationCreate,
        db: DbSession,
) -> OrganizationResponse:
    service = OrganizationService(db, current_user)
    organization = await service.create_organization(data=body)
    return OrganizationResponse.model_validate(organization)


@router.patch(
    "/{organization_id}",
    response_model=OrganizationResponse,
    status_code=status.HTTP_200_OK,
    summary="Update Organization",
    description=(
            "Update a existing organization."
    ),
)
async def update_organization(
        current_user: AdminDep,
        organization_id: Annotated[int, Field(gt=0)],
        body: OrganizationUpdate,
        db: DbSession,
) -> OrganizationResponse:
    service = OrganizationService(db, current_user)
    organization = await service.update_organization(organization_id, data=body)
    return OrganizationResponse.model_validate(organization)


@router.get(
    "/",
    response_model=OrganizationListResponse,
    status_code=status.HTTP_200_OK,
    summary="Get Organization list",
    description=(
            "Get organization list."
            "Apply filter using ids."
            "Apply filter using slugs."
            "Apply filter using page. Default and minimum is 1."
            "Apply filter using page_size. Default is 20 and maximum is 100."
            "Apply filter using sort_by. Default is created_at."
            "Apply filter using sort_order. Default is desc. Supported options are desc or asc."
    ),
)
async def get_organization(
        current_user: AdminDep,
        db: DbSession,
        params: OrganizationGetList = Query(),
) -> OrganizationListResponse:
    service = OrganizationService(db, current_user)
    return await service.get_organization(params)


@router.delete(
    "/{organization_id}",
    response_model=None,
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete Organization",
    description=(
            "Delete a existing organization."
    ),
)
async def delete_organization(
        current_user: AdminDep,
        organization_id: Annotated[int, Field(gt=0)],
        db: DbSession,
) -> None:
    service = OrganizationService(db, current_user)
    return await service.delete_organization(organization_id)
