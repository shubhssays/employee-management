"""
Alembic model discovery registry.

Import ALL ORM models here so that Alembic's autogenerate
can see the full metadata graph when generating migrations.

Responsibility: This file exists ONLY for Alembic metadata discovery.
Do NOT import from this module in application code — import directly
from the module's models.py instead.

Add an import here whenever you create a new ORM model.
"""

# Base must be imported first — it defines the metadata object
from app.db.base_model import Base  # noqa: F401

# ---------------------------------------------------------------------------
# Module models — add new imports here as modules are implemented
# ---------------------------------------------------------------------------
# from app.modules.organization.models import Organization  # noqa: F401
# from app.modules.auth.models import User, RefreshToken, PasswordResetToken  # noqa: F401
# from app.modules.employees.models import Employee  # noqa: F401
# from app.modules.work_tracker.models import WorkEntry  # noqa: F401
# from app.modules.attendance.models import AttendanceRecord  # noqa: F401
# from app.modules.leave.models import (  # noqa: F401
#     LeaveType, LeavePolicyRule, LeaveBalance, LeaveRecord
# )
from app.modules.auth.models import Admin  # noqa: F401
from app.modules.organization.models import Organization  # noqa: F401

__all__ = ["Base"]
