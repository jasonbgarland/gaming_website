"""
Pytest/Unittest DB setup for game_service tests.
Provides a shared connection and session factory for reliable test isolation.
"""

import os

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from apps.game_service.src.core.database import get_db
from apps.game_service.src.main import app

# Use in-memory SQLite DB for test isolation (consistent with auth_service)
TEST_DB_URL = "sqlite:///:memory:"
os.environ["GAME_SERVICE_DATABASE_URL"] = TEST_DB_URL

engine = create_engine(TEST_DB_URL, connect_args={"check_same_thread": False})
connection = engine.connect()
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=connection)


# Dependency override for FastAPI to use the shared test DB session
def override_get_db():
    """
    Provides a database session for testing purposes.
    This method overrides the default FastAPI dependency to use an in-memory SQLite database.
    Ensures reliable test isolation by creating and closing a session for each test.
    """
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db
