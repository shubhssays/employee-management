from app.core.exceptions import NotFoundError, UnprocessableError


class RolesNotFoundError(NotFoundError):
    error_code = "ROLE_NOT_FOUND"


class RolesNotActiveError(UnprocessableError):
    error_code = "ROLE_NOT_ACTIVE"

