"""
Tests for the POST collection entry API endpoints.
"""

# pylint: disable=duplicate-code, wrong-import-order

from unittest.mock import Mock, patch

from apps.game_service.src.services.collection_entry_service import GameNotFoundError
from apps.game_service.tests.api.collection_entry.test_base import (
    BaseCollectionEntryAPITest,
)
from apps.game_service.tests.utils import MOCK_IGDB_GAME, setup_mock_igdb_client


class TestCreateCollectionEntry(BaseCollectionEntryAPITest):
    """Test cases for POST /collections/{collection_id}/entries/ endpoint."""

    @patch("apps.game_service.src.api.collection_entry.IGDBClient")
    async def test_create_entry_success(self, mock_igdb_client_class):
        """
        Should create a collection entry successfully with all fields.
        """
        mock_igdb_client = Mock()
        setup_mock_igdb_client(mock_igdb_client, MOCK_IGDB_GAME)
        mock_igdb_client_class.return_value = mock_igdb_client

        # Create entry
        data = {
            "game_id": 1,
            "notes": "Test notes",
            "status": "playing",
            "rating": 8,
            "custom_tags": {"favorite": True},
        }
        response = await self.client.post(
            f"/collections/{self.test_collection.id}/entries/",
            json=data,
            headers=self.headers,
        )

        # Verify response
        self.assertEqual(response.status_code, 201)
        result = response.json()
        self.assertEqual(result["game_id"], 1)
        self.assertEqual(result["notes"], "Test notes")
        self.assertEqual(result["status"], "playing")
        self.assertEqual(result["rating"], 8)
        self.assertEqual(result["custom_tags"], {"favorite": True})
        self.assertEqual(result["collection_id"], self.test_collection.id)
        self.assertIn("id", result)
        self.assertIn("added_at", result)

        # Verify IGDB client was called
        mock_igdb_client.get_game_by_id.assert_called_once_with(1)

    @patch("apps.game_service.src.api.collection_entry.IGDBClient")
    async def test_create_entry_minimal(self, mock_igdb_client_class):
        """
        Should create a collection entry with only required fields (game_id).
        """
        mock_igdb_client = Mock()
        setup_mock_igdb_client(mock_igdb_client, MOCK_IGDB_GAME)
        mock_igdb_client_class.return_value = mock_igdb_client

        # Create entry with just game_id
        data = {"game_id": 1}
        response = await self.client.post(
            f"/collections/{self.test_collection.id}/entries/",
            json=data,
            headers=self.headers,
        )

        # Verify response
        self.assertEqual(response.status_code, 201)
        result = response.json()
        self.assertEqual(result["game_id"], 1)
        self.assertIsNone(result["notes"])
        self.assertIsNone(result["status"])
        self.assertIsNone(result["rating"])
        self.assertIsNone(result["custom_tags"])
        self.assertIn("id", result)
        self.assertIn("added_at", result)

        # Verify IGDB client was called
        mock_igdb_client.get_game_by_id.assert_called_once_with(1)

    async def test_create_entry_unauthorized(self):
        """
        Should return 401 Unauthorized if no JWT is provided.
        """
        data = {"game_id": 1}
        response = await self.client.post(
            f"/collections/{self.test_collection.id}/entries/",
            json=data,
            # No headers
        )
        self.assertEqual(response.status_code, 401)

    async def test_create_entry_invalid_collection_id(self):
        """
        Should return 422 Unprocessable Entity for invalid collection_id.
        """
        data = {"game_id": 1}
        response = await self.client.post(
            "/collections/abc/entries/",  # Invalid ID (not an integer)
            json=data,
            headers=self.headers,
        )
        self.assertEqual(response.status_code, 422)

    @patch("apps.game_service.src.api.collection_entry.IGDBClient")
    async def test_create_entry_nonexistent_collection(self, mock_igdb_client_class):
        """
        Should return 404 Not Found if collection doesn't exist.
        """
        mock_igdb_client = Mock()
        setup_mock_igdb_client(mock_igdb_client, MOCK_IGDB_GAME)
        mock_igdb_client_class.return_value = mock_igdb_client

        data = {"game_id": 1}
        response = await self.client.post(
            "/collections/999/entries/",  # Nonexistent collection ID
            json=data,
            headers=self.headers,
        )
        self.assertEqual(response.status_code, 404)
        self.assertIn("Collection not found", response.json()["detail"])

    @patch("apps.game_service.src.api.collection_entry.IGDBClient")
    async def test_create_entry_permission_denied(self, mock_igdb_client_class):
        """
        Should return 403 Forbidden if user doesn't own the collection.
        """
        mock_igdb_client = Mock()
        setup_mock_igdb_client(mock_igdb_client, MOCK_IGDB_GAME)
        mock_igdb_client_class.return_value = mock_igdb_client

        # Create another user
        other_user = self.add_user(
            username="other",
            email="other@example.com",
            password="$2b$12$KIXQJQbQhQJQbQhQJQbQhOQJQbQhQJQbQhQJQbQhQJQbQhQJQbQhO",
        )

        # Create collection for the other user
        other_collection = self.add_collection(
            user_id=other_user.id, name="Other Collection"
        )

        # Try to add entry to other user's collection
        data = {"game_id": 1}
        response = await self.client.post(
            f"/collections/{other_collection.id}/entries/",
            json=data,
            headers=self.headers,  # Using user 1's token
        )
        self.assertEqual(response.status_code, 403)
        self.assertIn("Permission denied", response.json()["detail"])

    async def test_create_entry_missing_game_id(self):
        """
        Should return 422 Unprocessable Entity if game_id is missing.
        """
        data = {"notes": "Missing game_id"}  # No game_id
        response = await self.client.post(
            f"/collections/{self.test_collection.id}/entries/",
            json=data,
            headers=self.headers,
        )
        self.assertEqual(response.status_code, 422)

    @patch("apps.game_service.src.api.collection_entry.IGDBClient")
    async def test_create_entry_invalid_data(self, mock_igdb_client_class):
        """
        Should return 422 Unprocessable Entity for invalid data.
        """
        mock_igdb_client = Mock()
        setup_mock_igdb_client(mock_igdb_client, MOCK_IGDB_GAME)
        mock_igdb_client_class.return_value = mock_igdb_client

        # Invalid rating
        data = {"game_id": 1, "rating": 15}  # Valid range is 0-10
        response = await self.client.post(
            f"/collections/{self.test_collection.id}/entries/",
            json=data,
            headers=self.headers,
        )
        self.assertEqual(response.status_code, 422)

    @patch("apps.game_service.src.api.collection_entry.IGDBClient")
    async def test_create_entry_game_not_found(self, mock_igdb_client_class):
        """
        Should return 404 Not Found if game doesn't exist in IGDB.
        """
        mock_igdb_client = Mock()
        mock_igdb_client.get_game_by_id.side_effect = GameNotFoundError(
            "Game not found"
        )
        mock_igdb_client_class.return_value = mock_igdb_client

        data = {"game_id": 99999}  # Nonexistent game ID
        response = await self.client.post(
            f"/collections/{self.test_collection.id}/entries/",
            json=data,
            headers=self.headers,
        )
        self.assertEqual(response.status_code, 404)
        self.assertIn("Game not found", response.json()["detail"])
