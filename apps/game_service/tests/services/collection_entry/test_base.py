"""
Base test class for collection entry service tests.
"""

from unittest.mock import Mock

from src.services.collection_entry_service import CollectionEntryService
from tests.conftest import TestingSessionLocal
from tests.test_base import TestDBBase

from db.models.collection import CollectionEntry  # pylint: disable=wrong-import-order
from db.models.game import Game  # pylint: disable=wrong-import-order


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
        Creates a Game record first, then creates the CollectionEntry.

        Args:
            entry_data (dict): The data for the entry (must include game_id).

        Returns:
            CollectionEntry: The created entry.
        """
        # Create a game record first using the game_id as the IGDB ID
        game_id = entry_data["game_id"]
        game = Game(
            igdb_id=game_id,
            name=f"Test Game {game_id}",
            platform="Test Platform",
            cover_url=f"https://example.com/cover{game_id}.jpg",
        )
        self.session.add(game)
        self.session.commit()
        self.session.refresh(game)

        # Create the collection entry using the local game ID
        entry_data_copy = entry_data.copy()
        entry_data_copy["game_id"] = game.id  # Use local game ID instead of IGDB ID

        entry = CollectionEntry(
            collection_id=self.test_collection.id, **entry_data_copy
        )
        self.session.add(entry)
        self.session.commit()
        self.session.refresh(entry)
        return entry
