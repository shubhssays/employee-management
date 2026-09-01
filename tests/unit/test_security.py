"""
Unit tests for core security utilities.

Tests password hashing and JWT token lifecycle.
These are pure unit tests — no database or HTTP calls.
"""

import time

import pytest
from jose import jwt

from app.core.config import settings
from app.core.exceptions import TokenInvalidError
from app.core.security import (
    create_access_token,
    decode_access_token,
    generate_opaque_token,
    hash_opaque_token,
    hash_password,
    verify_opaque_token,
    verify_password,
)

# ---------------------------------------------------------------------------
# Password hashing
# ---------------------------------------------------------------------------


class TestPasswordHashing:
    def test_hash_password_returns_string(self) -> None:
        hashed = hash_password("mysecretpassword")
        assert isinstance(hashed, str)
        assert len(hashed) > 0

    def test_hashed_password_differs_from_plaintext(self) -> None:
        plain = "mysecretpassword"
        hashed = hash_password(plain)
        assert hashed != plain

    def test_verify_password_success(self) -> None:
        plain = "correctpassword"
        hashed = hash_password(plain)
        assert verify_password(plain, hashed) is True

    def test_verify_password_wrong_password(self) -> None:
        hashed = hash_password("correctpassword")
        assert verify_password("wrongpassword", hashed) is False

    def test_same_password_produces_different_hashes(self) -> None:
        """bcrypt generates a unique salt every time."""
        h1 = hash_password("samepassword")
        h2 = hash_password("samepassword")
        assert h1 != h2

    def test_both_hashes_verify_correctly(self) -> None:
        h1 = hash_password("samepassword")
        h2 = hash_password("samepassword")
        assert verify_password("samepassword", h1) is True
        assert verify_password("samepassword", h2) is True


# ---------------------------------------------------------------------------
# JWT access tokens
# ---------------------------------------------------------------------------


class TestJWTTokens:
    def _sample_payload(self) -> dict:
        return {
            "sub": "00000000-0000-0000-0000-000000000001",
            "org": "00000000-0000-0000-0000-000000000002",
            "emp": "00000000-0000-0000-0000-000000000003",
            "role": "EMPLOYEE",
        }

    def test_create_access_token_returns_string(self) -> None:
        token = create_access_token(self._sample_payload())
        assert isinstance(token, str)
        assert len(token.split(".")) == 3  # header.payload.signature

    def test_decode_access_token_returns_payload(self) -> None:
        payload = self._sample_payload()
        token = create_access_token(payload)
        decoded = decode_access_token(token)
        assert decoded["sub"] == payload["sub"]
        assert decoded["org"] == payload["org"]
        assert decoded["role"] == payload["role"]
        assert decoded["type"] == "access"

    def test_invalid_token_raises_token_invalid_error(self) -> None:
        with pytest.raises(TokenInvalidError):
            decode_access_token("this.is.not.a.valid.jwt")

    def test_tampered_token_raises_token_invalid_error(self) -> None:
        token = create_access_token(self._sample_payload())
        tampered = token[:-5] + "XXXXX"
        with pytest.raises(TokenInvalidError):
            decode_access_token(tampered)

    def test_wrong_type_token_raises_token_invalid_error(self) -> None:
        """A refresh-type token should not be accepted as an access token."""
        payload = {**self._sample_payload(), "type": "refresh"}
        # Manually encode with the correct secret but wrong type
        raw = jwt.encode(
            {**payload, "exp": int(time.time()) + 3600},
            settings.JWT_SECRET_KEY,
            algorithm=settings.JWT_ALGORITHM,
        )
        with pytest.raises(TokenInvalidError):
            decode_access_token(raw)


# ---------------------------------------------------------------------------
# Opaque tokens (refresh / password reset)
# ---------------------------------------------------------------------------


class TestOpaqueTokens:
    def test_generate_opaque_token_returns_string(self) -> None:
        token = generate_opaque_token()
        assert isinstance(token, str)
        assert len(token) >= 20  # URL-safe base64, at least 20 chars for 32 bytes

    def test_two_generated_tokens_are_unique(self) -> None:
        t1 = generate_opaque_token()
        t2 = generate_opaque_token()
        assert t1 != t2

    def test_verify_opaque_token_success(self) -> None:
        token = generate_opaque_token()
        hashed = hash_opaque_token(token)
        assert verify_opaque_token(token, hashed) is True

    def test_verify_opaque_token_wrong_token(self) -> None:
        token = generate_opaque_token()
        hashed = hash_opaque_token(token)
        assert verify_opaque_token("wrongtoken", hashed) is False
