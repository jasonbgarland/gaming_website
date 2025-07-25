"""
Pytest/Unittest DB setup for game_service tests.
Provides a shared connection and session factory for reliable test isolation.
"""

import atexit
import os

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from src.core.database import get_db
from src.main import app

# Use file-based SQLite DB for test isolation to avoid connection issues
TEST_DB_FILE = "test_game_service.db"
TEST_DB_URL = f"sqlite:///{TEST_DB_FILE}"
os.environ["GAME_SERVICE_DATABASE_URL"] = TEST_DB_URL

engine = create_engine(TEST_DB_URL, connect_args={"check_same_thread": False})
connection = engine.connect()
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=connection)


def cleanup_test_database():
    """
    Clean up the test database file after all tests complete.
    This function is registered with atexit to ensure cleanup happens.
    """
    try:
        if connection:
            connection.close()
        if engine:
            engine.dispose()
        if os.path.exists(TEST_DB_FILE):
            os.remove(TEST_DB_FILE)
            print(f"✓ Cleaned up test database: {TEST_DB_FILE}")
    except (OSError, AttributeError) as e:
        print(f"⚠ Warning: Could not clean up test database {TEST_DB_FILE}: {e}")


# Register cleanup to run when Python exits
atexit.register(cleanup_test_database)


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
