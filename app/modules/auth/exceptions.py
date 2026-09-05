"""
Auth module exceptions.

Implementation: Phase 3
"""

from app.core.exceptions import (
    AuthenticationError,
    ForbiddenError,
    InvalidCredentialsError,
    NotFoundError,
    UnprocessableError,
)


class InvalidCredentialsError(InvalidCredentialsError):
    error_code = "INVALID_CREDENTIALS"

    def __init__(self) -> None:
        super().__init__("Invalid email or password.")


class AccountDeactivatedError(ForbiddenError):
    error_code = "ACCOUNT_DEACTIVATED"

    def __init__(self) -> None:
        super().__init__("This account has been deactivated.")


class RefreshTokenExpiredError(AuthenticationError):
    error_code = "REFRESH_TOKEN_EXPIRED"

    def __init__(self) -> None:
        super().__init__("Refresh token has expired or been revoked.")


class ResetTokenInvalidError(UnprocessableError):
    error_code = "RESET_TOKEN_INVALID"

    def __init__(self) -> None:
        super().__init__("Password reset token is invalid or has already been used.")

class AdminNotFoundError(NotFoundError):
    error_code = "ADMIN_NOT_FOUND"

    def __init__(self) -> None:
        super().__init__("Admin not found")


class TokenNotFoundError(UnprocessableError):
    error_code = "TOKEN_NOT_FOUND"

    def __init__(self) -> None:
        super().__init__("Token not found.")

class TokenInvalidError(UnprocessableError):
    error_code = "TOKEN_INVALID"

    def __init__(self) -> None:
        super().__init__("Token is invalid. Token must start with 'Bearer '")



