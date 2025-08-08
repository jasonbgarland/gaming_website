"""
Tests for the delete methods of CollectionService.
"""

# pylint: disable=duplicate-code, wrong-import-order

from unittest.mock import Mock, patch

from src.services.collection_service import CollectionNotFoundError
from tests.services.collection.test_base import (
    BaseCollectionServiceTest,
)
from db.models.collection import Collection, CollectionEntry


class TestDeleteCollection(BaseCollectionServiceTest):
    """Test cases for CollectionService delete_collection method."""

    def test_delete_collection_success(self):
        """Should delete the collection if it exists and user owns it."""
        # Verify it exists first
        collection = self.service.get_collection_by_id(
            collection_id=self.collection.id, user_id=self.user1_id, db=self.db
        )
        self.assertIsNotNone(collection)

        # Delete it
        self.service.delete_collection(
            collection_id=self.collection.id, user_id=self.user1_id, db=self.db
        )

        # No need to check return value as it's None

        # Verify it's gone
        with self.assertRaises(CollectionNotFoundError):
            self.service.get_collection_by_id(
                collection_id=self.collection.id, user_id=self.user1_id, db=self.db
            )

    def test_delete_collection_not_found(self):
        """Should raise CollectionNotFoundError if collection doesn't exist."""
        with self.assertRaises(CollectionNotFoundError):
            self.service.delete_collection(
                collection_id=999, user_id=self.user1_id, db=self.db
            )

    def test_delete_collection_permission_denied(self):
        """Should raise PermissionError if user doesn't own the collection."""
        with self.assertRaises(PermissionError):
            # user1 trying to delete user2's collection
            self.service.delete_collection(
                collection_id=self.collection2.id, user_id=self.user1_id, db=self.db
            )

    @patch("apps.game_service.src.services.collection_entry_service.IGDBClient")
    def test_delete_collection_removes_entries(self, mock_igdb_client_class):
        """Should remove all collection entries when deleting a collection."""
        # Setup mock IGDB client with different games for different IDs
        mock_igdb_client = Mock()

        # Mock different games for different IDs to avoid duplicate entries
        def mock_get_game_by_id(game_id):
            if game_id == 1:
                return {
                    "id": 1,
                    "name": "Test Game 1",
                    "cover_url": "https://example.com/cover1.jpg",
                    "summary": "First test game",
                    "release_date": 1234567890,
                    "genres": ["Action"],
                    "platforms": ["PC"],
                }
            if game_id == 2:
                return {
                    "id": 2,
                    "name": "Test Game 2",
                    "cover_url": "https://example.com/cover2.jpg",
                    "summary": "Second test game",
                    "release_date": 1234567891,
                    "genres": ["Adventure"],
                    "platforms": ["PlayStation"],
                }
            raise ValueError(f"Game {game_id} not found")

        mock_igdb_client.get_game_by_id.side_effect = mock_get_game_by_id
        mock_igdb_client_class.return_value = mock_igdb_client
        self.entry_service.igdb_client = mock_igdb_client

        # Add entries to the collection first
        self.entry_service.create_entry(
            collection_id=self.collection.id,
            user_id=self.user1_id,
            entry_data={"game_id": 1, "notes": "Test entry"},
            db=self.db,
        )
        self.entry_service.create_entry(
            collection_id=self.collection.id,
            user_id=self.user1_id,
            entry_data={"game_id": 2, "notes": "Another test entry"},
            db=self.db,
        )

        # Verify entries exist
        entries = self.entry_service.list_entries(
            collection_id=self.collection.id, user_id=self.user1_id, db=self.db
        )
        self.assertEqual(len(entries), 2)

        # Delete collection
        self.service.delete_collection(
            collection_id=self.collection.id, user_id=self.user1_id, db=self.db
        )

        # Collection should be gone, and entries with it
        collection = self.db.query(Collection).filter_by(id=self.collection.id).first()
        self.assertIsNone(collection)
        entries = (
            self.db.query(CollectionEntry)
            .filter_by(collection_id=self.collection.id)
            .all()
        )
        self.assertEqual(len(entries), 0)
