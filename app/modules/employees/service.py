from sqlalchemy.ext.asyncio import AsyncSession

from app.core.dependencies import CurrentUser
from app.core.enums import AdminRole, UserRole
from app.core.logging import get_logger
from app.core.security import hash_password
from app.modules.employees.exceptions import EmailAlreadyExistsError
from app.modules.employees.models import Employee
from app.modules.employees.repository import EmployeeRepository
from app.modules.employees.schemas import EmployeeCreate, EmployeeDetailResponse

logger = get_logger("__name__")


class EmployeeService:

    def __init__(self, db: AsyncSession, current_user: CurrentUser):
        self.db = db;
        self.repo = EmployeeRepository(db);
        self.user = current_user

    async def create_employee(self, data: EmployeeCreate) -> EmployeeDetailResponse:
        async with self.db.begin():
            existing = await self.repo.get_by(None, data.email)

            if existing:
                raise EmailAlreadyExistsError(existing.email)

            hashed_password = hash_password(data.password_hash.get_secret_value())

            emp_dict = {
                **data.model_dump(exclude_none=True, exclude={"password_hash"}),
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
            existing = await self.repo.get_by(new_emp.id, None)
            logger.info("Employee created successfully: %s", existing)
            return existing
