"""
Tests for the create methods of CollectionEntryService.
"""

# pylint: disable=duplicate-code, wrong-import-order

from unittest.mock import Mock, patch

from src.services.collection_entry_service import GameNotFoundError
from tests.services.collection_entry.test_base import BaseCollectionEntryServiceTest
from tests.utils import MOCK_IGDB_GAME, setup_mock_igdb_client

from db.models.collection import CollectionEntry


class TestCreateCollectionEntry(BaseCollectionEntryServiceTest):
    """Test cases for CollectionEntryService create_entry method."""

    @patch("apps.game_service.src.services.collection_entry_service.IGDBClient")
    def test_create_entry_success(self, mock_igdb_client_class):
        """
        Should successfully create an entry and return it.
        """
        mock_igdb_client = Mock()
        setup_mock_igdb_client(mock_igdb_client, MOCK_IGDB_GAME)
        mock_igdb_client_class.return_value = mock_igdb_client
        self.service.igdb_client = mock_igdb_client  # Ensure service uses the mock

        # Create entry
        entry_data = {
            "game_id": 1,
            "notes": "Test notes",
            "status": "playing",
            "rating": 8,
            "custom_tags": {"favorite": True},
        }
        result = self.service.create_entry(
            collection_id=self.test_collection.id,
            user_id=self.user.id,
            db=self.session,
            entry_data=entry_data,
        )

        # Verify result
        self.assertIsNotNone(result)
        self.assertEqual(result.game_id, 1)
        self.assertEqual(result.notes, "Test notes")
        self.assertEqual(result.status, "playing")
        self.assertEqual(result.rating, 8)
        self.assertEqual(result.custom_tags, {"favorite": True})
        self.assertEqual(result.collection_id, self.test_collection.id)

        # Verify DB state
        db_entry = (
            self.session.query(CollectionEntry)
            .filter(
                CollectionEntry.collection_id == self.test_collection.id,
                CollectionEntry.game_id == 1,
            )
            .first()
        )
        self.assertIsNotNone(db_entry)
        self.assertEqual(db_entry.id, result.id)

        # Verify IGDB client was called
        mock_igdb_client.get_game_by_id.assert_called_once_with(1)

    def test_create_entry_collection_not_found(self):
        """
        Should raise CollectionNotFoundError if collection doesn't exist.
        """
        nonexistent_id = 9999
        with self.assertRaises(Exception) as context:
            self.service.create_entry(
                collection_id=nonexistent_id,
                user_id=self.user.id,
                db=self.session,
                entry_data={"game_id": 1},
            )
        self.assertIn("Collection not found", str(context.exception))

    def test_create_entry_permission_denied(self):
        """
        Should raise PermissionError if user doesn't own the collection.
        """
        # Create another user and collection
        other_user = self.add_user(
            username="other", email="other@example.com", password="irrelevant"
        )
        other_collection = self.add_collection(
            user_id=other_user.id, name="Other Collection"
        )

        with self.assertRaises(Exception) as context:
            self.service.create_entry(
                collection_id=other_collection.id,
                user_id=self.user.id,
                db=self.session,
                entry_data={"game_id": 1},
            )
        self.assertIn("You do not own this collection", str(context.exception))

    @patch("apps.game_service.src.services.collection_entry_service.IGDBClient")
    def test_create_entry_duplicate(self, mock_igdb_client_class):
        """
        Should raise CollectionEntryAlreadyExistsError if entry already exists.
        """
        mock_igdb_client = Mock()
        setup_mock_igdb_client(mock_igdb_client, MOCK_IGDB_GAME)
        mock_igdb_client_class.return_value = mock_igdb_client
        self.service.igdb_client = mock_igdb_client  # Ensure service uses the mock

        # First create should succeed
        self.service.create_entry(
            collection_id=self.test_collection.id,
            user_id=self.user.id,
            db=self.session,
            entry_data={"game_id": 1, "notes": "First"},
        )

        # Second create should fail
        with self.assertRaises(
            Exception
        ) as context:  # Using general Exception since we may not have this specific error
            self.service.create_entry(
                collection_id=self.test_collection.id,
                user_id=self.user.id,
                db=self.session,
                entry_data={"game_id": 1, "notes": "Second"},
            )
        self.assertIn(
            "this game is already in the collection", str(context.exception).lower()
        )

    @patch("apps.game_service.src.services.collection_entry_service.IGDBClient")
    def test_create_entry_game_not_found(self, mock_igdb_client_class):
        """
        Should raise GameNotFoundError if game doesn't exist in IGDB.
        """
        mock_igdb_client = Mock()
        mock_igdb_client.get_game_by_id.side_effect = ValueError()
        mock_igdb_client_class.return_value = mock_igdb_client
        self.service.igdb_client = mock_igdb_client  # Ensure service uses the mock

        with self.assertRaises(GameNotFoundError):
            self.service.create_entry(
                collection_id=self.test_collection.id,
                user_id=self.user.id,
                db=self.session,
                entry_data={"game_id": 99999, "notes": "Should fail"},
            )

        mock_igdb_client.get_game_by_id.assert_called_once_with(99999)
