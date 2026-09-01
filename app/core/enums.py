"""
Enums shared across the application.

These are the role and status constants used by the auth/employee
modules and enforced by the authorization layer.
"""

import enum


class UserRole(enum.StrEnum):
    """The three fixed roles in the MVP permission model."""

    ADMIN = "ADMIN"
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
