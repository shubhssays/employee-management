"""
Organization router — /api/v1/organizations/*

APIs (from blueprint §11):
  POST  /api/v1/organizations/register   — public, no auth
  GET   /api/v1/organizations/me         — Admin only
  PATCH /api/v1/organizations/me         — Admin only

Implementation: Phase 2
"""

from fastapi import APIRouter

router = APIRouter(tags=["Organization"])

# TODO (Phase 2): Implement organization endpoints.
#
# @router.post("/register", status_code=201)
# async def register_organization(...) -> ...: ...
#
# @router.get("/me")
# async def get_organization_settings(current_user: AdminDep, db: DbSession) -> ...: ...
#
# @router.patch("/me")
# async def update_organization_settings(...) -> ...: ...
