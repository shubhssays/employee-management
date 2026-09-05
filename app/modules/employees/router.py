from typing import Annotated

from fastapi import APIRouter
from pydantic import Field
from starlette import status

from app.core.dependencies import DbSession, ManagerOrAdminDep, CurrentUserDep
from app.modules.employees.schemas import EmployeeCreate, EmployeeDetailResponse, EmployeeUpdate
from app.modules.employees.service import EmployeeService

router = APIRouter(tags=["Employee"])


@router.post(
    "/",
    response_model=EmployeeDetailResponse,
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
) -> EmployeeDetailResponse:
    service = EmployeeService(db, current_user)
    employee = await service.create_employee(body)
    return EmployeeDetailResponse.model_validate(employee)


@router.put(
    "/{emp_id}",
    response_model=EmployeeDetailResponse,
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

) -> EmployeeDetailResponse:
    service = EmployeeService(db, current_user)
    employee = await service.update_employee(emp_id, body)
    return EmployeeDetailResponse.model_validate(employee)
