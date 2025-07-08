"""Database connection and session utilities for auth-service."""

from typing import Generator
import os

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session


# Load the database URL from environment or config, default to SQLite in-memory for tests
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///:memory:")

# Create the SQLAlchemy engine
engine = create_engine(DATABASE_URL, pool_pre_ping=True)

# Create a configured "Session" class
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


# Dependency for FastAPI routes
def get_db() -> Generator[Session, None, None]:
    """Yield a database session for use in FastAPI dependency injection."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
