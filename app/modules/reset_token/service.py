from datetime import datetime, timedelta, timezone

from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import settings
from app.core.security import hash_password, generate_opaque_token, hash_opaque_token
from app.modules.employees.exceptions import EmployeeNotFoundError
from app.modules.employees.repository import EmployeeRepository
from app.modules.reset_token.exceptions import ResetTokenValidationError
from app.modules.reset_token.models import ResetToken
from app.modules.reset_token.repository import ResetTokenRepository
from app.modules.reset_token.schemas import ResetTokenResponse, EmployeeToken, \
    ResetTokenChangePassword


def create_reset_token_url(token: str) -> str:
    base = settings.BASE_URL.rstrip("/")
    prefix = settings.API_V1_PREFIX.strip("/")
    return f"{base}/{prefix}/auth/verify-token/{token}"


class ResetTokenService:
    def __init__(self, db: AsyncSession):
        self.db = db
        self.repo = ResetTokenRepository(db)
        self.emp_repo = EmployeeRepository(db)

    async def change_password(self, email: str) -> ResetTokenResponse:
        async with self.db.begin():
            existing_emp = await self.emp_repo.get_by(None, email)

            if not existing_emp:
                raise EmployeeNotFoundError()

            # Invalidate any existing unused token for this employee
            existing_token = await self.repo.get_unused(existing_emp.id)
            if existing_token:
                await self.repo.update(existing_token, {"is_active": False})

            token = generate_opaque_token()
            token_dict = {
                "emp_id": existing_emp.id,
                "token": hash_opaque_token(token),
                "is_active": True,
                "expiry_at": datetime.now(timezone.utc) + timedelta(hours=24),
            }
            new_token = await self.repo.create(ResetToken(**token_dict))
            url = create_reset_token_url(token)
            return ResetTokenResponse(url=url)

    async def verify_token(self, token: str) -> bool:
        async with self.db.begin():
            hash_token = hash_opaque_token(token)
            existing_token = await self.repo.get_by(hash_token, None)
            current_time = datetime.now(timezone.utc)

            if not existing_token:
                raise ResetTokenValidationError("Invalid reset link")

            if existing_token.expiry_at < current_time:
                raise ResetTokenValidationError("The link has been expired")

            if existing_token.used_at is not None or existing_token.is_active is False:
                raise ResetTokenValidationError("The link has been already used")

            return True

    async def update_password(self, data: ResetTokenChangePassword) -> bool:
        async with self.db.begin():
            existing_emp = await self.emp_repo.get_by(None, data.email)
            if not existing_emp:
                raise EmployeeNotFoundError()

            emp_token: EmployeeToken = {
                "emp_id": existing_emp.id,
                "token": hash_opaque_token(data.token),
            }
            existing_token = await self.repo.get_by(None, emp_token)
            current_time = datetime.now(timezone.utc)

            if not existing_token:
                raise ResetTokenValidationError("Invalid reset token.")

            if existing_token.used_at is not None or not existing_token.is_active:
                raise ResetTokenValidationError("The link has been already used")

            if existing_token.expiry_at < current_time:
                raise ResetTokenValidationError("The link has been expired. Kindly request a new one")

            # Marking token as used and deactivating it
            update_reset_token_dict = {
                "used_at": current_time,
                "is_active": False,
            }

            await self.repo.update(existing_token, update_reset_token_dict)

            # Updating Password
            hashed_password = hash_password(data.password.get_secret_value())

            emp_dict = {
                "password_hash": hashed_password,
            }

            await self.emp_repo.update(existing_emp, emp_dict)

            return True
