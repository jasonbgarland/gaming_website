"""
Tests for the DELETE collection entry API endpoints.
"""

# pylint: disable=duplicate-code, wrong-import-order

from unittest.mock import Mock, patch

from tests.api.collection_entry.test_base import (
    BaseCollectionEntryAPITest,
    generate_mock_jwt,
)
from tests.conftest import TestingSessionLocal
from tests.utils import MOCK_IGDB_GAME, setup_mock_igdb_client

from db.models.collection import Collection


class TestDeleteCollectionEntry(BaseCollectionEntryAPITest):
    """Test cases for DELETE /collections/{collection_id}/entries/{entry_id} endpoint."""

    @patch("src.api.collection_entry.IGDBClient")
    def test_delete_entry_success(self, mock_igdb_client_class):
        """
        Should delete a collection entry successfully.
        """
        mock_igdb_client = Mock()
        setup_mock_igdb_client(mock_igdb_client, MOCK_IGDB_GAME)
        mock_igdb_client_class.return_value = mock_igdb_client

        # First create an entry
        data = {"game_id": 1, "notes": "To delete"}
        create_response = self.client.post(
            f"/collections/{self.test_collection.id}/entries/",
            json=data,
            headers=self.headers,
        )
        self.assertEqual(create_response.status_code, 201)
        entry_id = create_response.json()["id"]

        # Now delete the entry
        delete_response = self.client.delete(
            f"/collections/{self.test_collection.id}/entries/{entry_id}",
            headers=self.headers,
        )

        # Verify response
        self.assertEqual(delete_response.status_code, 204)
        self.assertEqual(delete_response.text, "")

        # Verify entry is gone by trying to get it
        get_response = self.client.get(
            f"/collections/{self.test_collection.id}/entries/{entry_id}",
            headers=self.headers,
        )
        self.assertEqual(get_response.status_code, 404)

    def test_delete_entry_unauthorized(self):
        """
        Should return 401 Unauthorized if no JWT is provided.
        """
        response = self.client.delete(
            f"/collections/{self.test_collection.id}/entries/1",
            # No headers
        )
        self.assertEqual(response.status_code, 401)

    def test_delete_entry_invalid_collection_id(self):
        """
        Should return 422 Unprocessable Entity for invalid collection_id.
        """
        response = self.client.delete(
            "/collections/abc/entries/1",  # Invalid ID (not an integer)
            headers=self.headers,
        )
        self.assertEqual(response.status_code, 422)

    def test_delete_entry_invalid_entry_id(self):
        """
        Should return 422 Unprocessable Entity for invalid entry_id.
        """
        response = self.client.delete(
            f"/collections/{self.test_collection.id}/entries/abc",  # Invalid ID (not an integer)
            headers=self.headers,
        )
        self.assertEqual(response.status_code, 422)

    @patch("src.api.collection_entry.IGDBClient")
    def test_delete_entry_not_found(self, mock_igdb_client_class):
        """
        Should return 404 Not Found if entry doesn't exist.
        """
        mock_igdb_client = Mock()
        setup_mock_igdb_client(mock_igdb_client, MOCK_IGDB_GAME)
        mock_igdb_client_class.return_value = mock_igdb_client

        # Try to delete nonexistent entry
        response = self.client.delete(
            f"/collections/{self.test_collection.id}/entries/9999",  # Nonexistent ID
            headers=self.headers,
        )
        self.assertEqual(response.status_code, 404)
        self.assertIn("not found", response.json()["detail"].lower())

    @patch("src.api.collection_entry.IGDBClient")
    def test_delete_entry_permission_denied(self, mock_igdb_client_class):
        """
        Should return 403 Forbidden if user doesn't own the collection.
        """
        mock_igdb_client = Mock()
        setup_mock_igdb_client(mock_igdb_client, MOCK_IGDB_GAME)
        mock_igdb_client_class.return_value = mock_igdb_client

        # First create an entry
        data = {"game_id": 1, "notes": "To delete"}
        create_response = self.client.post(
            f"/collections/{self.test_collection.id}/entries/",
            json=data,
            headers=self.headers,
        )
        self.assertEqual(create_response.status_code, 201)
        entry_id = create_response.json()["id"]

        # Create another user and try to delete with their token
        other_user = self.add_user(
            username="other",
            email="other@example.com",
            password="$2b$12$KIXQJQbQhQJQbQhQJQbQhOQJQbQhQJQbQhQJQbQhQJQbQhQJQbQhO",
        )
        other_headers = {"Authorization": generate_mock_jwt(other_user.username)}

        # Try to delete
        delete_response = self.client.delete(
            f"/collections/{self.test_collection.id}/entries/{entry_id}",
            headers=other_headers,
        )
        self.assertEqual(delete_response.status_code, 403)
        self.assertIn("permission denied", delete_response.json()["detail"].lower())

    @patch("src.api.collection_entry.IGDBClient")
    def test_delete_entry_wrong_collection(self, mock_igdb_client_class):
        """
        Should return 404 Not Found if entry is in a different collection.
        """
        mock_igdb_client = Mock()
        setup_mock_igdb_client(mock_igdb_client, MOCK_IGDB_GAME)
        mock_igdb_client_class.return_value = mock_igdb_client

        # Create another collection for the same user
        other_collection = self.add_collection(user_id=1, name="Other Collection")

        # Create an entry in the first collection
        data = {"game_id": 1, "notes": "To delete"}
        create_response = self.client.post(
            f"/collections/{self.test_collection.id}/entries/",
            json=data,
            headers=self.headers,
        )
        self.assertEqual(create_response.status_code, 201)
        entry_id = create_response.json()["id"]

        # Try to delete from the other collection
        delete_response = self.client.delete(
            f"/collections/{other_collection.id}/entries/{entry_id}",
            headers=self.headers,
        )
        self.assertEqual(delete_response.status_code, 404)
        self.assertIn("not found", delete_response.json()["detail"].lower())

    @patch("src.api.collection_entry.IGDBClient")
    def test_delete_entry_after_delete(self, mock_igdb_client_class):
        """
        Should return 404 Not Found if entry is already deleted.
        """
        mock_igdb_client = Mock()
        setup_mock_igdb_client(mock_igdb_client, MOCK_IGDB_GAME)
        mock_igdb_client_class.return_value = mock_igdb_client

        # First create an entry
        data = {"game_id": 1, "notes": "To delete"}
        create_response = self.client.post(
            f"/collections/{self.test_collection.id}/entries/",
            json=data,
            headers=self.headers,
        )
        self.assertEqual(create_response.status_code, 201)
        entry_id = create_response.json()["id"]

        # Delete the entry
        first_delete = self.client.delete(
            f"/collections/{self.test_collection.id}/entries/{entry_id}",
            headers=self.headers,
        )
        self.assertEqual(first_delete.status_code, 204)

        # Try to delete again
        second_delete = self.client.delete(
            f"/collections/{self.test_collection.id}/entries/{entry_id}",
            headers=self.headers,
        )
        self.assertEqual(second_delete.status_code, 404)
        self.assertIn("not found", second_delete.json()["detail"].lower())

    @patch("src.api.collection_entry.IGDBClient")
    def test_delete_entry_after_collection_delete(self, mock_igdb_client_class):
        """
        Should return 404 Not Found if collection is deleted then entry is deleted.
        """
        mock_igdb_client = Mock()
        setup_mock_igdb_client(mock_igdb_client, MOCK_IGDB_GAME)
        mock_igdb_client_class.return_value = mock_igdb_client

        # First create an entry
        data = {"game_id": 1, "notes": "To delete"}
        create_response = self.client.post(
            f"/collections/{self.test_collection.id}/entries/",
            json=data,
            headers=self.headers,
        )
        self.assertEqual(create_response.status_code, 201)
        entry_id = create_response.json()["id"]

        # Delete the collection directly in the database
        db = TestingSessionLocal()
        db.delete(db.get(Collection, self.test_collection.id))
        db.commit()

        # Try to delete the entry
        delete_response = self.client.delete(
            f"/collections/{self.test_collection.id}/entries/{entry_id}",
            headers=self.headers,
        )
        self.assertEqual(delete_response.status_code, 404)
        self.assertIn("not found", delete_response.json()["detail"].lower())
        self.assertIn("not found", delete_response.json()["detail"].lower())
