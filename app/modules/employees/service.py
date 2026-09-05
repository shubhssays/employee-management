import math

from sqlalchemy.ext.asyncio import AsyncSession

from app.core.dependencies import CurrentUser
from app.core.enums import AdminRole, UserRole
from app.core.exceptions import AccessDeniedError
from app.core.logging import get_logger
from app.core.security import hash_password
from app.modules.employees.exceptions import (
    EmailAlreadyExistsError,
    EmployeeNotFoundError,
    EmployeeValidationError,
)
from app.modules.employees.models import Employee
from app.modules.employees.repository import EmployeeRepository
from app.modules.employees.schemas import EmployeeCreate, EmployeeDetailResponse, EmployeeUpdate, EmployeeGetList, \
    EmployeeListResponse

logger = get_logger("__name__")


class EmployeeService:

    def __init__(self, db: AsyncSession, current_user: CurrentUser):
        self.db = db
        self.repo = EmployeeRepository(db)
        self.user = current_user

    async def create_employee(self, data: EmployeeCreate) -> EmployeeDetailResponse:
        async with self.db.begin():
            existing = await self.repo.get_by(None, data.email)

            if existing:
                raise EmailAlreadyExistsError(existing.email)

            hashed_password = hash_password(data.password.get_secret_value())

            emp_dict = {
                **data.model_dump(exclude_none=True, exclude={"password"}),
                "password_hash": hashed_password,
                "is_active": True
            }

            if self.user.role == AdminRole.ADMIN:
                emp_dict["created_by_admin"] = self.user.user_id
            elif self.user.role == UserRole.MANAGER:
                emp_dict["created_by_emp"] = self.user.user_id
            else:
                raise ValueError("Employee can be created only be admin or manager")

            emp = Employee(**emp_dict)
            new_emp = await self.repo.create(emp)
            existing = await self.repo.get_by_detailed(new_emp.id, None)
            logger.info("Employee created successfully: %s", existing)
            return existing

    async def update_employee(self, emp_id: int, data: EmployeeUpdate) -> EmployeeDetailResponse:
        async with self.db.begin():
            existing = await self.repo.get_by(emp_id, None)

            logger.debug("existing_employee : %s", existing)

            if not existing:
                raise EmployeeNotFoundError()

            if self.user.role == UserRole.EMPLOYEE and existing.id != self.user.user_id:
                raise AccessDeniedError()

            emp_dict = {
                **data.model_dump(exclude_none=True, exclude_unset=True)
            }

            if not emp_dict:
                raise EmployeeValidationError("No data to update")

            if "is_active" in emp_dict and self.user.role not in [UserRole.MANAGER, AdminRole.ADMIN]:
                raise EmployeeValidationError("Only manager and admin can mark employee as active or inactive")

            if "mobile" in emp_dict and self.user.role not in [UserRole.MANAGER, AdminRole.ADMIN]:
                raise EmployeeValidationError("Only manager and admin can update mobile")

            if "email" in emp_dict and self.user.role not in [UserRole.MANAGER, AdminRole.ADMIN]:
                raise EmployeeValidationError("Only manager and admin can update email")

            if self.user.role in [UserRole.MANAGER, UserRole.EMPLOYEE]:
                emp_dict["updated_by_emp"] = self.user.user_id

            if self.user.role == AdminRole.ADMIN:
                emp_dict["updated_by_admin"] = self.user.user_id

            if "password" in emp_dict:
                password_hash = data.password.get_secret_value()
                emp_dict.pop("password", None);
                emp_dict["password_hash"] = hash_password(password_hash)

            await self.repo.update(existing, emp_dict)
            updated_employee = await self.repo.get_by_detailed(existing.id, None)
            return updated_employee

    async def delete_employee(self, emp_id: int) -> None:
        async with self.db.begin():
            existing = await self.repo.get_by(emp_id, None)

            if not existing:
                raise EmployeeNotFoundError()

            await self.repo.delete(existing)
            return None

    async def get_list(self, params: EmployeeGetList) -> EmployeeListResponse:
        async with self.db.begin():
            if (params.sort_by is None and params.sort_order is not None) or (
                    params.sort_by is not None and params.sort_order is None):
                raise EmployeeValidationError("Provide sort_order and sort_by or None")

            employees, total = await self.repo.get_list(params.model_dump())
            page = params.page or 1
            page_size = params.page_size or 20
            pages = math.ceil(total / page_size) if page_size > 0 else 0

            return EmployeeListResponse(
                items=employees,
                total=total,
                page=page,
                page_size=page_size,
                pages=pages,
            )
