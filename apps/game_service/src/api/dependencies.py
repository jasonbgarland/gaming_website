"""
FastAPI dependencies for game_service API routes.
Includes DB session and user authentication.
"""

from typing import Dict

from fastapi import Depends, HTTPException, Request, status
from sqlalchemy.orm import Session

from apps.game_service.src.core.database import get_db
from apps.game_service.src.igdb.auth import IGDBAuth
from db.models.user import User
from shared.core.jwt_utils import decode_access_token


def get_current_user(request: Request, db: Session = Depends(get_db)) -> Dict:
    """
    Extract and validate JWT from Authorization header.
    Returns user info dict with integer 'id'.
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
        username = payload.get("sub")
        if not username:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token: missing username",
            )

        # Query database to get user ID from username
        user = db.query(User).filter(User.username == username).first()
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="User not found",
            )
        return {"id": user.id}  # Return integer user ID

    except HTTPException:
        raise
    except Exception as exc:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token"
        ) from exc


def get_igdb_auth() -> IGDBAuth:
    """
    Dependency that provides an IGDBAuth instance for IGDB API access.
    """
    return IGDBAuth()
