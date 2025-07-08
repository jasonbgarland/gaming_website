import unittest
from fastapi.testclient import TestClient
from db.models.user import Base
from tests.conftest import TestingSessionLocal, connection, pwd_context
from src.main import app
from src.api.auth import create_access_token


class TestMeEndpoint(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        Base.metadata.create_all(bind=connection)

    @classmethod
    def tearDownClass(cls):
        Base.metadata.drop_all(bind=connection)

    def setUp(self):
        self.client = TestClient(app)
        # Create a user for testing
        from db.models.user import User

        db = TestingSessionLocal()
        user = User(
            username="meuser",
            email="meuser@example.com",
            hashed_password=pwd_context.hash("MePass123"),
        )
        db.add(user)
        db.commit()
        db.close()

    def tearDown(self):
        from db.models.user import User

        db = TestingSessionLocal()
        db.query(User).delete()
        db.commit()
        db.close()

    def test_me_valid_token(self):
        token = create_access_token({"sub": "meuser"})
        headers = {"Authorization": f"Bearer {token}"}
        response = self.client.get("/me", headers=headers)
        self.assertEqual(200, response.status_code)
        data = response.json()
        self.assertEqual("meuser", data["username"])
        self.assertEqual("meuser@example.com", data["email"])

    def test_me_invalid_token(self):
        headers = {"Authorization": "Bearer invalidtoken"}
        response = self.client.get("/me", headers=headers)
        self.assertEqual(401, response.status_code)
        self.assertIn("Invalid token", response.json().get("detail", ""))

    def test_me_missing_token(self):
        response = self.client.get("/me")
        self.assertEqual(
            403, response.status_code
        )  # FastAPI returns 403 for missing credentials

    def test_me_expired_token(self):
        # time module import removed (was unused)
        from datetime import timedelta

        # Create a token that expires immediately
        token = create_access_token(
            {"sub": "meuser"}, expires_delta=timedelta(seconds=-1)
        )
        headers = {"Authorization": f"Bearer {token}"}
        response = self.client.get("/me", headers=headers)
        self.assertEqual(401, response.status_code)
        self.assertIn("expired", response.json().get("detail", "").lower())

    def test_me_user_deleted(self):
        # Issue token for user, then delete user
        token = create_access_token({"sub": "meuser"})
        from db.models.user import User

        db = TestingSessionLocal()
        db.query(User).filter(User.username == "meuser").delete()
        db.commit()
        db.close()
        headers = {"Authorization": f"Bearer {token}"}
        response = self.client.get("/me", headers=headers)
        self.assertEqual(404, response.status_code)
        self.assertIn("not found", response.json().get("detail", "").lower())

    def test_me_token_with_wrong_sub(self):
        token = create_access_token({"sub": "notarealuser"})
        headers = {"Authorization": f"Bearer {token}"}
        response = self.client.get("/me", headers=headers)
        self.assertEqual(404, response.status_code)
        self.assertIn("not found", response.json().get("detail", "").lower())

    def test_me_token_tampered(self):
        # Tamper with the token by changing a character
        token = create_access_token({"sub": "meuser"})
        tampered = token[:-1] + ("a" if token[-1] != "a" else "b")
        headers = {"Authorization": f"Bearer {tampered}"}
        response = self.client.get("/me", headers=headers)
        self.assertEqual(401, response.status_code)
        self.assertIn("invalid token", response.json().get("detail", "").lower())

    def test_me_token_wrong_secret(self):
        import jwt as pyjwt

        # Create a token with a different secret
        wrong_token = pyjwt.encode(
            {"sub": "meuser", "exp": 9999999999}, "wrongsecret", algorithm="HS256"
        )
        headers = {"Authorization": f"Bearer {wrong_token}"}
        response = self.client.get("/me", headers=headers)
        self.assertEqual(401, response.status_code)
        self.assertIn("invalid token", response.json().get("detail", "").lower())


if __name__ == "__main__":
    unittest.main()
