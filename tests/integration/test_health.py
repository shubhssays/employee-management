"""
Health check integration test — the primary smoke test.

Verifies:
  1. The application starts successfully.
  2. GET /api/v1/health returns 200.
  3. The response body matches the expected schema.
  4. The X-Request-ID header is present in the response.

This test does not require a database connection.
It must pass before any other tests are run.
"""

import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_health_check_returns_200(client: AsyncClient) -> None:
    response = await client.get("/api/v1/health")
    assert response.status_code == 200


@pytest.mark.asyncio
async def test_health_check_response_body(client: AsyncClient) -> None:
    response = await client.get("/api/v1/health")
    data = response.json()
    assert data["status"] == "ok"
    assert "version" in data


@pytest.mark.asyncio
async def test_health_check_has_request_id_header(client: AsyncClient) -> None:
    response = await client.get("/api/v1/health")
    assert "x-request-id" in response.headers


@pytest.mark.asyncio
async def test_health_check_echoes_custom_request_id(client: AsyncClient) -> None:
    custom_id = "test-req-abc123"
    response = await client.get("/api/v1/health", headers={"X-Request-ID": custom_id})
    assert response.headers.get("x-request-id") == custom_id
