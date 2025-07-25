"""
Base test class with database setup and utilities for game_service tests.
"""

# pylint: disable=wrong-import-order

import unittest

from fastapi.testclient import TestClient
from src.main import app
from tests.conftest import TestingSessionLocal, connection

from db.models.collection import Collection
from db.models.user import Base, User
from shared.core.jwt_utils import create_access_token


def generate_mock_jwt(username: str = "testuser") -> str:
    """
    Generate a mock JWT for testing purposes.

    Args:
        username (str): The username to include in the JWT payload. Defaults to "testuser".

    Returns:
        str: A mock JWT string prefixed with "Bearer ".
    """
    token = create_access_token({"sub": username})
    return f"Bearer {token}"


class TestDBBase(unittest.TestCase):
    """Base test class for DB setup/teardown and user helpers."""

    @classmethod
    def setUpClass(cls):
        Base.metadata.create_all(bind=connection)

    @classmethod
    def tearDownClass(cls):
        Base.metadata.drop_all(bind=connection)

    def setUp(self):
        # Drop and recreate all tables for full isolation
        Base.metadata.drop_all(bind=connection)
        Base.metadata.create_all(bind=connection)
        # Explicitly commit the table creation
        connection.commit()
        self.client = TestClient(app)
        self._test_users = []  # Track created users for cleanup

    def add_user(self, username: str, email: str, password: str = "testpass") -> User:
        """Add a user to the test database and track for cleanup."""
        db = TestingSessionLocal()
        user = User(
            username=username,
            email=email,
            hashed_password=password,  # Store plain password for testing
        )
        db.add(user)
        db.commit()
        db.refresh(user)
        db.close()
        self._test_users.append(username)
        return user

    def add_collection(self, user_id: int, name: str, description: str = None):
        """
        Add a collection to the test database and return the collection object.
        Args:
            user_id (int): The user ID who owns the collection.
            name (str): The name of the collection.
            description (str, optional): The description of the collection.
        Returns:
            Collection: The created collection object.
        """

        db = TestingSessionLocal()
        collection = Collection(
            user_id=user_id,
            name=name,
            description=description,
        )
        db.add(collection)
        db.commit()
        db.refresh(collection)
        db.close()
        return collection

    def tearDown(self):
        db = TestingSessionLocal()
        for username in self._test_users:
            db.query(User).filter(User.username == username).delete()
        db.commit()
        db.close()
        self._test_users.clear()
        db.close()
        self._test_users.clear()
        db.close()
        self._test_users.clear()
