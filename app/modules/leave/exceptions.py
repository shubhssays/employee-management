"""
Leave module exceptions.

Implementation: Phase 7
"""

from app.core.exceptions import ConflictError, NotFoundError


class LeaveTypeNotFoundError(NotFoundError):
    error_code = "LEAVE_TYPE_NOT_FOUND"

    def __init__(self) -> None:
        super().__init__("Leave type was not found.")


class LeaveRequestNotFoundError(NotFoundError):
    error_code = "LEAVE_REQUEST_NOT_FOUND"

    def __init__(self) -> None:
        super().__init__("Leave request was not found.")


class InsufficientLeaveBalanceError(ConflictError):
    error_code = "INSUFFICIENT_LEAVE_BALANCE"

    def __init__(self) -> None:
        super().__init__("Insufficient leave balance to cover the requested dates.")


class OverlappingLeaveError(ConflictError):
    error_code = "OVERLAPPING_LEAVE"

    def __init__(self) -> None:
        super().__init__("Requested dates overlap with an existing active leave record.")


class LeaveRequestNotPendingError(ConflictError):
    error_code = "LEAVE_REQUEST_NOT_PENDING"

    def __init__(self) -> None:
        super().__init__("This leave request is no longer in PENDING status.")
