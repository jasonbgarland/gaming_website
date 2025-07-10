"""
Test configuration and fixtures for the authentication service.
"""

from passlib.context import CryptContext
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# from db.models.user import Base  # noqa: F401
from src.main import app
from src.core.database import get_db

SQLALCHEMY_TEST_DATABASE_URL = "sqlite:///:memory:"

# Shared engine and connection for all tests
engine = create_engine(
    SQLALCHEMY_TEST_DATABASE_URL, connect_args={"check_same_thread": False}
)
connection = engine.connect()
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=connection)

# Password hashing context (should match app's)
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def override_get_db():
    """Override for FastAPI dependency to use the test database session."""
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


# pylint: disable=duplicate-code
app.dependency_overrides[get_db] = override_get_db
