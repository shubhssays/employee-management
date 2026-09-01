"""
Work Tracker module exceptions.

Implementation: Phase 5
"""

from app.core.exceptions import NotFoundError, UnprocessableError


class WorkEntryNotFoundError(NotFoundError):
    error_code = "WORK_ENTRY_NOT_FOUND"

    def __init__(self) -> None:
        super().__init__("Work entry was not found.")


class WorkEntryLockedError(UnprocessableError):
    error_code = "WORK_ENTRY_LOCKED"

    def __init__(self) -> None:
        super().__init__("Work entry can no longer be edited — the 24-hour edit window has passed.")
