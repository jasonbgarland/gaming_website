"""
JWT utility functions and constants for Gaming Library services.
Shared by all services needing JWT authentication.
"""

import os
from datetime import datetime, timedelta, timezone

import jwt
from jwt import (
    DecodeError,
    ExpiredSignatureError,
    InvalidSignatureError,
    InvalidTokenError,
    PyJWTError,
)

# JWT settings
SECRET_KEY = os.environ.get("JWT_SECRET_KEY")
if not SECRET_KEY or SECRET_KEY == "dev-secret-key":
    env = os.environ.get("ENV", "development").lower()
    if env not in ("dev", "development", "test", "testing"):
        raise RuntimeError(
            "JWT_SECRET_KEY environment variable must be set in production!"
        )
    SECRET_KEY = "dev-secret-key"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.environ.get("ACCESS_TOKEN_EXPIRE_MINUTES", 30))


def create_access_token(data: dict, expires_delta: timedelta | None = None) -> str:
    """Create a JWT access token with an expiration."""
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + (
        expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    )
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


def decode_access_token(token: str) -> dict:
    """Decode and validate a JWT access token."""
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except ExpiredSignatureError:
        # Let this propagate to the route handler
        raise
    except (InvalidTokenError, PyJWTError, InvalidSignatureError, DecodeError) as exc:
        raise PyJWTError("Invalid token") from exc
