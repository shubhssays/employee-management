"""
Employees module exceptions.

Implementation: Phase 4
"""

from app.core.exceptions import ConflictError, NotFoundError, UnprocessableError


class EmployeeNotFoundError(NotFoundError):
    error_code = "EMPLOYEE_NOT_FOUND"

    def __init__(self) -> None:
        super().__init__("Employee was not found.")


class EmailAlreadyExistsError(ConflictError):
    error_code = "EMAIL_ALREADY_EXISTS"

    def __init__(self) -> None:
        super().__init__("An employee with this email already exists in the organization.")


class EmployeeAlreadyInactiveError(ConflictError):
    error_code = "EMPLOYEE_ALREADY_INACTIVE"

    def __init__(self) -> None:
        super().__init__("This employee is already inactive.")


class CannotDeactivateSoleAdminError(UnprocessableError):
    error_code = "CANNOT_DEACTIVATE_SOLE_ADMIN"

    def __init__(self) -> None:
        super().__init__("Cannot deactivate the only Admin of the organization.")
