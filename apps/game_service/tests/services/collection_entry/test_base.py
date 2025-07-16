"""
Base test class for collection entry service tests.
"""

from unittest.mock import Mock

from apps.game_service.src.services.collection_entry_service import (
    CollectionEntryService,
)
from apps.game_service.tests.conftest import TestingSessionLocal
from apps.game_service.tests.test_base import TestDBBase
from db.models.collection import CollectionEntry


class BaseCollectionEntryServiceTest(TestDBBase):
    """Base test class for collection entry service tests with common setup."""

    def setUp(self):
        # pylint: disable=duplicate-code
        super().setUp()
        # Create a DB session
        self.session = TestingSessionLocal()

        # Create user with id=1
        self.user = self.add_user(
            username="testuser",
            email="testuser@example.com",
            password="$2b$12$KIXQJQbQhQJQbQhQJQbQhOQJQbQhQJQbQhQJQbQhQJQbQhQJQbQhO",
        )

        # Create a test collection
        self.test_collection = self.add_collection(
            user_id=self.user.id, name="Test Collection", description="Test Description"
        )

        # Initialize service
        self.service = CollectionEntryService()

        # Mock IGDB client that can be used by test subclasses
        self.mock_igdb_client = Mock()

    def tearDown(self):
        self.session.close()
        super().tearDown()

    def _create_test_entry(self, entry_data):
        """
        Helper method to create a test collection entry.

        Args:
            entry_data (dict): The data for the entry.

        Returns:
            CollectionEntry: The created entry.
        """
        entry = CollectionEntry(collection_id=self.test_collection.id, **entry_data)
        self.session.add(entry)
        self.session.commit()
        self.session.refresh(entry)
        return entry
