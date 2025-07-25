"""
Base test class for collection service tests.
"""

import unittest

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from src.services.collection_entry_service import CollectionEntryService
from src.services.collection_service import CollectionService

from db.models import Base  # pylint: disable=wrong-import-order
from db.models.collection import Collection  # pylint: disable=wrong-import-order

# pylint: disable=too-many-instance-attributes


class BaseCollectionServiceTest(unittest.TestCase):
    """Base test class for collection service tests with common setup."""

    def setUp(self):
        """Set up a new in-memory SQLite DB and service for each test."""
        self.engine = create_engine("sqlite:///:memory:")
        Base.metadata.create_all(self.engine)
        self.session_local = sessionmaker(bind=self.engine)
        self.db = self.session_local()
        self.service = CollectionService()
        self.entry_service = CollectionEntryService()

        # Setup user IDs for tests
        self.user1_id = 1
        self.user2_id = 2

        # Create test collections
        self.collection = Collection(
            id=1,
            name="Test Collection",
            user_id=self.user1_id,
            description="A test collection",
        )
        self.collection2 = Collection(
            id=2,
            name="Test Collection 2",
            user_id=self.user2_id,
            description="Another test collection",
        )
        self.db.add(self.collection)
        self.db.add(self.collection2)
        self.db.commit()
        self.db.refresh(self.collection)
        self.db.refresh(self.collection2)

    def tearDown(self):
        """Clean up DB session and engine after each test."""
        self.db.close()
        self.engine.dispose()
