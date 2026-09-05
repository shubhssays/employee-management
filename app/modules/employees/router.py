from fastapi import APIRouter
from starlette import status

from app.core.dependencies import DbSession, ManagerOrAdminDep
from app.modules.employees.schemas import EmployeeCreate, EmployeeDetailResponse
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
