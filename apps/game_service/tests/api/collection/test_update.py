"""
Tests for the update collection API endpoints.
"""

# pylint: disable=duplicate-code,wrong-import-order

from tests.api.collection.test_base import BaseCollectionAPITest, generate_mock_jwt


class TestUpdateCollection(BaseCollectionAPITest):
    """
    Unit tests for the update collection API route.

    This test class verifies the behavior of the `/collections/{collection_id}` PUT endpoint
    for updating game collections. It includes tests for successful updates,
    validation errors, permissions, and not found cases.

    Inherits from BaseCollectionAPITest to utilize the test database setup and teardown.
    """

    def setUp(self):
        super().setUp()
        self.user_id = 1
        # Create user with id=1 already done in BaseCollectionAPITest

        # Create test collection for this user
        response = self.client.post(
            "/collections/",
            json={"name": "Original Collection", "description": "Original description"},
            headers=self.headers,
        )
        self.assertEqual(response.status_code, 201)
        self.collection = response.json()
        self.collection_id = self.collection["id"]

        # Create a second user and their collection
        self.other_user_id = 2
        self.other_user_token = generate_mock_jwt(username="otheruser")
        # Create user with ID 2 (test setup will use this ID)
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

    def test_update_collection_success(self):
        """Test updating a collection successfully."""
        payload = {"name": "Updated Collection", "description": "Updated description"}
        response = self.client.put(
            f"/collections/{self.collection_id}",
            json=payload,
            headers=self.headers,
        )
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data["name"], "Updated Collection")
        self.assertEqual(data["description"], "Updated description")
        self.assertEqual(data["id"], self.collection_id)
        self.assertEqual(data["user_id"], self.user_id)

    def test_update_collection_partial(self):
        """Test updating only name of a collection."""
        payload = {"name": "New Name Only"}
        response = self.client.put(
            f"/collections/{self.collection_id}",
            json=payload,
            headers=self.headers,
        )
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data["name"], "New Name Only")
        self.assertEqual(data["description"], self.collection["description"])

    def test_update_collection_description_only(self):
        """Test updating only description of a collection."""
        payload = {"description": "New description only"}
        response = self.client.put(
            f"/collections/{self.collection_id}",
            json=payload,
            headers=self.headers,
        )
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data["name"], self.collection["name"])
        self.assertEqual(data["description"], "New description only")

    def test_update_collection_not_found(self):
        """Test updating a collection that doesn't exist."""
        payload = {"name": "Updated Collection"}
        response = self.client.put(
            "/collections/9999",
            json=payload,
            headers=self.headers,
        )
        self.assertEqual(response.status_code, 404)

    def test_update_collection_duplicate_name(self):
        """Test updating a collection with a name that already exists for the user."""
        # First create another collection with a different name
        response = self.client.post(
            "/collections/",
            json={"name": "Another Collection"},
            headers=self.headers,
        )
        self.assertEqual(response.status_code, 201)
        # Now try to update the first collection with the name of the second
        payload = {"name": "Another Collection"}
        response = self.client.put(
            f"/collections/{self.collection_id}",
            json=payload,
            headers=self.headers,
        )
        self.assertEqual(response.status_code, 409)
        # Verify the collection wasn't updated
        get_response = self.client.get(
            f"/collections/{self.collection_id}",
            headers=self.headers,
        )
        # If the update failed, the collection should still exist and have the original name
        if get_response.status_code == 200:
            self.assertEqual(get_response.json()["name"], "Original Collection")
        else:
            # If not found, check for error detail
            self.assertIn("detail", get_response.json())

    def test_update_collection_unauthorized(self):
        """Test updating a collection without authentication."""
        payload = {"name": "Updated Collection"}
        response = self.client.put(
            f"/collections/{self.collection_id}",
            json=payload,
        )
        self.assertEqual(response.status_code, 401)

    def test_update_collection_wrong_user(self):
        """Test updating a collection owned by another user."""
        payload = {"name": "Trying to update"}
        response = self.client.put(
            f"/collections/{self.other_collection_id}",
            json=payload,
            headers=self.headers,
        )
        self.assertEqual(response.status_code, 404)

    def test_update_collection_validation_error(self):
        """Test updating a collection with invalid data."""
        # Test with too long name
        long_name = "A" * 200  # Longer than the 100 char limit
        payload = {"name": long_name}
        response = self.client.put(
            f"/collections/{self.collection_id}",
            json=payload,
            headers=self.headers,
        )
        self.assertEqual(response.status_code, 422)
