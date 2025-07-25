"""
Tests for the update methods of CollectionEntryService.
"""

# pylint: disable=duplicate-code, wrong-import-order

# Removed unused import

from src.services.collection_entry_service import (
    CollectionEntryNotFoundError,
    CollectionEntryPermissionError,
)
from tests.services.collection_entry.test_base import (
    BaseCollectionEntryServiceTest,
)
from db.models.collection import CollectionEntry


class TestUpdateCollectionEntry(BaseCollectionEntryServiceTest):
    """Test cases for CollectionEntryService update_entry method."""

    def test_update_entry_success(self):
        """
        Should successfully update an entry and return it.
        """
        # Create an entry first
        entry_data = {
            "game_id": 1,
            "notes": "Initial notes",
            "status": "playing",
            "rating": 7,
        }
        entry = self._create_test_entry(entry_data)

        # Update the entry
        update_data = {
            "notes": "Updated notes",
            "status": "completed",
            "rating": 9,
            "custom_tags": {"favorite": True},
        }
        result = self.service.update_entry(
            collection_id=self.test_collection.id,
            entry_id=entry.id,
            user_id=self.user.id,
            db=self.session,
            update_data=update_data,
        )

        # Verify result
        self.assertEqual(result.id, entry.id)
        self.assertEqual(result.notes, "Updated notes")
        self.assertEqual(result.status, "completed")
        self.assertEqual(result.rating, 9)
        self.assertEqual(result.custom_tags, {"favorite": True})

        # Verify DB state
        db_entry = self.session.query(CollectionEntry).get(entry.id)
        self.assertEqual(db_entry.notes, "Updated notes")
        self.assertEqual(db_entry.status, "completed")
        self.assertEqual(db_entry.rating, 9)
        self.assertEqual(db_entry.custom_tags, {"favorite": True})

    def test_update_entry_not_found(self):
        """
        Should raise CollectionEntryNotFoundError if entry doesn't exist.
        """
        update_data = {"notes": "Should not work"}
        with self.assertRaises(CollectionEntryNotFoundError):
            self.service.update_entry(
                collection_id=self.test_collection.id,
                entry_id=99999,
                user_id=self.user.id,
                db=self.session,
                update_data=update_data,
            )

    def test_update_entry_permission_denied(self):
        """
        Should raise CollectionEntryPermissionError if user doesn't own the collection.
        """
        # Create an entry first
        entry_data = {"game_id": 1, "notes": "Initial notes"}
        entry = self._create_test_entry(entry_data)

        # Create another user and try to update
        other_user = self.add_user(
            username="other", email="other@example.com", password="irrelevant"
        )

        update_data = {"notes": "Should not work"}
        with self.assertRaises(CollectionEntryPermissionError):
            self.service.update_entry(
                collection_id=self.test_collection.id,
                entry_id=entry.id,
                user_id=other_user.id,
                db=self.session,
                update_data=update_data,
            )

    def test_update_entry_wrong_collection(self):
        """
        Should raise CollectionEntryNotFoundError if entry doesn't belong to collection.
        """
        # Create an entry first
        entry_data = {"game_id": 1, "notes": "Initial notes"}
        entry = self._create_test_entry(entry_data)

        # Create another collection for same user
        other_collection = self.add_collection(
            user_id=self.user.id, name="Other Collection"
        )

        update_data = {"notes": "Should not work"}
        with self.assertRaises(CollectionEntryNotFoundError):
            self.service.update_entry(
                collection_id=other_collection.id,
                entry_id=entry.id,
                user_id=self.user.id,
                db=self.session,
                update_data=update_data,
            )

    def test_update_entry_partial_update(self):
        """
        Should update only the specified fields.
        """
        # Create an entry first
        entry_data = {
            "game_id": 1,
            "notes": "Initial notes",
            "status": "playing",
            "rating": 7,
        }
        entry = self._create_test_entry(entry_data)

        # Update only one field
        update_data = {"status": "completed"}
        result = self.service.update_entry(
            collection_id=self.test_collection.id,
            entry_id=entry.id,
            user_id=self.user.id,
            db=self.session,
            update_data=update_data,
        )

        # Verify only that field was updated
        self.assertEqual(result.status, "completed")
        self.assertEqual(result.notes, "Initial notes")
        self.assertEqual(result.rating, 7)
