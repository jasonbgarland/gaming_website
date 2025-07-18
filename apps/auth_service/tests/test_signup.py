"""
Unit tests for the /signup endpoint.

# pylint: disable=R0801
"""

import unittest

from tests.test_base import TestDBBase


class TestSignupEndpoint(TestDBBase):
    """Unit tests for the /signup endpoint."""

    def test_signup_success(self):
        """Test /signup with valid data returns 201 and JWT token."""
        payload = {
            "username": "testuser",
            "email": "testuser@example.com",
            "password": "StrongPassword123",
        }
        response = self.client.post("/signup", json=payload)
        self.assertEqual(201, response.status_code)
        data = response.json()
        self.assertIn("access_token", data)
        self.assertEqual("bearer", data["token_type"])
        self.assertTrue(data["access_token"])  # Ensure token is not empty

    def test_duplicate_username(self):
        """Test /signup with duplicate username returns 409."""
        payload1 = {
            "username": "user1",
            "email": "user1@example.com",
            "password": "Password123",
        }
        self.client.post("/signup", json=payload1)
        payload2 = {
            "username": "user1",
            "email": "user2@example.com",
            "password": "Password123",
        }
        response = self.client.post("/signup", json=payload2)
        self.assertEqual(409, response.status_code)
        self.assertIn("Username already taken", response.json().get("detail", ""))

    def test_duplicate_email(self):
        """Test /signup with duplicate email returns 409."""
        payload1 = {
            "username": "user1",
            "email": "user1@example.com",
            "password": "Password123",
        }
        self.client.post("/signup", json=payload1)
        payload2 = {
            "username": "user2",
            "email": "user1@example.com",
            "password": "Password123",
        }
        response = self.client.post("/signup", json=payload2)
        self.assertEqual(409, response.status_code)
        self.assertIn("Email already registered", response.json().get("detail", ""))

    def test_missing_username(self):
        """Test /signup with missing username returns 422."""
        payload = {"email": "user@example.com", "password": "Password123"}
        response = self.client.post("/signup", json=payload)
        self.assertEqual(422, response.status_code)

    def test_missing_email(self):
        """Test /signup with missing email returns 422."""
        payload = {"username": "user1", "password": "Password123"}
        response = self.client.post("/signup", json=payload)
        self.assertEqual(422, response.status_code)

    def test_missing_password(self):
        """Test /signup with missing password returns 422."""
        payload = {"username": "user1", "email": "user@example.com"}
        response = self.client.post("/signup", json=payload)
        self.assertEqual(422, response.status_code)

    def test_invalid_email_format(self):
        """Test /signup with invalid email format returns 422."""
        payload = {
            "username": "user1",
            "email": "not-an-email",
            "password": "Password123",
        }
        response = self.client.post("/signup", json=payload)
        self.assertEqual(422, response.status_code)

    def test_password_too_short(self):
        """Test /signup with too short password returns 422."""
        payload = {
            "username": "user1",
            "email": "user@example.com",
            "password": "short",
        }
        response = self.client.post("/signup", json=payload)
        self.assertEqual(422, response.status_code)

    def test_username_too_short(self):
        """Test /signup with too short username returns 422."""
        payload = {
            "username": "a",
            "email": "user@example.com",
            "password": "Password123",
        }
        response = self.client.post("/signup", json=payload)
        self.assertEqual(422, response.status_code)

    def test_password_too_long(self):
        """Test /signup with too long password returns 422."""
        payload = {
            "username": "user1",
            "email": "user@example.com",
            "password": "a" * 129,
        }
        response = self.client.post("/signup", json=payload)
        self.assertEqual(422, response.status_code)

    def test_username_too_long(self):
        """Test /signup with too long username returns 422."""
        payload = {
            "username": "a" * 51,
            "email": "user@example.com",
            "password": "Password123",
        }
        response = self.client.post("/signup", json=payload)
        self.assertEqual(422, response.status_code)

    def test_password_not_returned(self):
        """Test /signup does not return password in response."""
        payload = {
            "username": "user1",
            "email": "user@example.com",
            "password": "Password123",
        }
        response = self.client.post("/signup", json=payload)
        self.assertNotIn("password", response.json())

    def test_case_sensitivity_username(self):
        """Test /signup allows case-sensitive usernames."""
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


if __name__ == "__main__":
    unittest.main()
