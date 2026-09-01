"""
Dashboard router — /api/v1/dashboard

APIs (from blueprint §11):
  GET /api/v1/dashboard  — returns role-scoped summary (Employee | Manager | Admin view)

The dashboard never mutates data. It only reads from other modules' services.
It has no repository of its own.

Implementation: Phase 8
"""

from fastapi import APIRouter

router = APIRouter(tags=["Dashboard"])

# TODO (Phase 8): Implement dashboard endpoint.
#
# @router.get("")
# async def get_dashboard(current_user: CurrentUserDep, db: DbSession) -> ...:
#     """Returns Employee, Manager, or Admin dashboard based on current_user.role."""
#     ...
