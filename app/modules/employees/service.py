import math

from sqlalchemy.ext.asyncio import AsyncSession

from app.core.dependencies import CurrentUser
from app.core.enums import AdminRole, UserRole
from app.core.exceptions import AccessDeniedError
from app.core.logging import get_logger
from app.core.security import hash_password
from app.modules.employee_roles.models import EmployeeRoles
from app.modules.employee_roles.repository import EmployeeRolesRepository
from app.modules.employees.exceptions import (
    EmailAlreadyExistsError,
    EmployeeNotFoundError,
    EmployeeValidationError,
)
from app.modules.employees.models import Employee
from app.modules.employees.repository import EmployeeRepository
from app.modules.employees.schemas import EmployeeCreate, EmployeeDetailResponse, EmployeeUpdate, EmployeeGetList, \
    EmployeeListResponse
from app.modules.roles.exceptions import RolesNotFoundError, RolesNotActiveError
from app.modules.roles.repository import RolesRepository

logger = get_logger("__name__")


class EmployeeService:

    def __init__(self, db: AsyncSession, current_user: CurrentUser):
        self.db = db
        self.emp_repo = EmployeeRepository(db)
        self.role_repo = RolesRepository(db)
        self.emp_roles_repo = EmployeeRolesRepository(db)
        self.user = current_user

    async def create_employee(self, data: EmployeeCreate) -> EmployeeDetailResponse | None:
        async with self.db.begin():
            existing = await self.emp_repo.get_by(None, data.email)

            if existing:
                raise EmailAlreadyExistsError(existing.email)

            hashed_password = hash_password(data.password.get_secret_value())

            role_slug = data.role_slug

            emp_dict = {
                **data.model_dump(exclude_none=True, exclude={"password", "role_slug"}),
                "password_hash": hashed_password,
                "is_active": True
            }

            if self.user.active_role == AdminRole.ADMIN:
                emp_dict["created_by_admin"] = self.user.user_id
            elif self.user.active_role == UserRole.MANAGER:
                emp_dict["created_by_emp"] = self.user.user_id
            else:
                raise ValueError("Employee can be created only be admin or manager")

            emp = Employee(**emp_dict)
            new_emp = await self.emp_repo.create(emp)

            # Adding role
            existing_roles = await self.role_repo.get_by_slug([role_slug])
            if not existing_roles:
                raise RolesNotFoundError()

            existing_role = existing_roles[0]

            if not existing_role.is_active:
                raise RolesNotActiveError()

            emp_roles_dict = {
                "emp_id": new_emp.id,
                "role_id": existing_role.id
            }

            emp_roles = EmployeeRoles(**emp_roles_dict)
            await self.emp_roles_repo.create(emp_roles)

            existing = await self.emp_repo.get_by_detailed(new_emp.id, None)
            logger.info("Employee created successfully: %s", existing)
            return existing

    async def update_employee(self, emp_id: int, data: EmployeeUpdate) -> EmployeeDetailResponse | None:
        async with self.db.begin():
            existing = await self.emp_repo.get_by(emp_id, None)

            if not existing:
                raise EmployeeNotFoundError()

            if self.user.active_role == UserRole.EMPLOYEE and existing.id != self.user.user_id:
                raise AccessDeniedError()

            role_slug = data.role_slug
            remove_roles_slug = data.remove_roles_slug

            emp_dict = {
                **data.model_dump(exclude_none=True, exclude_unset=True, exclude={"role_slug", "remove_roles_slug"})
            }

            if not emp_dict:
                raise EmployeeValidationError("No data to update")

            if "is_active" in emp_dict and self.user.active_role not in [UserRole.MANAGER, AdminRole.ADMIN]:
                raise EmployeeValidationError("Only manager and admin can mark employee as active or inactive")

            if "mobile" in emp_dict and self.user.active_role not in [UserRole.MANAGER, AdminRole.ADMIN]:
                raise EmployeeValidationError("Only manager and admin can update mobile")

            if "email" in emp_dict and self.user.active_role not in [UserRole.MANAGER, AdminRole.ADMIN]:
                raise EmployeeValidationError("Only manager and admin can update email")

            if self.user.active_role in [UserRole.MANAGER, UserRole.EMPLOYEE]:
                emp_dict["updated_by_emp"] = self.user.user_id

            if self.user.active_role == AdminRole.ADMIN:
                emp_dict["updated_by_admin"] = self.user.user_id

            if "password" in emp_dict:
                password_hash = data.password.get_secret_value()
                emp_dict.pop("password", None);
                emp_dict["password_hash"] = hash_password(password_hash)

            await self.emp_repo.update(existing, emp_dict)

            # Validating roles
            if remove_roles_slug and role_slug:
                if role_slug in remove_roles_slug:
                    raise EmployeeValidationError(
                        f"Same '{role_slug}' role cannot be added and removed at the same time")

            # Finding existing roles
            existing_emp_roles = await self.emp_roles_repo.get_emp_roles(existing.id)

            ## Removing slug
            # Checking roles that needs to be removed is actually assigned to employee or not
            if remove_roles_slug:
                for role in remove_roles_slug:
                    if role not in existing_emp_roles:
                        raise EmployeeValidationError(f"'{role}' is not assigned to user. Thus, it cannot be removed")

                # Finding role_id of roles to remove
                assigned_roles_to_removed = await self.role_repo.get_by_slug(remove_roles_slug)
                if assigned_roles_to_removed:
                    assigned_role_ids_to_removed = [assigned_role_to_removed.id for assigned_role_to_removed in
                                                    assigned_roles_to_removed]

                    # Deleting entering from employee_roles table
                    await self.emp_roles_repo.delete_by(existing.id, assigned_role_ids_to_removed)

            ## Adding role

            # Checking if role that needs to be added is actually assigned to employee or not
            if role_slug:
                if role_slug in existing_emp_roles:
                    logger.warning(f"'{role_slug}' is already assigned to user. Thus, it cannot be assigned again")
                else:
                    existing_roles = await self.role_repo.get_by_slug([role_slug])
                    if not existing_roles:
                        raise RolesNotFoundError()

                    existing_role = existing_roles[0]

                    if not existing_role.is_active:
                        raise RolesNotActiveError()

                    emp_roles_dict = {
                        "emp_id": existing.id,
                        "role_id": existing_role.id
                    }

                    emp_roles = EmployeeRoles(**emp_roles_dict)

                    await self.emp_roles_repo.create(emp_roles)

            updated_employee = await self.emp_repo.get_by_detailed(existing.id, None)
            return updated_employee

    async def delete_employee(self, emp_id: int) -> None:
        async with self.db.begin():
            existing = await self.emp_repo.get_by(emp_id, None)

            if not existing:
                raise EmployeeNotFoundError()

            # Deleting employee roles first
            await self.emp_roles_repo.delete_by(existing.id, None)
            # Deleting employee now
            await self.emp_repo.delete(existing)
            return None

    async def get_list(self, params: EmployeeGetList) -> EmployeeListResponse:
        async with self.db.begin():
            if (params.sort_by is None and params.sort_order is not None) or (
                    params.sort_by is not None and params.sort_order is None):
                raise EmployeeValidationError("Provide sort_order and sort_by or None")

            employees, total = await self.emp_repo.get_list(params.model_dump())
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
