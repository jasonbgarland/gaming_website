"""
Unit tests for the /login endpoint.

# pylint: disable=duplicate-code, R0801
"""

import unittest

from tests.test_base import TestDBBase


class TestLoginEndpoint(TestDBBase):
    """Unit tests for the /login endpoint."""

    def setUp(self):
        super().setUp()
        # Create a user directly in the DB for login tests
        self.add_user(
            username="loginuser",
            email="loginuser@example.com",
            password="LoginPass123",
        )

    def test_login_success(self):
        """Test /login with correct credentials returns a token."""
        payload = {"email": "loginuser@example.com", "password": "LoginPass123"}
        response = self.client.post("/login", json=payload)
        self.assertEqual(200, response.status_code)
        data = response.json()
        self.assertIn("access_token", data)
        self.assertEqual("bearer", data.get("token_type"))
        # Optionally: check JWT structure (header.payload.signature)
        token = data["access_token"]
        self.assertTrue(token.count(".") == 2)

    def test_login_wrong_password(self):
        """Test /login with wrong password returns 401."""
        payload = {"email": "loginuser@example.com", "password": "WrongPass"}
        response = self.client.post("/login", json=payload)
        self.assertEqual(401, response.status_code)
        self.assertIn("Invalid email or password", response.json().get("detail", ""))

    def test_login_nonexistent_user(self):
        """Test /login with a non-existent user returns 401."""
        payload = {"email": "doesnotexist@example.com", "password": "AnyPass123"}
        response = self.client.post("/login", json=payload)
        self.assertEqual(401, response.status_code)
        self.assertIn("Invalid email or password", response.json().get("detail", ""))

    def test_login_missing_email(self):
        """Test /login with missing email returns 422."""
        payload = {"password": "LoginPass123"}
        response = self.client.post("/login", json=payload)
        self.assertEqual(422, response.status_code)

    def test_login_missing_password(self):
        """Test /login with missing password returns 422."""
        payload = {"email": "loginuser@example.com"}
        response = self.client.post("/login", json=payload)
        self.assertEqual(422, response.status_code)


if __name__ == "__main__":
    unittest.main()
