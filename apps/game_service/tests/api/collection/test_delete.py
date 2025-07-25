"""
Tests for the delete collection API endpoints.
"""

# pylint: disable=duplicate-code,wrong-import-order

from tests.api.collection.test_base import BaseCollectionAPITest, generate_mock_jwt


class TestDeleteCollection(BaseCollectionAPITest):
    """
    Unit tests for the delete collection API route.

    This test class verifies the behavior of the `/collections/{collection_id}` DELETE endpoint
    for removing game collections. It includes tests for successful deletion,
    permissions, and not found cases.

    Inherits from BaseCollectionAPITest to utilize the test database setup and teardown.
    """

    def setUp(self):
        super().setUp()
        self.user_id = 1
        # Create user with id=1 already done in BaseCollectionAPITest

        # Create test collection for this user
        response = self.client.post(
            "/collections/",
            json={"name": "Collection to Delete", "description": "Will be deleted"},
            headers=self.headers,
        )
        self.assertEqual(response.status_code, 201)
        self.collection = response.json()
        self.collection_id = self.collection["id"]

        # Create a second user and their collection
        self.other_user_id = 2
        self.other_user_token = generate_mock_jwt(username="otheruser")
        self.add_user(
            username="otheruser",
            email="otheruser@example.com",
            password="$2b$12$KIXQJQbQhQJQbQhQJQbQhOQJQbQhQJQbQhQJQbQhQJQbQhQJQbQhO",
        )

        response = self.client.post(
            "/collections/",
            json={"name": "Other User Collection"},
            headers={"Authorization": self.other_user_token},
        )
        self.assertEqual(response.status_code, 201)
        self.other_collection = response.json()
        self.other_collection_id = self.other_collection["id"]

    def test_delete_collection_success(self):
        """Test deleting a collection successfully."""
        response = self.client.delete(
            f"/collections/{self.collection_id}",
            headers=self.headers,
        )
        self.assertEqual(response.status_code, 204)

        # Verify collection is gone
        get_response = self.client.get(
            f"/collections/{self.collection_id}",
            headers=self.headers,
        )
        self.assertEqual(get_response.status_code, 404)

    def test_delete_collection_not_found(self):
        """Test deleting a collection that doesn't exist."""
        response = self.client.delete(
            "/collections/9999",
            headers=self.headers,
        )
        self.assertEqual(response.status_code, 404)

    def test_delete_collection_unauthorized(self):
        """Test deleting a collection without authentication."""
        response = self.client.delete(
            f"/collections/{self.collection_id}",
        )
        self.assertEqual(response.status_code, 401)

        # Verify collection still exists
        get_response = self.client.get(
            f"/collections/{self.collection_id}",
            headers=self.headers,
        )
        self.assertEqual(get_response.status_code, 200)

    def test_delete_collection_wrong_user(self):
        """Test deleting a collection owned by another user."""
        response = self.client.delete(
            f"/collections/{self.other_collection_id}",
            headers=self.headers,
        )
        self.assertEqual(response.status_code, 404)

        # Verify collection still exists for the other user
        get_response = self.client.get(
            f"/collections/{self.other_collection_id}",
            headers={"Authorization": self.other_user_token},
        )
        self.assertEqual(get_response.status_code, 200)
