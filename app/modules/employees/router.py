from typing import Annotated

from fastapi import APIRouter, Query
from pydantic import Field
from starlette import status

from app.core.dependencies import DbSession, ManagerOrAdminDep, CurrentUserDep
from app.modules.employees.schemas import EmployeeCreate, EmployeeDetailResponse, EmployeeUpdate, EmployeeListResponse, \
    EmployeeGetList
from app.modules.employees.service import EmployeeService
from app.shared.schemas import SuccessResponse

router = APIRouter(tags=["Employee"])


@router.post(
    "/",
    response_model=SuccessResponse[EmployeeDetailResponse],
    status_code=status.HTTP_201_CREATED,
    summary="Create Employee",
    description=(
            "Create a new employee. Email and mobile must be unique"
            "Both manager and admin can create employee"
    ),
)
async def create_employee(
        current_user: ManagerOrAdminDep,
        body: EmployeeCreate,
        db: DbSession,
) -> SuccessResponse[EmployeeDetailResponse]:
    service = EmployeeService(db, current_user)
    employee = await service.create_employee(body)
    response = EmployeeDetailResponse.model_validate(employee)
    return SuccessResponse(
        data=response,
        message="Employee created successfully"
    )


@router.put(
    "/{emp_id}",
    response_model=SuccessResponse[EmployeeDetailResponse],
    status_code=status.HTTP_200_OK,
    summary="Update existing employee",
    description=(
            "Can be used by admin, manager and employee themself."
            "Fields like in_active, email and mobile can only be updated by admin or manager and not employee"
    ),

)
async def update_employee(
        current_user: CurrentUserDep or ManagerOrAdminDep,
        emp_id: Annotated[int, Field(gt=0)],
        body: EmployeeUpdate,
        db: DbSession,

) -> SuccessResponse[EmployeeDetailResponse]:
    service = EmployeeService(db, current_user)
    employee = await service.update_employee(emp_id, body)
    response = EmployeeDetailResponse.model_validate(employee)
    return SuccessResponse(
        data=response,
        message="Employee updated successfully"
    )


@router.delete(
    "/{emp_id}",
    response_model=SuccessResponse[None],
    status_code=status.HTTP_200_OK,
    summary="Delete existing employee",
    description=(
            "Only admin and manager can delete the employee"
    ),
)
async def delete_employee(
        current_user: ManagerOrAdminDep,
        emp_id: Annotated[int, Field(gt=0)],
        db: DbSession
) -> SuccessResponse[None]:
    service = EmployeeService(db, current_user)
    await service.delete_employee(emp_id)
    return SuccessResponse(
        data=None,
        message="Employee deleted successfully"
    )


@router.get(
    "/",
    response_model=SuccessResponse[EmployeeListResponse],
    status_code=status.HTTP_200_OK,
    summary="Get employee list",
    description=(
            "Get employee list."
            "Apply filter using ids."
            "Apply filter using departments."
            "Apply filter using email."
            "Apply filter using mobile."
            "Apply filter using first_name."
            "Apply filter using last_name."
            "Apply filter using page. Default and minimum is 1."
            "Apply filter using page_size. Default is 20 and maximum is 100."
            "Apply filter using sort_by. Default is created_at."
            "Apply filter using sort_order. Default is desc. Supported options are desc or asc."
    ),
)
async def get_employees(
        current_user: ManagerOrAdminDep,
        db: DbSession,
        params: EmployeeGetList = Query()
) -> SuccessResponse[EmployeeListResponse]:
    service = EmployeeService(db, current_user)
    response = await service.get_list(params)
    return SuccessResponse(
        data=response,
    )
