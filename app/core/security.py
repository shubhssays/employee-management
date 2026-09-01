"""
Security utilities: JWT handling and password hashing.

This module owns the cryptographic primitives. It does NOT own
the authentication flow (that lives in app/modules/auth/service.py).

Password hashing
----------------
Uses bcrypt directly (cost factor 12). passlib is not used because it
is unmaintained and incompatible with bcrypt 5.x on Python 3.13+.
Never store or log plaintext passwords.

JWT tokens
----------
Access tokens: short-lived JWTs signed with HS256.
Refresh tokens: opaque random strings stored as SHA-256 hashes in the database.
Password reset tokens: opaque random strings stored as SHA-256 hashes.
"""

import hashlib
import hmac
import secrets
from datetime import UTC, datetime, timedelta
from typing import Any

import bcrypt
from jose import JWTError, jwt

from app.core.config import settings
from app.core.exceptions import TokenExpiredError, TokenInvalidError

# ---------------------------------------------------------------------------
# Password hashing (bcrypt, cost factor 12)
# ---------------------------------------------------------------------------

_BCRYPT_ROUNDS = 12


def hash_password(plain_password: str) -> str:
    """Hash a plaintext password using bcrypt (cost factor 12)."""
    pwd_bytes = plain_password.encode("utf-8")
    salt = bcrypt.gensalt(rounds=_BCRYPT_ROUNDS)
    return bcrypt.hashpw(pwd_bytes, salt).decode("utf-8")


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Return True if the plain password matches the bcrypt hash."""
    try:
        return bcrypt.checkpw(
            plain_password.encode("utf-8"),
            hashed_password.encode("utf-8"),
        )
    except Exception:
        return False


# ---------------------------------------------------------------------------
# JWT access tokens
# ---------------------------------------------------------------------------


def create_access_token(payload: dict[str, Any]) -> str:
    """
    Create a signed JWT access token.

    The caller is responsible for including all required claims in `payload`.
    This function adds `exp` (expiry) and `iat` (issued-at) automatically.
    """
    now = datetime.now(UTC)
    expire = now + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    data = {
        **payload,
        "iat": now,
        "exp": expire,
        "type": "access",
    }
    return jwt.encode(data, settings.JWT_SECRET_KEY, algorithm=settings.JWT_ALGORITHM)


def decode_access_token(token: str) -> dict[str, Any]:
    """
    Decode and validate a JWT access token.

    Raises:
        TokenExpiredError: if the token has expired.
        TokenInvalidError: if the token cannot be decoded.
    """
    try:
        payload = jwt.decode(
            token,
            settings.JWT_SECRET_KEY,
            algorithms=[settings.JWT_ALGORITHM],
        )
        if payload.get("type") != "access":
            raise TokenInvalidError("Token type mismatch.")
        return payload
    except JWTError as exc:
        if "expired" in str(exc).lower():
            raise TokenExpiredError("Access token has expired.") from exc
        raise TokenInvalidError("Access token is invalid.") from exc


# ---------------------------------------------------------------------------
# Opaque tokens (refresh tokens, password reset tokens)
# ---------------------------------------------------------------------------


def generate_opaque_token() -> str:
    """
    Generate a cryptographically secure URL-safe random token string.

    The raw token is returned and should be sent to the user (e.g., in email or response).
    Store only the hashed version in the database via `hash_opaque_token`.
    """
    return secrets.token_urlsafe(32)


def hash_opaque_token(token: str) -> str:
    """
    Hash an opaque token for safe database storage using SHA-256.

    We use SHA-256 (not bcrypt) for opaque tokens because:
      1. These are already high-entropy random strings (not user passwords).
      2. bcrypt has a 72-byte limit — long URL-safe tokens can exceed it.
      3. SHA-256 is fast for known-entropy tokens and produces a fixed 64-char hex string.
    """
    return hashlib.sha256(token.encode("utf-8")).hexdigest()


def verify_opaque_token(plain_token: str, hashed_token: str) -> bool:
    """Verify a raw opaque token against its stored SHA-256 hash (timing-safe)."""
    expected = hash_opaque_token(plain_token)
    return hmac.compare_digest(expected, hashed_token)
