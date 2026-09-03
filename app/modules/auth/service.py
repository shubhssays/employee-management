from sqlalchemy.ext.asyncio import AsyncSession

from app.core.logging import get_logger
from app.core.security import verify_password, create_access_token
from app.modules.auth.exceptions import InvalidCredentialsError, AccountDeactivatedError
from app.modules.auth.repository import AuthRepository
from app.modules.auth.schemas import AdminLogin, AdminLoginResponse

logger = get_logger(__name__)


class AuthService:
    def __init__(self, db: AsyncSession):
        self.db = db
        self.repo = AuthRepository(db)

    async def admin_login(self, data: AdminLogin) -> AdminLoginResponse:
        async with self.db.begin():
            existing = await self.repo.get_admin(data.email, None)

            if not existing:
                raise InvalidCredentialsError()

            logger.debug("Existing: %s", existing)

            password_match = verify_password(data.password, existing.password_hash)

            if not password_match:
                raise InvalidCredentialsError()

            if not existing.is_active:
                raise AccountDeactivatedError()

            result = {
                "user_id": existing.id,
                "email": existing.email,
            }

            token = create_access_token(result)
            logger.info("Admin login successful")
            return AdminLoginResponse(
                id=existing.id,
                email=existing.email,
                name=existing.name,
                token=token
            )
