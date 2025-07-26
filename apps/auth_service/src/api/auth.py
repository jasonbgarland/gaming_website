"""Authentication API endpoints for the Gaming Library Auth Service."""

import logging

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jwt import ExpiredSignatureError
from passlib.context import CryptContext
from sqlalchemy.orm import Session
from src.core.database import get_db
from src.schemas.token_out import TokenOut  # noqa: E0401
from src.schemas.user_login import UserLogin  # noqa: E0401
from src.schemas.user_out import UserOut  # noqa: E0401
from src.schemas.user_signup import UserSignup  # noqa: E0401

# pylint: disable=wrong-import-order
from db.models.user import User
from shared.core.jwt_utils import create_access_token, decode_access_token

# Configure logger for this module
logger = logging.getLogger("auth_service")
logging.basicConfig(level=logging.INFO)

# Password hashing context
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

router = APIRouter()
security = HTTPBearer()


@router.get(
    "/me",
    response_model=UserOut,
    summary="Get current user info",
    tags=["auth"],
    responses={
        401: {"description": "Invalid or expired token"},
        404: {"description": "User not found"},
    },
)
def read_me(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db),
) -> UserOut:
    """Return info about the authenticated user."""
    # Extract JWT from Authorization header
    token = credentials.credentials
    try:
        payload = decode_access_token(token)
    except ExpiredSignatureError as exc:
        logger.warning("JWT expired in /me: %s", exc)
        raise HTTPException(status_code=401, detail="Token has expired") from exc
    except Exception as exc:
        logger.warning("JWT error in /me: %s", exc)
        raise HTTPException(status_code=401, detail="Invalid token") from exc
    if not isinstance(payload, dict):
        logger.warning("JWT payload is not a dict: %s", payload)
        raise HTTPException(status_code=401, detail="Invalid token")
    username = payload.get("sub")
    if not username:
        logger.warning("JWT missing 'sub' claim: %s", token)
        raise HTTPException(status_code=401, detail="Invalid token payload")
    user = db.query(User).filter(User.username == username).first()
    if not user:
        logger.info("User not found for token sub: %s", username)
        raise HTTPException(status_code=404, detail="User not found")
    logger.info("/me accessed by user: %s", username)
    return UserOut(username=user.username, email=user.email)


@router.post(
    "/signup",
    status_code=status.HTTP_201_CREATED,
    response_model=TokenOut,
    summary="Register a new user and return JWT access token",
    tags=["auth"],
    responses={409: {"description": "Username or email already exists"}},
)
def signup(user: UserSignup, db: Session = Depends(get_db)) -> TokenOut:
    """Register a new user account and return JWT access token."""
    # Check for duplicate username first
    existing_username = db.query(User).filter(User.username == user.username).first()
    if existing_username:
        logger.info("Signup failed: username already taken (%s)", user.username)
        raise HTTPException(status_code=409, detail="Username already taken")
    # Then check for duplicate email
    existing_email = db.query(User).filter(User.email == user.email).first()
    if existing_email:
        logger.info("Signup failed: email already registered (%s)", user.email)
        raise HTTPException(status_code=409, detail="Email already registered")

    # Hash the password
    hashed_password = pwd_context.hash(user.password)
    db_user = User(
        username=user.username, email=user.email, hashed_password=hashed_password
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    logger.info("New user signed up: %s", user.username)

    # Create and return JWT access token (like login)
    access_token = create_access_token({"sub": db_user.username})
    logger.info("JWT token created for new user: %s", user.username)
    return TokenOut(access_token=access_token, token_type="bearer")


@router.post(
    "/login",
    response_model=TokenOut,
    summary="Authenticate and get JWT access token",
    tags=["auth"],
    responses={401: {"description": "Invalid email or password"}},
)
def login(user: UserLogin, db: Session = Depends(get_db)) -> TokenOut:
    """Authenticate user and return JWT access token."""
    # Find user by email
    db_user = db.query(User).filter(User.email == user.email).first()

    if not db_user or not pwd_context.verify(user.password, db_user.hashed_password):
        logger.info("Login failed for email: %s", user.email)
        raise HTTPException(status_code=401, detail="Invalid email or password")
    access_token = create_access_token({"sub": db_user.username})
    logger.info("User logged in: %s (email: %s)", db_user.username, user.email)
    return TokenOut(access_token=access_token, token_type="bearer")
