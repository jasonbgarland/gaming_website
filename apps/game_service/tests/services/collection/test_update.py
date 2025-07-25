"""
Tests for the update methods of CollectionService.
"""

# pylint: disable=duplicate-code, wrong-import-order

from src.schemas.collection import CollectionUpdate
from src.services.collection_service import CollectionNotFoundError
from tests.services.collection.test_base import (
    BaseCollectionServiceTest,
)


class TestUpdateCollection(BaseCollectionServiceTest):
    """Test cases for CollectionService update_collection method."""

    def test_update_collection_success(self):
        """Should update collection name and description."""
        data = CollectionUpdate(
            name="Updated Collection", description="Updated description"
        )
        updated = self.service.update_collection(
            collection_id=self.collection.id,
            user_id=self.user1_id,
            db=self.db,
            data=data,
        )

        self.assertEqual(updated.name, "Updated Collection")
        self.assertEqual(updated.description, "Updated description")

        # Verify DB state
        refreshed = self.service.get_collection_by_id(
            collection_id=self.collection.id, user_id=self.user1_id, db=self.db
        )
        self.assertEqual(refreshed.name, "Updated Collection")
        self.assertEqual(refreshed.description, "Updated description")

    def test_update_collection_name_only(self):
        """Should update just the name if that's all that's provided."""
        data = CollectionUpdate(name="New Name Only")
        updated = self.service.update_collection(
            collection_id=self.collection.id,
            user_id=self.user1_id,
            db=self.db,
            data=data,
        )

        self.assertEqual(updated.name, "New Name Only")
        self.assertEqual(updated.description, self.collection.description)  # Unchanged

    def test_update_collection_description_only(self):
        """Should update just the description if that's all that's provided."""
        data = CollectionUpdate(description="New description only")
        updated = self.service.update_collection(
            collection_id=self.collection.id,
            user_id=self.user1_id,
            db=self.db,
            data=data,
        )

        self.assertEqual(updated.name, self.collection.name)  # Unchanged
        self.assertEqual(updated.description, "New description only")

    def test_update_collection_not_found(self):
        """Should raise CollectionNotFoundError if collection doesn't exist."""
        data = CollectionUpdate(name="Won't Work")
        with self.assertRaises(CollectionNotFoundError):
            self.service.update_collection(
                collection_id=999, user_id=self.user1_id, db=self.db, data=data
            )

    def test_update_collection_permission_denied(self):
        """Should raise PermissionError if user doesn't own the collection."""
        data = CollectionUpdate(name="Won't Work")
        with self.assertRaises(PermissionError):
            # user1 trying to update user2's collection
            self.service.update_collection(
                collection_id=self.collection2.id,
                user_id=self.user1_id,
                db=self.db,
                data=data,
            )
