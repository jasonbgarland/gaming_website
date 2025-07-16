"""
Tests for the delete methods of CollectionEntryService.
"""

# pylint: disable=duplicate-code, wrong-import-order

from apps.game_service.src.services.collection_entry_service import (
    CollectionEntryNotFoundError,
    CollectionEntryPermissionError,
)

# Import removed - CollectionNotFoundError not needed
from apps.game_service.tests.services.collection_entry.test_base import (
    BaseCollectionEntryServiceTest,
)
from db.models.collection import CollectionEntry


class TestDeleteCollectionEntry(BaseCollectionEntryServiceTest):
    """Test cases for CollectionEntryService delete_entry method."""

    def test_delete_entry_success(self):
        """
        Should successfully delete an entry and return None.
        """
        # Create an entry first
        entry_data = {"game_id": 1, "notes": "To delete"}
        entry = self._create_test_entry(entry_data)
        entry_id = entry.id

        # Delete the entry
        self.service.delete_entry(
            collection_id=self.test_collection.id,
            entry_id=entry_id,
            user_id=self.user.id,
            db=self.session,
        )

        # Verify DB state - entry should be gone
        db_entry = self.session.query(CollectionEntry).get(entry_id)
        self.assertIsNone(db_entry)

    def test_delete_entry_not_found(self):
        """
        Should raise CollectionEntryNotFoundError if entry doesn't exist.
        """
        with self.assertRaises(CollectionEntryNotFoundError):
            self.service.delete_entry(
                collection_id=self.test_collection.id,
                entry_id=99999,
                user_id=self.user.id,
                db=self.session,
            )

    def test_delete_entry_permission_denied(self):
        """
        Should raise CollectionEntryPermissionError if user doesn't own the collection.
        """
        # Create an entry first
        entry_data = {"game_id": 1, "notes": "To delete"}
        entry = self._create_test_entry(entry_data)

        # Create another user and try to delete
        other_user = self.add_user(
            username="other", email="other@example.com", password="irrelevant"
        )

        with self.assertRaises(CollectionEntryPermissionError):
            self.service.delete_entry(
                collection_id=self.test_collection.id,
                entry_id=entry.id,
                user_id=other_user.id,
                db=self.session,
            )

    def test_delete_entry_wrong_collection(self):
        """
        Should raise CollectionEntryNotFoundError if entry doesn't belong to collection.
        """
        # Create an entry first
        entry_data = {"game_id": 1, "notes": "To delete"}
        entry = self._create_test_entry(entry_data)

        # Create another collection for same user
        other_collection = self.add_collection(
            user_id=self.user.id, name="Other Collection"
        )

        with self.assertRaises(CollectionEntryNotFoundError):
            self.service.delete_entry(
                collection_id=other_collection.id,
                entry_id=entry.id,
                user_id=self.user.id,
                db=self.session,
            )

    def test_delete_entry_collection_not_found(self):
        """
        Should raise CollectionEntryNotFoundError if collection doesn't exist.
        """
        # Create an entry first
        entry_data = {"game_id": 1, "notes": "To delete"}
        entry = self._create_test_entry(entry_data)

        with self.assertRaises(CollectionEntryNotFoundError):
            self.service.delete_entry(
                collection_id=99999,
                entry_id=entry.id,
                user_id=self.user.id,
                db=self.session,
            )

    def test_delete_entry_double_delete(self):
        """
        Should raise CollectionEntryNotFoundError on second delete attempt.
        """
        # Create an entry first
        entry_data = {"game_id": 1, "notes": "To delete"}
        entry = self._create_test_entry(entry_data)
        entry_id = entry.id

        # First delete should succeed
        self.service.delete_entry(
            collection_id=self.test_collection.id,
            entry_id=entry_id,
            user_id=self.user.id,
            db=self.session,
        )

        # Second delete should fail
        with self.assertRaises(CollectionEntryNotFoundError):
            self.service.delete_entry(
                collection_id=self.test_collection.id,
                entry_id=entry_id,
                user_id=self.user.id,
                db=self.session,
            )
