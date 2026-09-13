from typing import Annotated

from fastapi import APIRouter, status, Query
from pydantic import Field

from app.core.dependencies import DbSession, AdminDep
from app.modules.organization.schemas import OrganizationResponse, OrganizationCreate, OrganizationUpdate, \
    OrganizationGetList, OrganizationListResponse
from app.modules.organization.service import OrganizationService
from app.shared.schemas import SuccessResponse

router = APIRouter(tags=["Organization"])


@router.post(
    "/",
    response_model=SuccessResponse[OrganizationResponse],
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
) -> SuccessResponse[OrganizationResponse]:
    service = OrganizationService(db, current_user)
    organization = await service.create_organization(data=body)
    response = OrganizationResponse.model_validate(organization)
    return SuccessResponse(
        data=response,
        message="Organization created successfully"
    )


@router.patch(
    "/{organization_id}",
    response_model=SuccessResponse[OrganizationResponse],
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
) -> SuccessResponse[OrganizationResponse]:
    service = OrganizationService(db, current_user)
    organization = await service.update_organization(organization_id, data=body)
    response = OrganizationResponse.model_validate(organization)
    SuccessResponse(
        data=response,
        message="Organization updated successfully"
    )


@router.get(
    "/",
    response_model=SuccessResponse[OrganizationListResponse],
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
) -> SuccessResponse[OrganizationListResponse]:
    service = OrganizationService(db, current_user)
    response = await service.get_organization(params)
    return SuccessResponse(
        data=response,
    )


@router.delete(
    "/{organization_id}",
    response_model=SuccessResponse[None],
    status_code=status.HTTP_200_OK,
    summary="Delete Organization",
    description=(
            "Delete a existing organization."
    ),
)
async def delete_organization(
        current_user: AdminDep,
        organization_id: Annotated[int, Field(gt=0)],
        db: DbSession,
) -> SuccessResponse[None]:
    service = OrganizationService(db, current_user)
    await service.delete_organization(organization_id)
    return SuccessResponse(
        data=None
    )
