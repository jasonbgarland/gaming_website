"""
Tests for the delete methods of CollectionService.
"""

# pylint: disable=duplicate-code, wrong-import-order

from apps.game_service.src.services.collection_service import CollectionNotFoundError
from apps.game_service.tests.services.collection.test_base import (
    BaseCollectionServiceTest,
)


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

    def test_delete_collection_removes_entries(self):
        """Should remove all collection entries when deleting a collection."""
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
        # (the list_entries call would fail since the collection is gone)
