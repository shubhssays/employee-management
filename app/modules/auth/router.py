from fastapi import APIRouter, status

from app.core.dependencies import DbSession, CurrentUserDep
from app.modules.auth.schemas import Login, AdminLoginResponse, LoginResponse, SwitchRole
from app.modules.auth.service import AuthService

router = APIRouter(tags=["Auth"])


@router.post(
    "/admin_login",
    response_model=AdminLoginResponse,
    status_code=status.HTTP_200_OK,
    description=(
            "Admin login api."
    ),
)
async def admin_login(body: Login, db: DbSession) -> AdminLoginResponse:
    service = AuthService(db, None)
    login_response = await service.admin_login(body)
    return AdminLoginResponse.model_validate(login_response)


@router.post(
    "/login",
    response_model=LoginResponse,
    status_code=status.HTTP_200_OK,
    description=(
            "Login api."
    ),
)
async def login(body: Login, db: DbSession) -> LoginResponse:
    service = AuthService(db, None)
    login_response = await service.emp_mng_login(body)
    return LoginResponse.model_validate(login_response)


@router.post(
    "/switch_role",
    response_model=LoginResponse,
    status_code=status.HTTP_200_OK,
    description=(
            "Switch role api."
    ),
)
async def switch_role(
        body: SwitchRole,
        db: DbSession,
        current_user: CurrentUserDep,
) -> LoginResponse:
    service = AuthService(db, current_user)
    login_response = await service.switch_role(body.role)
    return LoginResponse.model_validate(login_response)
