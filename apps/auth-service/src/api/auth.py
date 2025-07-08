"""Authentication API endpoints for the Gaming Library Auth Service."""

import os
import logging
from datetime import datetime, timedelta, timezone
from fastapi import APIRouter, status, HTTPException, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from passlib.context import CryptContext
from sqlalchemy.orm import Session
import jwt
from jwt import PyJWTError, ExpiredSignatureError, InvalidTokenError
from db.models.user import User

# First-party imports (local to this service)
from src.core.database import get_db
from src.schemas.user_signup import UserSignup  # noqa: E0401
from src.schemas.user_login import UserLogin  # noqa: E0401
from src.schemas.user_out import UserOut  # noqa: E0401
from src.schemas.token_out import TokenOut  # noqa: E0401


# Configure logger for this module
logger = logging.getLogger("auth_service")
logging.basicConfig(level=logging.INFO)

# Password hashing context
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


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

# JWT decode/verify utility
security = HTTPBearer()

router = APIRouter()


def decode_access_token(token: str) -> dict:
    """Decode and validate a JWT access token."""
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except ExpiredSignatureError as exc:
        logger.warning("JWT expired: %s", token)
        raise HTTPException(status_code=401, detail="Token has expired") from exc
    except (InvalidTokenError, PyJWTError) as exc:
        logger.warning("Invalid JWT: %s", token)
        raise HTTPException(status_code=401, detail="Invalid token") from exc


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
    token = credentials.credentials
    payload = decode_access_token(token)
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
    response_model=UserOut,
    summary="Register a new user",
    tags=["auth"],
    responses={409: {"description": "Username or email already exists"}},
)
def signup(user: UserSignup, db: Session = Depends(get_db)) -> UserOut:
    """Register a new user account."""
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
    # Return user info (excluding password)
    return UserOut(username=db_user.username, email=db_user.email)


def create_access_token(data: dict, expires_delta: timedelta | None = None) -> str:
    """Create a JWT access token with an expiration."""
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + (
        expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    )
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


@router.post(
    "/login",
    response_model=TokenOut,
    summary="Authenticate and get JWT access token",
    tags=["auth"],
    responses={401: {"description": "Invalid username or password"}},
)
def login(user: UserLogin, db: Session = Depends(get_db)) -> TokenOut:
    """Authenticate user and return JWT access token."""
    db_user = db.query(User).filter(User.username == user.username).first()
    if not db_user or not pwd_context.verify(user.password, db_user.hashed_password):
        logger.info("Login failed for username: %s", user.username)
        raise HTTPException(status_code=401, detail="Invalid username or password")
    access_token = create_access_token({"sub": db_user.username})
    logger.info("User logged in: %s", user.username)
    return TokenOut(access_token=access_token, token_type="bearer")
