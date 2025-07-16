"""
Unit tests for the /me endpoint (user info retrieval).

# pylint: disable=duplicate-code, R0801
"""

import unittest
from datetime import timedelta
import jwt as pyjwt
from sqlalchemy import text
from tests.test_base import TestDBBase
from tests.conftest import TestingSessionLocal
from src.api.auth import create_access_token


class TestMeEndpoint(TestDBBase):
    """Unit tests for the /me endpoint (user info retrieval)."""

    def setUp(self):
        super().setUp()
        # Ensure no duplicate user exists before adding
        db = TestingSessionLocal()
        db.execute(text("DELETE FROM users WHERE username = 'meuser'"))
        db.commit()
        db.close()
        self.add_user(
            username="meuser",
            email="meuser@example.com",
            password="MePass123",
        )

    def test_me_valid_token(self):
        """Test /me with a valid token returns user info."""
        token = create_access_token({"sub": "meuser"})
        headers = {"Authorization": f"Bearer {token}"}
        response = self.client.get("/me", headers=headers)
        self.assertEqual(200, response.status_code)
        data = response.json()
        self.assertEqual("meuser", data["username"])
        self.assertEqual("meuser@example.com", data["email"])

    def test_me_invalid_token(self):
        """Test /me with an invalid token returns 401."""
        headers = {"Authorization": "Bearer invalidtoken"}
        response = self.client.get("/me", headers=headers)
        self.assertEqual(401, response.status_code)
        self.assertIn("Invalid token", response.json().get("detail", ""))

    def test_me_missing_token(self):
        """Test /me with no token returns 403."""
        response = self.client.get("/me")
        self.assertEqual(
            403, response.status_code
        )  # FastAPI returns 403 for missing credentials

    def test_me_expired_token(self):
        """Test /me with an expired token returns 401."""
        # Create a token that expires immediately
        token = create_access_token(
            {"sub": "meuser"}, expires_delta=timedelta(seconds=-1)
        )
        headers = {"Authorization": f"Bearer {token}"}
        response = self.client.get("/me", headers=headers)
        self.assertEqual(401, response.status_code)
        self.assertIn("expired", response.json().get("detail", "").lower())

    def test_me_user_deleted(self):
        """Test /me with a token for a deleted user returns 404."""
        # Issue token for user, then delete user
        token = create_access_token({"sub": "meuser"})
        # Use the base class's cleanup logic
        self._test_users.clear()  # Remove from tracking so tearDown doesn't try to delete again
        db = TestingSessionLocal()
        db.execute(text("DELETE FROM users WHERE username = 'meuser'"))
        db.commit()
        db.close()
        headers = {"Authorization": f"Bearer {token}"}
        response = self.client.get("/me", headers=headers)
        self.assertEqual(404, response.status_code)
        self.assertIn("not found", response.json().get("detail", "").lower())

    def test_me_token_with_wrong_sub(self):
        """Test /me with a token for a non-existent user returns 404."""
        token = create_access_token({"sub": "notarealuser"})
        headers = {"Authorization": f"Bearer {token}"}
        response = self.client.get("/me", headers=headers)
        self.assertEqual(404, response.status_code)
        self.assertIn("not found", response.json().get("detail", "").lower())

    def test_me_token_tampered(self):
        """Test /me with a tampered token returns 401."""
        # Tamper with the token by changing a character
        token = create_access_token({"sub": "meuser"})
        tampered = token[:-1] + ("a" if token[-1] != "a" else "b")
        headers = {"Authorization": f"Bearer {tampered}"}
        response = self.client.get("/me", headers=headers)
        self.assertEqual(401, response.status_code)
        self.assertIn("invalid token", response.json().get("detail", "").lower())

    def test_me_token_wrong_secret(self):
        """Test /me with a token signed with the wrong secret returns 401."""
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
