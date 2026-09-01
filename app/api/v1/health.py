"""
Health check endpoint.

GET /api/v1/health

Returns the application's operational status. Used by:
  - Load balancer health checks
  - Deployment readiness probes
  - Smoke tests

No authentication required — this endpoint is always public.
"""

from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter(tags=["System"])


class HealthResponse(BaseModel):
    status: str
    version: str = "1.0.0"


@router.get(
    "/health",
    response_model=HealthResponse,
    summary="Health Check",
    description="Returns the application status. No authentication required.",
)
async def health_check() -> HealthResponse:
    return HealthResponse(status="ok")
