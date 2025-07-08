import unittest
from fastapi.testclient import TestClient
from db.models.user import Base
from tests.conftest import TestingSessionLocal, connection, pwd_context
from src.main import app


class TestLoginEndpoint(unittest.TestCase):
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
        # Create a user directly in the DB for login tests
        from db.models.user import User

        db = TestingSessionLocal()
        user = User(
            username="loginuser",
            email="loginuser@example.com",
            hashed_password=pwd_context.hash("LoginPass123"),
        )
        db.add(user)
        db.commit()
        db.close()

    def tearDown(self):
        # Clean up users after each test
        from db.models.user import User

        db = TestingSessionLocal()
        db.query(User).delete()
        db.commit()
        db.close()

    def test_login_success(self):
        payload = {"username": "loginuser", "password": "LoginPass123"}
        response = self.client.post("/login", json=payload)
        self.assertEqual(200, response.status_code)
        data = response.json()
        self.assertIn("access_token", data)
        self.assertEqual("bearer", data.get("token_type"))
        # Optionally: check JWT structure (header.payload.signature)
        token = data["access_token"]
        self.assertTrue(token.count(".") == 2)

    def test_login_wrong_password(self):
        payload = {"username": "loginuser", "password": "WrongPass"}
        response = self.client.post("/login", json=payload)
        self.assertEqual(401, response.status_code)
        self.assertIn("Invalid username or password", response.json().get("detail", ""))

    def test_login_nonexistent_user(self):
        payload = {"username": "doesnotexist", "password": "AnyPass123"}
        response = self.client.post("/login", json=payload)
        self.assertEqual(401, response.status_code)
        self.assertIn("Invalid username or password", response.json().get("detail", ""))

    def test_login_missing_username(self):
        payload = {"password": "LoginPass123"}
        response = self.client.post("/login", json=payload)
        self.assertEqual(422, response.status_code)

    def test_login_missing_password(self):
        payload = {"username": "loginuser"}
        response = self.client.post("/login", json=payload)
        self.assertEqual(422, response.status_code)


if __name__ == "__main__":
    unittest.main()
