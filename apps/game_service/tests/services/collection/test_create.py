"""
Tests for the create methods of CollectionService.
"""

# pylint: disable=duplicate-code, wrong-import-order

from pydantic import ValidationError

from src.schemas.collection import CollectionCreate

# Import removed - CollectionService is imported from the base class
from tests.services.collection.test_base import (
    BaseCollectionServiceTest,
)
from db.models.collection import Collection


class TestCreateCollection(BaseCollectionServiceTest):
    """Test cases for CollectionService create_collection method."""

    def test_create_collection_success(self):
        """Test creating a collection successfully."""
        user_id = 1
        data = CollectionCreate(name="Library")
        collection = self.service.create_collection(
            user_id=user_id, db=self.db, data=data
        )

        self.assertIsNotNone(collection)
        self.assertEqual(collection.name, "Library")
        self.assertEqual(collection.user_id, user_id)
        self.assertIsNone(collection.description)

    def test_create_collection_with_description(self):
        """Test creating a collection with a description successfully."""
        user_id = 1
        data = CollectionCreate(name="Library", description="My games library")
        collection = self.service.create_collection(
            user_id=user_id, db=self.db, data=data
        )

        self.assertIsNotNone(collection)
        self.assertEqual(collection.name, "Library")
        self.assertEqual(collection.user_id, user_id)
        self.assertEqual(collection.description, "My games library")

    def test_create_collection_name_too_short(self):
        """Should raise ValidationError if name is too short."""
        user_id = 1
        with self.assertRaises(ValidationError):
            data = CollectionCreate(name="A")  # Too short
            self.service.create_collection(user_id=user_id, db=self.db, data=data)

    def test_create_collection_name_too_long(self):
        """Should raise ValidationError if name is too long."""
        user_id = 1
        with self.assertRaises(ValidationError):
            data = CollectionCreate(name="A" * 101)  # Too long
            self.service.create_collection(user_id=user_id, db=self.db, data=data)

    def test_create_collection_persists_to_db(self):
        """Ensure the collection is persisted to the database."""
        user_id = 1
        data = CollectionCreate(name="Persistence Test")
        collection = self.service.create_collection(
            user_id=user_id, db=self.db, data=data
        )

        # Query directly to ensure it was persisted
        db_collection = (
            self.db.query(Collection).filter(Collection.id == collection.id).first()
        )

        self.assertIsNotNone(db_collection)
        self.assertEqual(db_collection.name, "Persistence Test")
        self.assertEqual(db_collection.user_id, user_id)
