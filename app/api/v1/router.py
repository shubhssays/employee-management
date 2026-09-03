"""
API v1 router registry.

All v1 routers are registered here and then mounted onto the
FastAPI application in main.py under the /api/v1 prefix.

Adding a new module router:
  1. Import the router from app/modules/<module>/router.py
  2. Add an api_router.include_router(...) call below
  3. The module is immediately available under /api/v1/<prefix>

Prefix and tag conventions:
  - prefix="/organizations"  → /api/v1/organizations/*
  - prefix="/auth"           → /api/v1/auth/*
  - prefix="/employees"      → /api/v1/employees/*
  etc.
"""

from fastapi import APIRouter

from app.api.v1.health import router as health_router

from app.modules.organization.router import router as org_router

# Placeholder imports — uncomment as modules are implemented:
# from app.modules.organization.router import router as org_router
# from app.modules.auth.router import router as auth_router
# from app.modules.employees.router import router as employees_router
# from app.modules.work_tracker.router import router as work_router
# from app.modules.attendance.router import router as attendance_router
# from app.modules.leave.router import router as leave_router
# from app.modules.dashboard.router import router as dashboard_router

api_router = APIRouter()

# ── System ─────────────────────────────────────────────────────────────────────────
api_router.include_router(health_router)

# ── Business modules (uncomment when implemented) ─────────────────────────
api_router.include_router(org_router,         prefix="/organizations")
# api_router.include_router(auth_router,        prefix="/auth")
# api_router.include_router(employees_router,   prefix="/employees")
# api_router.include_router(work_router,        prefix="/work-entries")
# api_router.include_router(attendance_router,  prefix="/attendance")
# api_router.include_router(leave_router,       prefix="/leave")
# api_router.include_router(dashboard_router,   prefix="/dashboard")
