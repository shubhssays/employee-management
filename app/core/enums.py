"""
Enums shared across the application.

These are the role and status constants used by the auth/employee
modules and enforced by the authorization layer.
"""

import enum


class AdminRole(enum.StrEnum):
    ADMIN = "ADMIN"


class UserRole(enum.StrEnum):
    """The two fixed roles in the MVP permission model."""
    MANAGER = "MANAGER"
    EMPLOYEE = "EMPLOYEE"


class UserStatus(enum.StrEnum):
    ACTIVE = "ACTIVE"
    INACTIVE = "INACTIVE"


class LeaveStatus(enum.StrEnum):
    PENDING = "PENDING"
    APPROVED = "APPROVED"
    REJECTED = "REJECTED"
    CANCELLED = "CANCELLED"
    GRANTED = "GRANTED"


class AttendanceStatus(enum.StrEnum):
    PRESENT = "PRESENT"
    ABSENT = "ABSENT"
    LEAVE = "LEAVE"
    # HALF_DAY = "HALF_DAY"  # Post-MVP


class AllocationFrequency(enum.StrEnum):
    MONTHLY = "MONTHLY"
    QUARTERLY = "QUARTERLY"
    ANNUALLY = "ANNUALLY"


class DepartmentType(enum.StrEnum):
    DEVELOPER = "DEVELOPER"
    SUPPORT = "SUPPORT"
    HR = "HR"
    MANAGEMENT = "MANAGEMENT"
