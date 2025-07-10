"""
Base class for shared DB setup/teardown logic in auth-service tests.
"""

import unittest
from fastapi.testclient import TestClient
from db.models.user import Base, User
from tests.conftest import TestingSessionLocal, connection, pwd_context
from src.main import app


class TestDBBase(unittest.TestCase):
    """Base test class for DB setup/teardown and user helpers."""

    @classmethod
    def setUpClass(cls):
        Base.metadata.create_all(bind=connection)

    @classmethod
    def tearDownClass(cls):
        Base.metadata.drop_all(bind=connection)

    def setUp(self):
        self.client = TestClient(app)
        self._test_users = []  # Track created users for cleanup

    def add_user(self, username: str, email: str, password: str) -> User:
        """Add a user to the test database and track for cleanup."""
        db = TestingSessionLocal()
        user = User(
            username=username,
            email=email,
            hashed_password=pwd_context.hash(password),
        )
        db.add(user)
        db.commit()
        db.refresh(user)
        db.close()
        self._test_users.append(username)
        return user

    def tearDown(self):
        db = TestingSessionLocal()
        for username in self._test_users:
            db.query(User).filter(User.username == username).delete()
        db.commit()
        db.close()
        self._test_users.clear()
