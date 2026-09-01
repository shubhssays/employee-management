"""
FastAPI dependency providers.

These are the shared Depends() functions injected into routers.
They establish the authentication and authorization boundary.

Dependency injection chain:
    HTTP Request
        → get_db (database session)
        → get_current_user (extract + validate JWT, return CurrentUser)
        → require_admin / require_manager (role gate)

CurrentUser is a lightweight data object — not an ORM model.
It carries exactly the fields needed for authorization decisions:
  user_id, organization_id, employee_id, role.

This keeps routers and services decoupled from SQLAlchemy model internals.
"""

from typing import Annotated
from uuid import UUID

from fastapi import Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.enums import UserRole
from app.core.exceptions import (
    AuthenticationError,
    ForbiddenError,
    TokenExpiredError,
    TokenInvalidError,
)
from app.core.security import decode_access_token
from app.db.session import get_db  # noqa: F401 — re-exported for convenience

# ---------------------------------------------------------------------------
# Re-export get_db so callers can import from here or from db.session
# ---------------------------------------------------------------------------

# ---------------------------------------------------------------------------
# Current user identity object
# ---------------------------------------------------------------------------


class CurrentUser(BaseModel):
    """
    Lightweight representation of the authenticated user.

    Injected into route handlers via get_current_user dependency.
    Services receive this object to perform authorization checks.

    Attributes:
        user_id:          UUID of the User record (auth identity)
        organization_id:  UUID of the tenant the user belongs to
        employee_id:      UUID of the Employee record (HR profile)
        role:             Role enum (ADMIN | MANAGER | EMPLOYEE)
    """

    user_id: UUID
    organization_id: UUID
    employee_id: UUID
    role: UserRole


# ---------------------------------------------------------------------------
# Bearer token extractor
# ---------------------------------------------------------------------------

_bearer = HTTPBearer(auto_error=False)


async def get_current_user(
    credentials: Annotated[HTTPAuthorizationCredentials | None, Depends(_bearer)],
) -> CurrentUser:
    """
    Extract and validate the Bearer JWT from the Authorization header.

    Returns a CurrentUser instance populated from the token payload.
    Raises AuthenticationError (401) if the token is missing or invalid.

    Note: This dependency does NOT hit the database. The JWT payload
    carries all the information needed for identity and authorization.
    A database call is only needed when the caller requires full user
    profile data — that is the responsibility of the service layer.
    """
    if credentials is None:
        raise AuthenticationError("Authorization header is missing.")

    try:
        payload = decode_access_token(credentials.credentials)
    except (TokenExpiredError, TokenInvalidError) as exc:
        raise exc

    try:
        return CurrentUser(
            user_id=UUID(payload["sub"]),
            organization_id=UUID(payload["org"]),
            employee_id=UUID(payload["emp"]),
            role=UserRole(payload["role"]),
        )
    except (KeyError, ValueError) as exc:
        raise AuthenticationError("Token payload is malformed.") from exc


# ---------------------------------------------------------------------------
# Role gates — composable authorization dependencies
# ---------------------------------------------------------------------------


async def require_admin(
    current_user: Annotated[CurrentUser, Depends(get_current_user)],
) -> CurrentUser:
    """Allow only ADMIN role. Returns CurrentUser for further use."""
    if current_user.role != UserRole.ADMIN:
        raise ForbiddenError("Admin privileges are required.")
    return current_user


async def require_manager_or_admin(
    current_user: Annotated[CurrentUser, Depends(get_current_user)],
) -> CurrentUser:
    """Allow MANAGER or ADMIN role. Returns CurrentUser for further use."""
    if current_user.role == UserRole.EMPLOYEE:
        raise ForbiddenError("Manager or Admin privileges are required.")
    return current_user


# ---------------------------------------------------------------------------
# Convenience type aliases for route signatures
# ---------------------------------------------------------------------------

CurrentUserDep = Annotated[CurrentUser, Depends(get_current_user)]
AdminDep = Annotated[CurrentUser, Depends(require_admin)]
ManagerOrAdminDep = Annotated[CurrentUser, Depends(require_manager_or_admin)]
DbSession = Annotated[AsyncSession, Depends(get_db)]
