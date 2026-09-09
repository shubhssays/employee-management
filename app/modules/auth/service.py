import sqlalchemy.ext.asyncio

from app.core.dependencies import CurrentUser
from app.core.enums import AdminRole, UserRole
from app.core.logging import get_logger
from app.core.security import create_access_token, verify_password
from app.modules.auth.exceptions import AccountDeactivatedError, InvalidCredentialsError
from app.modules.auth.repository import AuthRepository
from app.modules.auth.schemas import Login, AdminLoginResponse, LoginResponse
from app.modules.employee_roles.repository import EmployeeRolesRepository
from app.modules.employees.exceptions import EmployeeRoleValidationError, EmployeeValidationError
from app.modules.employees.repository import EmployeeRepository

logger = get_logger(__name__)


class AuthService:
    def __init__(self, db: sqlalchemy.ext.asyncio.AsyncSession, current_user: CurrentUser | None):
        self.db = db
        self.repo = AuthRepository(db)
        self.emp_role_repo = EmployeeRolesRepository(db)
        self.emp_repo = EmployeeRepository(db)
        self.user = current_user

    async def admin_login(self, data: Login) -> AdminLoginResponse:
        async with self.db.begin():
            existing = await self.repo.get_admin(data.email, None)

            if not existing:
                raise InvalidCredentialsError()

            password_match = verify_password(data.password.get_secret_value(), existing.password_hash)

            if not password_match:
                raise InvalidCredentialsError()

            if not existing.is_active:
                raise AccountDeactivatedError()

            result = {
                "sub": str(existing.id),
                "org": 0,  # Ideally, Admin is not linked to any org, but it is just for the sake of consistency
                "active_role": AdminRole.ADMIN.value
            }

            token = create_access_token(result)
            logger.info("Admin login successful")
            return AdminLoginResponse(
                id=existing.id,
                email=existing.email,
                name=existing.name,
                roles=[AdminRole.ADMIN.value],
                access_token=token,
            )

    async def emp_mng_login(self, data: Login) -> LoginResponse:
        async with self.db.begin():
            existing = await self.repo.get_emp_or_mng(data.email, None)

            if not existing:
                raise InvalidCredentialsError()

            password_match = verify_password(data.password.get_secret_value(), existing.password_hash)

            if not password_match:
                raise InvalidCredentialsError()

            if not existing.is_active:
                raise AccountDeactivatedError()

            # Find existing roles that's associated with person trying to login
            existing_roles_slug = await self.emp_role_repo.get_emp_roles(existing.id)

            if not existing_roles_slug:
                raise EmployeeRoleValidationError()

            active_role = UserRole.MANAGER if UserRole.MANAGER in existing_roles_slug else UserRole.EMPLOYEE

            result = {
                "sub": str(existing.id),
                "org": existing.organization_id,
                "active_role": active_role
            }

            token = create_access_token(result)
            logger.info(f"'{active_role}' login successful")

            return LoginResponse(
                id=existing.id,
                email=existing.email,
                mobile=existing.mobile,
                first_name=existing.first_name,
                last_name=existing.last_name,
                roles=existing_roles_slug,
                access_token=token
            )

    async def switch_role(self, role: UserRole) -> LoginResponse:

        if role == self.user.active_role:
            raise EmployeeValidationError(f"You are already switched to '{role}'")

        existing = await self.emp_repo.get_by_detailed(self.user.user_id, None)

        if not existing.roles:
            raise EmployeeRoleValidationError()

        existing_roles_slug = [role.slug for role in existing.roles]

        if role not in existing_roles_slug:
            raise EmployeeValidationError(f"'{role}' is not assigned to you. Thus, you cannot switch to this role")

        result = {
            "sub": str(existing.id),
            "org": existing.organization_id,
            "active_role": role
        }

        token = create_access_token(result)

        return LoginResponse(
            id=existing.id,
            email=existing.email,
            mobile=existing.mobile,
            first_name=existing.first_name,
            last_name=existing.last_name,
            roles=existing_roles_slug,
            access_token=token
        )
