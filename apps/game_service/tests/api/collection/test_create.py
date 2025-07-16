"""
Tests for the create collection API endpoints.
"""

# pylint: disable=duplicate-code,wrong-import-order

from apps.game_service.tests.api.collection.test_base import BaseCollectionAPITest


class TestCreateCollection(BaseCollectionAPITest):
    """
    Unit tests for the create collection API route.

    This test class verifies the behavior of the `/collections/` endpoint
    for creating game collections. It includes tests for successful creation,
    validation errors, and authentication requirements.

    Inherits from BaseCollectionAPITest to utilize the test database setup and teardown.
    """

    def test_create_collection_success(self):
        """Test creating a new collection via API."""
        payload = {"name": "Library", "description": "My main game collection"}
        response = self.client.post("/collections/", json=payload, headers=self.headers)
        self.assertEqual(response.status_code, 201)
        data = response.json()
        self.assertEqual(data["name"], "Library")
        self.assertEqual(data["description"], "My main game collection")
        self.assertIn("id", data)
        self.assertIn("user_id", data)

    def test_create_collection_missing_name(self):
        """Test creating a collection with missing name."""
        payload = {"description": "No name"}
        response = self.client.post("/collections/", json=payload, headers=self.headers)
        self.assertEqual(
            response.status_code, 422
        )  # FastAPI returns 422 for validation errors

    def test_create_collection_unauthenticated(self):
        """Test creating a collection without authentication."""
        payload = {"name": "Library"}
        response = self.client.post("/collections/", json=payload)
        self.assertEqual(response.status_code, 401)

    def test_create_collection_duplicate_name(self):
        """Test creating two collections with the same name for the same user."""
        payload = {"name": "Library", "description": "First collection"}
        response1 = self.client.post(
            "/collections/", json=payload, headers=self.headers
        )
        self.assertEqual(response1.status_code, 201)
        response2 = self.client.post(
            "/collections/", json=payload, headers=self.headers
        )
        # Expecting 400 or 409 depending on API design; adjust as needed
        self.assertIn(response2.status_code, [400, 409])

    def test_create_collection_name_too_long(self):
        """Test creating a collection with a name exceeding allowed length."""
        long_name = "A" * 300  # Adjust length to match schema constraint
        payload = {"name": long_name, "description": "Too long name"}
        response = self.client.post("/collections/", json=payload, headers=self.headers)
        self.assertEqual(response.status_code, 422)

    def test_create_collection_description_too_long(self):
        """Test creating a collection with a description exceeding allowed length."""
        long_description = "D" * 2000  # Adjust length to match schema constraint
        payload = {"name": "Library", "description": long_description}
        response = self.client.post("/collections/", json=payload, headers=self.headers)
        self.assertEqual(response.status_code, 422)

    def test_create_collection_empty_name(self):
        """Test creating a collection with an empty name."""
        payload = {"name": "", "description": "Empty name"}
        response = self.client.post("/collections/", json=payload, headers=self.headers)
        self.assertEqual(response.status_code, 422)

    def test_create_collection_invalid_characters_in_name(self):
        """Test creating a collection with invalid/special characters in the name."""
        payload = {"name": "Lib@ry!", "description": "Invalid chars"}
        response = self.client.post("/collections/", json=payload, headers=self.headers)
        self.assertEqual(response.status_code, 422)

    def test_create_collection_missing_description(self):
        """Test creating a collection with only a name (description optional)."""
        payload = {"name": "NoDescription"}
        response = self.client.post("/collections/", json=payload, headers=self.headers)
        # If description is optional, expect success
        self.assertEqual(response.status_code, 201)

    def test_create_collection_non_json_payload(self):
        """Test creating a collection with a non-JSON payload."""
        response = self.client.post(
            "/collections/", content="name=Library", headers=self.headers
        )
        self.assertIn(response.status_code, [400, 422])

    def test_create_collection_extra_fields(self):
        """Test creating a collection with extra, unexpected fields in the payload."""
        payload = {
            "name": "Library",
            "description": "Extra fields",
            "extra": "unexpected",
        }
        response = self.client.post("/collections/", json=payload, headers=self.headers)
        # If extra fields are ignored, expect success; otherwise, expect validation error
        self.assertIn(response.status_code, [201, 422])
