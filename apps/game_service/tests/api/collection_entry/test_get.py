"""
Tests for the GET collection entry API endpoints.
"""

# pylint: disable=duplicate-code, wrong-import-order

from unittest.mock import Mock, patch

from tests.api.collection_entry.test_base import (
    BaseCollectionEntryAPITest,
    generate_mock_jwt,
)
from tests.utils import MOCK_IGDB_GAME, setup_mock_igdb_client


class TestListCollectionEntries(BaseCollectionEntryAPITest):
    """Test cases for GET /collections/{collection_id}/entries/ endpoint."""

    @patch("apps.game_service.src.api.collection_entry.IGDBClient")
    async def test_list_entries_success(self, mock_igdb_client_class):
        """
        Should list all entries in a collection successfully.
        """
        mock_igdb_client = Mock()
        setup_mock_igdb_client(mock_igdb_client, MOCK_IGDB_GAME)
        mock_igdb_client_class.return_value = mock_igdb_client

        # Create multiple entries
        entries = [
            {"game_id": 1, "notes": "First entry"},
            {"game_id": 2, "notes": "Second entry"},
            {"game_id": 3, "notes": "Third entry"},
        ]

        for entry in entries:
            response = await self.client.post(
                f"/collections/{self.test_collection.id}/entries/",
                json=entry,
                headers=self.headers,
            )
            self.assertEqual(response.status_code, 201)

        # List the entries
        response = await self.client.get(
            f"/collections/{self.test_collection.id}/entries/", headers=self.headers
        )

        # Verify response
        self.assertEqual(response.status_code, 200)
        results = response.json()
        self.assertEqual(len(results), len(entries))

        # Verify game IDs
        game_ids = [entry["game_id"] for entry in results]
        self.assertIn(1, game_ids)
        self.assertIn(2, game_ids)
        self.assertIn(3, game_ids)

        # Verify notes
        notes = [entry["notes"] for entry in results]
        self.assertIn("First entry", notes)
        self.assertIn("Second entry", notes)
        self.assertIn("Third entry", notes)

    async def test_list_entries_empty(self):
        """
        Should return an empty list for a collection with no entries.
        """
        response = await self.client.get(
            f"/collections/{self.test_collection.id}/entries/", headers=self.headers
        )
        self.assertEqual(response.status_code, 200)
        results = response.json()
        self.assertEqual(len(results), 0)
        self.assertEqual(results, [])

    async def test_list_entries_unauthorized(self):
        """
        Should return 401 Unauthorized if no JWT is provided.
        """
        response = await self.client.get(
            f"/collections/{self.test_collection.id}/entries/",
            # No headers
        )
        self.assertEqual(response.status_code, 401)

    async def test_list_entries_invalid_collection_id(self):
        """
        Should return 422 Unprocessable Entity for invalid collection_id.
        """
        response = await self.client.get(
            "/collections/abc/entries/",  # Invalid ID (not an integer)
            headers=self.headers,
        )
        self.assertEqual(response.status_code, 422)

    @patch("apps.game_service.src.api.collection_entry.IGDBClient")
    async def test_list_entries_nonexistent_collection(self, mock_igdb_client_class):
        """
        Should return 404 Not Found if collection doesn't exist.
        """
        mock_igdb_client = Mock()
        setup_mock_igdb_client(mock_igdb_client, MOCK_IGDB_GAME)
        mock_igdb_client_class.return_value = mock_igdb_client

        response = await self.client.get(
            "/collections/999/entries/",  # Nonexistent collection ID
            headers=self.headers,
        )
        self.assertEqual(response.status_code, 404)
        self.assertIn("Collection not found", response.json()["detail"])

    @patch("apps.game_service.src.api.collection_entry.IGDBClient")
    async def test_list_entries_permission_denied(self, mock_igdb_client_class):
        """
        Should return 403 Forbidden if user doesn't own the collection.
        """
        mock_igdb_client = Mock()
        setup_mock_igdb_client(mock_igdb_client, MOCK_IGDB_GAME)
        mock_igdb_client_class.return_value = mock_igdb_client

        # Create another user with their own collection
        other_user = self.add_user(
            username="other",
            email="other@example.com",
            password="$2b$12$KIXQJQbQhQJQbQhQJQbQhOQJQbQhQJQbQhQJQbQhQJQbQhQJQbQhO",
        )
        other_collection = self.add_collection(
            user_id=other_user.id, name="Other Collection"
        )

        # Try to list entries with original user's token
        response = await self.client.get(
            f"/collections/{other_collection.id}/entries/",
            headers=self.headers,  # Using user 1's token
        )
        self.assertEqual(response.status_code, 403)
        self.assertIn("Permission denied", response.json()["detail"])


class TestGetCollectionEntry(BaseCollectionEntryAPITest):
    """Test cases for GET /collections/{collection_id}/entries/{entry_id} endpoint."""

    @patch("apps.game_service.src.api.collection_entry.IGDBClient")
    async def test_get_entry_success(self, mock_igdb_client_class):
        """
        Should get a single entry by ID successfully.
        """
        mock_igdb_client = Mock()
        setup_mock_igdb_client(mock_igdb_client, MOCK_IGDB_GAME)
        mock_igdb_client_class.return_value = mock_igdb_client

        # Create an entry first
        data = {"game_id": 1, "notes": "Details test"}
        create_response = await self.client.post(
            f"/collections/{self.test_collection.id}/entries/",
            json=data,
            headers=self.headers,
        )
        self.assertEqual(create_response.status_code, 201)
        entry_id = create_response.json()["id"]

        # Get the entry by ID
        get_response = await self.client.get(
            f"/collections/{self.test_collection.id}/entries/{entry_id}",
            headers=self.headers,
        )

        # Verify response
        self.assertEqual(get_response.status_code, 200)
        result = get_response.json()
        self.assertEqual(result["id"], entry_id)
        self.assertEqual(result["game_id"], 1)
        self.assertEqual(result["notes"], "Details test")
        self.assertEqual(result["collection_id"], self.test_collection.id)
        self.assertIn("added_at", result)

    async def test_get_entry_unauthorized(self):
        """
        Should return 401 Unauthorized if no JWT is provided.
        """
        response = await self.client.get(
            f"/collections/{self.test_collection.id}/entries/1",
            # No headers
        )
        self.assertEqual(response.status_code, 401)

    async def test_get_entry_invalid_collection_id(self):
        """
        Should return 422 Unprocessable Entity for invalid collection_id.
        """
        response = await self.client.get(
            "/collections/abc/entries/1",  # Invalid ID (not an integer)
            headers=self.headers,
        )
        self.assertEqual(response.status_code, 422)

    async def test_get_entry_invalid_entry_id(self):
        """
        Should return 422 Unprocessable Entity for invalid entry_id.
        """
        response = await self.client.get(
            f"/collections/{self.test_collection.id}/entries/abc",  # Invalid ID (not an integer)
            headers=self.headers,
        )
        self.assertEqual(response.status_code, 422)

    async def test_get_entry_not_found(self):
        """
        Should return 404 Not Found if entry doesn't exist.
        """
        response = await self.client.get(
            f"/collections/{self.test_collection.id}/entries/9999",  # Nonexistent ID
            headers=self.headers,
        )
        self.assertEqual(response.status_code, 404)
        self.assertIn("Entry not found", response.json()["detail"])

    @patch("apps.game_service.src.api.collection_entry.IGDBClient")
    async def test_get_entry_permission_denied(self, mock_igdb_client_class):
        """
        Should return 403 Forbidden if user doesn't own the collection.
        """
        mock_igdb_client = Mock()
        setup_mock_igdb_client(mock_igdb_client, MOCK_IGDB_GAME)
        mock_igdb_client_class.return_value = mock_igdb_client

        # First create an entry
        data = {"game_id": 1, "notes": None}
        create_response = await self.client.post(
            f"/collections/{self.test_collection.id}/entries/",
            json=data,
            headers=self.headers,
        )
        self.assertEqual(create_response.status_code, 201)
        entry_id = create_response.json()["id"]

        # Create another user and try to get with their token
        other_user = self.add_user(
            username="other",
            email="other@example.com",
            password="$2b$12$KIXQJQbQhQJQbQhQJQbQhOQJQbQhQJQbQhQJQbQhQJQbQhQJQbQhO",
        )
        other_headers = {"Authorization": generate_mock_jwt(str(other_user.id))}

        # Try to get
        get_response = await self.client.get(
            f"/collections/{self.test_collection.id}/entries/{entry_id}",
            headers=other_headers,
        )
        self.assertEqual(get_response.status_code, 403)
        self.assertIn("Permission denied", get_response.json()["detail"])
