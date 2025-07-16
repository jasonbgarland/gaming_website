"""
FastAPI dependencies for game_service API routes.
Includes DB session and user authentication.
"""

from typing import Dict

from fastapi import HTTPException, Request, status

from apps.game_service.src.igdb.auth import IGDBAuth
from shared.core.jwt_utils import decode_access_token


def get_current_user(request: Request) -> Dict:
    """
    Extract and validate JWT from Authorization header.
    Returns user info dict (at minimum, 'id').
    """
    auth_header = request.headers.get("Authorization")
    if not auth_header or not auth_header.startswith("Bearer "):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Missing or invalid Authorization header",
        )
    token = auth_header.split(" ", 1)[1]
    try:
        payload = decode_access_token(token)
        user_id = payload.get("sub")
        if not user_id:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token: missing user id",
            )
        return {"id": user_id}
    except Exception as exc:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token"
        ) from exc


def get_igdb_auth() -> IGDBAuth:
    """
    Dependency that provides an IGDBAuth instance for IGDB API access.
    """
    return IGDBAuth()
