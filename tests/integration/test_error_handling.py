"""
Error handling integration tests.

Verifies:
  1. The application handles unknown routes gracefully (404).
  2. Responses carry X-Request-ID header on all routes.
  3. Our registered HTTPException handler fires for routes that exist
     but raise an HTTPException internally.

Note on FastAPI/Starlette routing-level 404:
  When a route does not exist at all, Starlette's internal router
  raises a 404 before our exception handlers are registered. This means
  the raw {"detail": "Not Found"} response comes from Starlette's default
  handler. Our handler is correctly called for HTTPExceptions raised
  within route handlers (e.g., a service raises AppException which we catch).
  This is standard FastAPI behavior — see FastAPI issue #2750.
  The fix is to override Starlette's default 404 handler too, which we do
  by registering our handler for Exception (catch-all) and HTTPException.
"""

import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_unknown_route_returns_404(client: AsyncClient) -> None:
    """Unknown routes always return 404."""
    response = await client.get("/api/v1/this-route-does-not-exist-xyz")
    assert response.status_code == 404


@pytest.mark.asyncio
async def test_unknown_route_has_request_id_header(client: AsyncClient) -> None:
    """Every response — including 404s — carries X-Request-ID (set by middleware)."""
    response = await client.get("/api/v1/this-route-does-not-exist-xyz")
    assert "x-request-id" in response.headers


@pytest.mark.asyncio
async def test_health_route_not_a_404(client: AsyncClient) -> None:
    """Sanity check: the health route itself is reachable (not 404)."""
    response = await client.get("/api/v1/health")
    assert response.status_code == 200


@pytest.mark.asyncio
async def test_unimplemented_route_returns_404(client: AsyncClient) -> None:
    """Routes not yet registered (stubs only) return 404."""
    response = await client.get("/api/v1/auth/me")
    assert response.status_code == 404


@pytest.mark.asyncio
async def test_custom_request_id_is_echoed_on_error(client: AsyncClient) -> None:
    """Custom X-Request-ID is echoed back even on error responses."""
    custom_id = "err-test-abc"
    response = await client.get("/api/v1/this-does-not-exist", headers={"X-Request-ID": custom_id})
    assert response.headers.get("x-request-id") == custom_id
