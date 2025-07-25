"""
Unit tests for CollectionEntry Pydantic schemas.
Follows TDD: tests will fail until schemas are implemented.
"""

import unittest
from datetime import UTC, datetime

from pydantic import ValidationError

from src.schemas.collection_entry import (
    CollectionEntryCreate,
    CollectionEntryOut,
    CollectionEntryUpdate,
)


class TestCollectionEntrySchemas(unittest.TestCase):
    """Unit tests for CollectionEntry Pydantic schemas."""

    def test_entry_create_valid(self):
        """Test valid creation of a CollectionEntry schema with all fields."""
        obj = CollectionEntryCreate(
            game_id=42,
            notes="Great game!",
            status="completed",
            rating=9,
            custom_tags={"genre": "RPG"},
        )
        self.assertEqual(42, obj.game_id)
        self.assertEqual("Great game!", obj.notes)
        self.assertEqual("completed", obj.status)
        self.assertEqual(9, obj.rating)
        self.assertEqual({"genre": "RPG"}, obj.custom_tags)

    def test_entry_create_minimal(self):
        """Test minimal valid creation of a CollectionEntry schema."""
        obj = CollectionEntryCreate(game_id=99)
        self.assertEqual(99, obj.game_id)
        self.assertIsNone(obj.notes)
        self.assertIsNone(obj.status)
        self.assertIsNone(obj.rating)
        self.assertIsNone(obj.custom_tags)

    def test_entry_out_fields(self):
        """Test CollectionEntryOut schema fields and values."""
        now = datetime.now(UTC)
        obj = CollectionEntryOut(
            id=5,
            collection_id=1,
            game_id=2,
            added_at=now,
            notes="note",
            status="playing",
            rating=8,
            custom_tags={"platform": "PC"},
        )
        self.assertEqual(5, obj.id)
        self.assertEqual(1, obj.collection_id)
        self.assertEqual(2, obj.game_id)
        self.assertEqual(now, obj.added_at)
        self.assertEqual("note", obj.notes)
        self.assertEqual("playing", obj.status)
        self.assertEqual(8, obj.rating)
        self.assertEqual({"platform": "PC"}, obj.custom_tags)

    def test_entry_update_partial(self):
        """Test partial update of a CollectionEntry schema."""
        obj = CollectionEntryUpdate(notes="Updated note")
        self.assertEqual("Updated note", obj.notes)
        self.assertIsNone(getattr(obj, "status", None))

    def test_entry_create_missing_game_id(self):
        """Test CollectionEntryCreate raises error if game_id is missing."""
        with self.assertRaises(ValidationError):
            CollectionEntryCreate()


if __name__ == "__main__":
    unittest.main()
