"""
Tests for the get and list methods of CollectionEntryService.
"""

# pylint: disable=duplicate-code, wrong-import-order

from src.services.collection_entry_service import (
    CollectionEntryNotFoundError,
    CollectionEntryPermissionError,
)

# Import removed - CollectionNotFoundError not needed here
from tests.services.collection_entry.test_base import (
    BaseCollectionEntryServiceTest,
)


class TestGetCollectionEntry(BaseCollectionEntryServiceTest):
    """Test cases for CollectionEntryService get_entry method."""

    def test_get_entry_success(self):
        """
        Should successfully get an entry by ID.
        """
        # Create an entry first
        entry_data = {"game_id": 1, "notes": "Test notes"}
        entry = self._create_test_entry(entry_data)

        # Get the entry
        result = self.service.get_entry(
            collection_id=self.test_collection.id,
            entry_id=entry.id,
            user_id=self.user.id,
            db=self.session,
        )

        # Verify result
        self.assertIsNotNone(result)
        self.assertEqual(result.id, entry.id)
        self.assertEqual(result.game_id, 1)
        self.assertEqual(result.notes, "Test notes")
        self.assertEqual(result.collection_id, self.test_collection.id)

    def test_get_entry_not_found(self):
        """
        Should raise CollectionEntryNotFoundError if entry doesn't exist.
        """
        with self.assertRaises(CollectionEntryNotFoundError):
            self.service.get_entry(
                collection_id=self.test_collection.id,
                entry_id=99999,
                user_id=self.user.id,
                db=self.session,
            )

    def test_get_entry_permission_denied(self):
        """
        Should raise CollectionEntryPermissionError if user doesn't own the collection.
        """
        # Create an entry first
        entry_data = {"game_id": 1, "notes": "Test notes"}
        entry = self._create_test_entry(entry_data)

        # Create another user and try to get the entry
        other_user = self.add_user(
            username="other", email="other@example.com", password="irrelevant"
        )

        with self.assertRaises(CollectionEntryPermissionError):
            self.service.get_entry(
                collection_id=self.test_collection.id,
                entry_id=entry.id,
                user_id=other_user.id,
                db=self.session,
            )

    def test_get_entry_wrong_collection(self):
        """
        Should raise CollectionEntryNotFoundError if entry doesn't belong to collection.
        """
        # Create an entry first
        entry_data = {"game_id": 1, "notes": "Test notes"}
        entry = self._create_test_entry(entry_data)

        # Create another collection for same user
        other_collection = self.add_collection(
            user_id=self.user.id, name="Other Collection"
        )

        with self.assertRaises(CollectionEntryNotFoundError):
            self.service.get_entry(
                collection_id=other_collection.id,
                entry_id=entry.id,
                user_id=self.user.id,
                db=self.session,
            )


class TestListCollectionEntries(BaseCollectionEntryServiceTest):
    """Test cases for CollectionEntryService list_entries method."""

    def test_list_entries_success(self):
        """
        Should successfully list all entries in a collection.
        """
        # Create multiple entries
        self._create_test_entry({"game_id": 1, "notes": "First entry"})
        self._create_test_entry({"game_id": 2, "notes": "Second entry"})
        self._create_test_entry({"game_id": 3, "notes": "Third entry"})

        # List the entries
        results = self.service.list_entries(
            collection_id=self.test_collection.id, user_id=self.user.id, db=self.session
        )

        # Verify results
        self.assertEqual(len(results), 3)
        game_ids = [entry.game_id for entry in results]
        self.assertIn(1, game_ids)
        self.assertIn(2, game_ids)
        self.assertIn(3, game_ids)

    def test_list_entries_empty_collection(self):
        """
        Should return an empty list for a collection with no entries.
        """
        results = self.service.list_entries(
            collection_id=self.test_collection.id, user_id=self.user.id, db=self.session
        )
        self.assertEqual(len(results), 0)
        self.assertEqual(results, [])

    def test_list_entries_permission_denied(self):
        """
        Should raise CollectionEntryPermissionError if user doesn't own the collection.
        """
        # Create entries
        self._create_test_entry({"game_id": 1, "notes": "First entry"})
        self._create_test_entry({"game_id": 2, "notes": "Second entry"})

        # Create another user and try to list entries
        other_user = self.add_user(
            username="other", email="other@example.com", password="irrelevant"
        )

        with self.assertRaises(CollectionEntryPermissionError):
            self.service.list_entries(
                collection_id=self.test_collection.id,
                user_id=other_user.id,
                db=self.session,
            )
