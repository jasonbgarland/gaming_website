"""
Unit tests for Collection and CollectionEntry Pydantic schemas.
Follows TDD: tests will fail until schemas are implemented.
"""

import unittest
from datetime import UTC, datetime

from pydantic import ValidationError

# Import schemas
from apps.game_service.src.schemas.collection import (
    CollectionCreate,
    CollectionOut,
    CollectionUpdate,
)


class TestCollectionSchemas(unittest.TestCase):
    """Unit tests for Collection Pydantic schemas."""

    def test_collection_create_valid(self):
        """Test valid creation of a Collection schema."""
        obj = CollectionCreate(name="Backlog", description="Games to play")
        self.assertEqual("Backlog", obj.name)
        self.assertEqual("Games to play", obj.description)

    def test_collection_create_missing_name(self):
        """Test CollectionCreate raises error if name is missing."""
        with self.assertRaises(ValidationError):
            CollectionCreate()

    def test_collection_out_fields(self):
        """Test CollectionOut schema fields and values."""
        now = datetime.now(UTC)
        obj = CollectionOut(
            id=1,
            user_id=2,
            name="Library",
            description=None,
            created_at=now,
            updated_at=now,
        )
        self.assertEqual(1, obj.id)
        self.assertEqual(2, obj.user_id)
        self.assertEqual("Library", obj.name)
        self.assertIsNone(obj.description)
        self.assertEqual(now, obj.created_at)
        self.assertEqual(now, obj.updated_at)

    def test_collection_update_partial(self):
        """Test partial update of a Collection schema."""
        obj = CollectionUpdate(description="Updated desc")
        self.assertEqual("Updated desc", obj.description)
        self.assertIsNone(getattr(obj, "name", None))


if __name__ == "__main__":
    unittest.main()
