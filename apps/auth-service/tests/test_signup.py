import unittest
from fastapi.testclient import TestClient
from db.models.user import Base
from tests.conftest import connection
from src.main import app


class TestSignupEndpoint(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # Create all tables once for the shared connection
        Base.metadata.create_all(bind=connection)

    @classmethod
    def tearDownClass(cls):
        # Drop all tables after all tests
        Base.metadata.drop_all(bind=connection)

    def setUp(self):
        self.client = TestClient(app)

    def test_signup_success(self):
        payload = {
            "username": "testuser",
            "email": "testuser@example.com",
            "password": "StrongPassword123",
        }
        response = self.client.post("/signup", json=payload)
        self.assertEqual(201, response.status_code)
        data = response.json()
        self.assertEqual("testuser", data["username"])
        self.assertEqual("testuser@example.com", data["email"])
        self.assertNotIn("password", data)

    def test_duplicate_username(self):
        payload = {
            "username": "user1",
            "email": "user1@example.com",
            "password": "Password123",
        }
        self.client.post("/signup", json=payload)
        payload2 = {
            "username": "user1",
            "email": "user2@example.com",
            "password": "Password123",
        }
        response = self.client.post("/signup", json=payload2)
        self.assertEqual(409, response.status_code)
        self.assertIn("Username already taken", response.json().get("detail", ""))

    def test_duplicate_email(self):
        payload = {
            "username": "user1",
            "email": "user1@example.com",
            "password": "Password123",
        }
        self.client.post("/signup", json=payload)
        payload2 = {
            "username": "user2",
            "email": "user1@example.com",
            "password": "Password123",
        }
        response = self.client.post("/signup", json=payload2)
        self.assertEqual(409, response.status_code)
        self.assertIn("Email already registered", response.json().get("detail", ""))

    def test_missing_username(self):
        payload = {"email": "user@example.com", "password": "Password123"}
        response = self.client.post("/signup", json=payload)
        self.assertEqual(422, response.status_code)

    def test_missing_email(self):
        payload = {"username": "user1", "password": "Password123"}
        response = self.client.post("/signup", json=payload)
        self.assertEqual(422, response.status_code)

    def test_missing_password(self):
        payload = {"username": "user1", "email": "user@example.com"}
        response = self.client.post("/signup", json=payload)
        self.assertEqual(422, response.status_code)

    def test_invalid_email_format(self):
        payload = {
            "username": "user1",
            "email": "not-an-email",
            "password": "Password123",
        }
        response = self.client.post("/signup", json=payload)
        self.assertEqual(422, response.status_code)

    def test_password_too_short(self):
        payload = {
            "username": "user1",
            "email": "user@example.com",
            "password": "short",
        }
        response = self.client.post("/signup", json=payload)
        self.assertEqual(422, response.status_code)

    def test_username_too_short(self):
        payload = {
            "username": "a",
            "email": "user@example.com",
            "password": "Password123",
        }
        response = self.client.post("/signup", json=payload)
        self.assertEqual(422, response.status_code)

    def test_password_too_long(self):
        payload = {
            "username": "user1",
            "email": "user@example.com",
            "password": "a" * 129,
        }
        response = self.client.post("/signup", json=payload)
        self.assertEqual(422, response.status_code)

    def test_username_too_long(self):
        payload = {
            "username": "a" * 51,
            "email": "user@example.com",
            "password": "Password123",
        }
        response = self.client.post("/signup", json=payload)
        self.assertEqual(422, response.status_code)

    def test_password_not_returned(self):
        payload = {
            "username": "user1",
            "email": "user@example.com",
            "password": "Password123",
        }
        response = self.client.post("/signup", json=payload)
        self.assertNotIn("password", response.json())

    def test_case_sensitivity_username(self):
        payload1 = {
            "username": "User1",
            "email": "user1@example.com",
            "password": "Password123",
        }
        payload2 = {
            "username": "user1",
            "email": "user2@example.com",
            "password": "Password123",
        }
        self.client.post("/signup", json=payload1)
        response = self.client.post("/signup", json=payload2)
        # Should allow both if case-sensitive, else should block
        # Adjust this assertion if you want case-insensitive usernames
        self.assertEqual(201, response.status_code)


if __name__ == "__main__":
    unittest.main()
