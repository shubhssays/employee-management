"""
Attendance module exceptions.

Implementation: Phase 6
"""

from app.core.exceptions import ConflictError, NotFoundError


class AttendanceRecordNotFoundError(NotFoundError):
    error_code = "ATTENDANCE_RECORD_NOT_FOUND"

    def __init__(self) -> None:
        super().__init__("Attendance record was not found.")


class AlreadyCheckedInError(ConflictError):
    error_code = "ALREADY_CHECKED_IN"

    def __init__(self) -> None:
        super().__init__("Employee has already checked in today.")


class AlreadyCheckedOutError(ConflictError):
    error_code = "ALREADY_CHECKED_OUT"

    def __init__(self) -> None:
        super().__init__("Employee has already checked out today.")


class NotCheckedInError(ConflictError):
    error_code = "NOT_CHECKED_IN"

    def __init__(self) -> None:
        super().__init__("Employee has not checked in yet today.")
