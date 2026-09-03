"""
Organization exceptions.

Implementation: Phase 2
"""

from app.core.exceptions import BadRequestError, ConflictError, NotFoundError, UnprocessableError


class OrganizationNotFoundError(NotFoundError):
    error_code = "ORGANIZATION_NOT_FOUND"

    def __init__(self) -> None:
        super().__init__("Organization was not found.")


class OrganizationNameConflictError(ConflictError):
    error_code = "ORGANIZATION_NAME_CONFLICT"

    def __init__(self) -> None:
        super().__init__("An organization with this name already exists.")


class OrganizationSlugConflictError(ConflictError):
    error_code = "ORGANIZATION_SLUG_CONFLICT"

    def __init__(self, slug: str) -> None:
        super().__init__(f"An organization with slug '{slug}' already exists.")


class OrganizationNotActiveError(UnprocessableError):
    error_code = "ORGANIZATION_NOT_ACTIVE"

    def __init__(self) -> None:
        super().__init__("Organization is not active.")

class OrganizationValidationError(BadRequestError):
     error_code = "BAD_REQUEST_ERROR"

     def __init__(self, msg) -> None:
         super().__init__(f"{msg}")

