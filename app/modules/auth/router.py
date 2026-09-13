from typing import Annotated

from fastapi import APIRouter, status
from pydantic import Field

from app.core.dependencies import DbSession, CurrentUserDep
from app.modules.auth.schemas import Login, AdminLoginResponse, LoginResponse, SwitchRole
from app.modules.auth.service import AuthService
from app.modules.reset_token.schemas import ResetTokenResponse, ResetTokenChangePassword
from app.modules.reset_token.service import ResetTokenService
from app.shared.schemas import SuccessResponse

router = APIRouter(tags=["Auth"])


@router.post(
    "/admin_login",
    response_model=SuccessResponse[AdminLoginResponse],
    status_code=status.HTTP_200_OK,
    description=(
            "Admin login api."
    ),
)
async def admin_login(body: Login, db: DbSession) -> SuccessResponse[AdminLoginResponse]:
    service = AuthService(db, None)
    login_response = await service.admin_login(body)
    response = AdminLoginResponse.model_validate(login_response)
    return SuccessResponse(
        data=response,
        message="Login successful"
    )


@router.post(
    "/login",
    response_model=SuccessResponse[LoginResponse],
    status_code=status.HTTP_200_OK,
    description=(
            "Login api."
    ),
)
async def login(body: Login, db: DbSession) -> SuccessResponse[LoginResponse]:
    service = AuthService(db, None)
    login_response = await service.emp_mng_login(body)
    response = LoginResponse.model_validate(login_response)
    return SuccessResponse(
        data=response,
        message="Login successful"
    )


@router.post(
    "/switch-role",
    response_model=SuccessResponse[LoginResponse],
    status_code=status.HTTP_200_OK,
    description=(
            "Switch role api."
    ),
)
async def switch_role(
        body: SwitchRole,
        db: DbSession,
        current_user: CurrentUserDep,
) -> SuccessResponse[LoginResponse]:
    service = AuthService(db, current_user)
    login_response = await service.switch_role(body.role)
    response = LoginResponse.model_validate(login_response)
    return SuccessResponse(
        data=response,
        message=f"Role switched to '{body.role} successfully'"
    )


@router.get(
    "/change-password/{email}",
    response_model=SuccessResponse[ResetTokenResponse],
    status_code=status.HTTP_200_OK,
    description=(
            "Change password for employee."
    ),
)
async def change_password(
        email: Annotated[str, Field(description="Email of employee")],
        db: DbSession,
) -> SuccessResponse[ResetTokenResponse]:
    service = ResetTokenService(db)
    change_password_response = await service.change_password(email)
    response = ResetTokenResponse.model_validate(change_password_response)
    return SuccessResponse(
        data=response,
        message="Url generated successfully"
    )


@router.get(
    "/verify-token/{token}",
    response_model=SuccessResponse[bool],
    status_code=status.HTTP_200_OK,
    description=(
            "Verify token for reset password url."
    ),
)
async def verify_token(
        token: Annotated[str, Field(description="Reset password token")],
        db: DbSession,
) -> SuccessResponse[bool]:
    service = ResetTokenService(db)
    verify_token_response = await service.verify_token(token)
    response = verify_token_response
    return SuccessResponse(
        data=response,
    )


@router.put(
    "/update-password",
    response_model=SuccessResponse[bool],
    status_code=status.HTTP_200_OK,
    description=(
            "Change password."
    ),
)
async def update_password(
        body: ResetTokenChangePassword,
        db: DbSession,
) -> SuccessResponse[bool]:
    service = ResetTokenService(db)
    update_password_response = await service.update_password(body)
    response = update_password_response
    return SuccessResponse(
        data=response,
        message="Password changed successfully"
    )
