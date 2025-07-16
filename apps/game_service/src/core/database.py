"""
Database connection and session utilities for game_service.
"""

import os
from typing import Generator

from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker


def get_engine():
    """Create a SQLAlchemy engine using the current environment variable."""
    db_url = os.getenv("GAME_SERVICE_DATABASE_URL", "sqlite:///:memory:")
    return create_engine(db_url, pool_pre_ping=True)


def get_session_local():
    """Create a sessionmaker bound to a fresh engine."""
    engine = get_engine()
    return sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db() -> Generator[Session, None, None]:
    """Yield a database session for use in FastAPI dependency injection."""
    session_local = get_session_local()
    db = session_local()
    try:
        yield db
    finally:
        db.close()
