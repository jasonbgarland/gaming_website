"""
Tests for the get methods of CollectionService.
"""

# pylint: disable=duplicate-code, wrong-import-order

from src.services.collection_service import CollectionNotFoundError
from tests.services.collection.test_base import (
    BaseCollectionServiceTest,
)


class TestGetCollection(BaseCollectionServiceTest):
    """Test cases for CollectionService get_collection method."""

    def test_get_collection_success(self):
        """Should return a collection if it exists and user owns it."""
        collection = self.service.get_collection_by_id(
            collection_id=self.collection.id, user_id=self.user1_id, db=self.db
        )
        self.assertEqual(collection.id, self.collection.id)
        self.assertEqual(collection.name, self.collection.name)
        self.assertEqual(collection.description, self.collection.description)

    def test_get_collection_not_found(self):
        """Should raise CollectionNotFoundError if collection doesn't exist."""
        with self.assertRaises(CollectionNotFoundError):
            self.service.get_collection_by_id(
                collection_id=999, user_id=self.user1_id, db=self.db
            )

    def test_get_collection_permission_denied(self):
        """Should raise CollectionNotFoundError if the user does not own the collection."""
        with self.assertRaises(CollectionNotFoundError):
            # user1 trying to get user2's collection
            self.service.get_collection_by_id(
                collection_id=self.collection2.id, user_id=self.user1_id, db=self.db
            )


class TestListCollections(BaseCollectionServiceTest):
    """Test cases for CollectionService list_collections method."""

    def test_list_collections_success(self):
        """Should return all collections owned by the user."""
        # Add a second collection for user1
        self.service.create_collection(
            user_id=self.user1_id,
            db=self.db,
            data={"name": "Second Collection", "description": "Another test"},
        )

        collections = self.service.list_collections(user_id=self.user1_id, db=self.db)

        self.assertEqual(len(collections), 2)
        collection_names = [c.name for c in collections]
        self.assertIn("Test Collection", collection_names)
        self.assertIn("Second Collection", collection_names)

    def test_list_collections_empty(self):
        """Should return an empty list if user has no collections."""
        # Use a user ID that doesn't have any collections
        user_id = 999
        collections = self.service.list_collections(user_id=user_id, db=self.db)

        self.assertEqual(len(collections), 0)
        self.assertEqual(collections, [])
