"""
Organization exceptions.

Implementation: Phase 2
"""

from app.core.exceptions import ConflictError, NotFoundError, UnprocessableError


class OrganizationNotFoundError(NotFoundError):
    error_code = "ORGANIZATION_NOT_FOUND"

    def __init__(self) -> None:
        super().__init__("Organization was not found.")


class OrganizationNameConflictError(ConflictError):
    error_code = "ORGANIZATION_NAME_CONFLICT"

    def __init__(self) -> None:
        super().__init__("An organization with this name already exists.")


class TimezoneChangeNotSupportedError(UnprocessableError):
    error_code = "TIMEZONE_CHANGE_NOT_SUPPORTED"

    def __init__(self) -> None:
        super().__init__(
            "Changing the organization timezone is not supported via self-service. "
            "Please contact support."
        )
