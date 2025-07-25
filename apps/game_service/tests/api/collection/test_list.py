"""
Tests for the list collections API endpoints.
"""

# pylint: disable=duplicate-code,wrong-import-order

from unittest.mock import patch

from tests.api.collection.test_base import BaseCollectionAPITest, generate_mock_jwt


class TestListCollections(BaseCollectionAPITest):
    """Unit tests for GET /collections/ API route."""

    def test_list_collections_returns_user_collections(self):
        """Should return only collections belonging to the authenticated user."""
        # Create test collections for the user
        payload1 = {"name": "Library", "description": "My main game collection"}
        payload2 = {"name": "Backlog", "description": "Games to play later"}
        self.client.post("/collections/", json=payload1, headers=self.headers)
        self.client.post("/collections/", json=payload2, headers=self.headers)

        # Get collections
        response = self.client.get("/collections/", headers=self.headers)
        self.assertEqual(response.status_code, 200)

        # Verify response
        data = response.json()
        self.assertEqual(len(data), 2)
        names = [c["name"] for c in data]
        self.assertIn("Library", names)
        self.assertIn("Backlog", names)

    def test_list_collections_returns_empty_for_no_collections(self):
        """Should return an empty list if user has no collections."""
        response = self.client.get("/collections/", headers=self.headers)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), [])

    def test_list_collections_unauthenticated(self):
        """Test listing collections without authentication."""
        response = self.client.get("/collections/")
        self.assertEqual(response.status_code, 401)

    def test_list_collections_unusual_names(self):
        """Should handle collections with valid unusual names and max length."""
        payloads = [
            {"name": "My Games", "description": "Valid name"},
            {"name": "A" * 100, "description": "Max length name"},
            {"name": "Games 123", "description": "Numbers and spaces"},
        ]
        for payload in payloads:
            resp = self.client.post("/collections/", json=payload, headers=self.headers)
            print(
                f"POST {payload['name']} status: {resp.status_code}, response: {resp.text}"
            )
            self.assertEqual(
                resp.status_code,
                201,
                f"Failed to create: {payload['name']}, got {resp.text}",
            )
        response = self.client.get("/collections/", headers=self.headers)
        self.assertEqual(response.status_code, 200)
        names = [c["name"] for c in response.json()]
        self.assertIn("My Games", names)
        self.assertIn("A" * 100, names)
        self.assertIn("Games 123", names)

    def test_list_collections_name_too_long(self):
        """Should not allow collection names longer than 100 characters."""
        long_name = "B" * 101
        payload = {"name": long_name, "description": "Too long"}
        resp = self.client.post("/collections/", json=payload, headers=self.headers)
        print(
            f"POST {long_name[:10]}... status: {resp.status_code}, response: {resp.text}"
        )
        self.assertEqual(resp.status_code, 422)

    def test_list_collections_db_failure(self):
        """Should return 500 if DB error occurs."""
        with patch(
            "apps.game_service.src.services.collection_service.CollectionService.list_collections",
            side_effect=Exception("DB fail"),
        ):
            response = self.client.get("/collections/", headers=self.headers)
            self.assertEqual(response.status_code, 500)
            self.assertIn("error", response.text.lower())

    def test_list_collections_multiple_users(self):
        """Should only return collections for the authenticated user."""
        # Create collections for user 1
        self.client.post(
            "/collections/", json={"name": "User1Coll"}, headers=self.headers
        )
        # Create a second user and collection
        self.add_user(
            username="otheruser",
            email="otheruser@example.com",
            password="$2b$12$KIXQJQbQhQJQbQhQJQbQhQJQbQhQJQbQhQJQbQhQJQbQhQJQbQhO",
        )
        second_jwt = generate_mock_jwt(username="otheruser")
        second_headers = {"Authorization": second_jwt}
        self.client.post(
            "/collections/", json={"name": "User2Coll"}, headers=second_headers
        )
        # User 1 should only see their own collection
        response = self.client.get("/collections/", headers=self.headers)
        self.assertEqual(response.status_code, 200)
        names = [c["name"] for c in response.json()]
        self.assertIn("User1Coll", names)
        self.assertNotIn("User2Coll", names)
