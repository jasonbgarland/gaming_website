# pylint: disable=wrong-import-position

"""
Unit tests for SQLAlchemy models in the gaming library database.

Covers User, Game, Collection, and CollectionEntry models, including relationships and constraints.
"""
import unittest
from sqlalchemy import create_engine, event
from sqlalchemy.orm import sessionmaker
from db.models import Base, User, Game, Collection, CollectionEntry


class BaseModelTestCase(unittest.TestCase):
    """Base test case for setting up and tearing down the in-memory database."""

    def setUp(self):
        self.engine = create_engine("sqlite:///:memory:")

        # Enable foreign key support for SQLite
        @event.listens_for(self.engine, "connect")
        def set_sqlite_pragma(dbapi_connection, _connection_record):
            cursor = dbapi_connection.cursor()
            cursor.execute("PRAGMA foreign_keys=ON")
            cursor.close()

        Base.metadata.create_all(self.engine)
        self.session_factory = sessionmaker(bind=self.engine)
        self.session = self.session_factory()

    def tearDown(self):
        self.session.close()
        self.engine.dispose()


class TestUserModel(BaseModelTestCase):
    """
    Tests for the User model.
    """

    def test_create_user(self):
        """Test creating a user and verifying the ID is set."""
        user = User(email="user@example.com", username="user", hashed_password="pw")
        self.session.add(user)
        self.session.commit()
        self.assertIsNotNone(user.id)


class TestGameModel(BaseModelTestCase):
    """
    Tests for the Game model.
    """

    def test_create_game(self):
        """Test creating a game and verifying the ID is set."""
        game = Game(title="Halo", platform="Xbox")
        self.session.add(game)
        self.session.commit()
        self.assertIsNotNone(game.id)


class TestCollectionModel(BaseModelTestCase):
    """
    Tests for the Collection model.
    """

    def test_collection_without_user_fails(self):
        """Test that a collection without a user fails to commit."""
        collection = Collection(user_id=None, name="Orphaned")
        self.session.add(collection)
        with self.assertRaises(Exception):
            self.session.commit()

    def test_long_collection_name(self):
        """Test creating a collection with a long name."""
        user = User(email="long@b.com", username="long", hashed_password="pw")
        self.session.add(user)
        self.session.commit()
        long_name = "A" * 300  # Adjust if you set a max length
        collection = Collection(user_id=user.id, name=long_name)
        self.session.add(collection)
        self.session.commit()
        self.assertEqual(collection.name, long_name)

    def test_duplicate_igdb_id(self):
        """Test that duplicate IGDB IDs are not allowed for games."""
        game1 = Game(title="Game1", platform="PC", igdb_id=123)
        game2 = Game(title="Game2", platform="PC", igdb_id=123)
        self.session.add_all([game1, game2])
        with self.assertRaises(Exception):
            self.session.commit()

    def test_duplicate_email(self):
        """Test that duplicate emails are not allowed for users."""
        user1 = User(email="dup@b.com", username="dup1", hashed_password="pw")
        user2 = User(email="dup@b.com", username="dup2", hashed_password="pw")
        self.session.add_all([user1, user2])
        with self.assertRaises(Exception):
            self.session.commit()

    def test_duplicate_username(self):
        """Test that duplicate usernames are not allowed for users."""
        user1 = User(email="u1@b.com", username="dup", hashed_password="pw")
        user2 = User(email="u2@b.com", username="dup", hashed_password="pw")
        self.session.add_all([user1, user2])
        with self.assertRaises(Exception):
            self.session.commit()

    def test_create_collection(self):
        """Test creating a collection for a user."""
        user = User(email="test@example.com", username="testuser", hashed_password="pw")
        self.session.add(user)
        self.session.commit()
        collection = Collection(user_id=user.id, name="Favorites")
        self.session.add(collection)
        self.session.commit()
        self.assertEqual(collection.user_id, user.id)

    def test_unique_collection_name_per_user(self):
        """Test that collection names are unique per user."""
        user = User(email="a@b.com", username="a", hashed_password="pw")
        self.session.add(user)
        self.session.commit()
        c1 = Collection(user_id=user.id, name="Backlog")
        c2 = Collection(user_id=user.id, name="Backlog")
        self.session.add_all([c1, c2])
        with self.assertRaises(Exception):
            self.session.commit()

    def test_multiple_collections_per_user(self):
        """Test that a user can have multiple collections."""
        user = User(email="multi@b.com", username="multi", hashed_password="pw")
        self.session.add(user)
        self.session.commit()
        c1 = Collection(user_id=user.id, name="Backlog")
        c2 = Collection(user_id=user.id, name="Favorites")
        self.session.add_all([c1, c2])
        self.session.commit()
        self.assertEqual(
            len(self.session.query(Collection).filter_by(user_id=user.id).all()), 2
        )


class TestCollectionEntryModel(BaseModelTestCase):
    """
    Tests for the CollectionEntry model.
    """

    def test_entry_without_collection_or_game_fails(self):
        """Test that an entry without a collection or game fails to commit."""
        entry1 = CollectionEntry(collection_id=None, game_id=1)
        entry2 = CollectionEntry(collection_id=1, game_id=None)
        self.session.add_all([entry1, entry2])
        with self.assertRaises(Exception):
            self.session.commit()

    def test_update_entry_fields(self):
        """Test updating fields on a collection entry."""
        user = User(email="update@b.com", username="update", hashed_password="pw")
        game = Game(title="Update", platform="PC")
        self.session.add_all([user, game])
        self.session.commit()
        collection = Collection(user_id=user.id, name="UpdateTest")
        self.session.add(collection)
        self.session.commit()
        entry = CollectionEntry(
            collection_id=collection.id,
            game_id=game.id,
            status="playing",
            rating=5,
            notes="ok",
        )
        self.session.add(entry)
        self.session.commit()
        entry.status = "completed"
        entry.rating = 10
        entry.notes = "Excellent!"
        self.session.commit()
        fetched = self.session.get(CollectionEntry, entry.id)
        self.assertEqual(fetched.status, "completed")
        self.assertEqual(fetched.rating, 10)
        self.assertEqual(fetched.notes, "Excellent!")

    def test_add_game_to_collection(self):
        """Test adding a game to a collection."""
        user = User(email="b@b.com", username="b", hashed_password="pw")
        game = Game(title="Zelda", platform="Switch")
        self.session.add_all([user, game])
        self.session.commit()
        collection = Collection(user_id=user.id, name="Adventure")
        self.session.add(collection)
        self.session.commit()
        entry = CollectionEntry(collection_id=collection.id, game_id=game.id)
        self.session.add(entry)
        self.session.commit()
        self.assertEqual(entry.collection_id, collection.id)
        self.assertEqual(entry.game_id, game.id)

    def test_unique_game_per_collection(self):
        """Test that a game can only appear once per collection."""
        user = User(email="c@b.com", username="c", hashed_password="pw")
        game = Game(title="Mario", platform="Switch")
        self.session.add_all([user, game])
        self.session.commit()
        collection = Collection(user_id=user.id, name="Platformers")
        self.session.add(collection)
        self.session.commit()
        entry1 = CollectionEntry(collection_id=collection.id, game_id=game.id)
        entry2 = CollectionEntry(collection_id=collection.id, game_id=game.id)
        self.session.add_all([entry1, entry2])
        with self.assertRaises(Exception):
            self.session.commit()

    def test_game_in_multiple_collections(self):
        """Test that a game can be in multiple collections."""
        user = User(email="d@b.com", username="d", hashed_password="pw")
        game = Game(title="Celeste", platform="Switch")
        self.session.add_all([user, game])
        self.session.commit()
        c1 = Collection(user_id=user.id, name="Indies")
        c2 = Collection(user_id=user.id, name="Favorites")
        self.session.add_all([c1, c2])
        self.session.commit()
        entry1 = CollectionEntry(collection_id=c1.id, game_id=game.id)
        entry2 = CollectionEntry(collection_id=c2.id, game_id=game.id)
        self.session.add_all([entry1, entry2])
        self.session.commit()
        self.assertEqual(
            self.session.query(CollectionEntry).filter_by(game_id=game.id).count(), 2
        )

    def test_entry_optional_fields(self):
        """Test that optional fields on entry can be set and retrieved."""
        user = User(email="e@b.com", username="e", hashed_password="pw")
        game = Game(title="Hades", platform="PC")
        self.session.add_all([user, game])
        self.session.commit()
        collection = Collection(user_id=user.id, name="Roguelikes")
        self.session.add(collection)
        self.session.commit()
        entry = CollectionEntry(
            collection_id=collection.id,
            game_id=game.id,
            status="completed",
            rating=9,
            notes="Great game!",
        )
        self.session.add(entry)
        self.session.commit()
        fetched = self.session.get(CollectionEntry, entry.id)
        self.assertEqual(fetched.status, "completed")
        self.assertEqual(fetched.rating, 9)
        self.assertEqual(fetched.notes, "Great game!")


class TestRelationships(BaseModelTestCase):
    """
    Tests for model relationships and cascade behaviors.
    """

    def test_delete_collection_entry_only(self):
        """Test deleting a collection entry does not delete related collection or game."""
        user = User(email="delentry@b.com", username="delentry", hashed_password="pw")
        game = Game(title="DeleteEntry", platform="PC")
        self.session.add_all([user, game])
        self.session.commit()
        collection = Collection(user_id=user.id, name="DeleteEntryTest")
        self.session.add(collection)
        self.session.commit()
        entry = CollectionEntry(collection_id=collection.id, game_id=game.id)
        self.session.add(entry)
        self.session.commit()
        self.session.delete(entry)
        self.session.commit()
        self.assertEqual(self.session.query(CollectionEntry).count(), 0)
        self.assertEqual(self.session.query(Collection).count(), 1)
        self.assertEqual(self.session.query(Game).count(), 1)

    def test_relationship_navigation(self):
        """Test navigating relationships between user, collection, game, and entry."""
        user = User(email="rel@b.com", username="rel", hashed_password="pw")
        game = Game(title="RelGame", platform="PC")
        self.session.add_all([user, game])
        self.session.commit()
        collection = Collection(user_id=user.id, name="RelCol")
        self.session.add(collection)
        self.session.commit()
        entry = CollectionEntry(
            collection_id=collection.id, game_id=game.id, status="playing"
        )
        self.session.add(entry)
        self.session.commit()
        # Fetch collections for user
        user_collections = (
            self.session.query(Collection).filter_by(user_id=user.id).all()
        )
        self.assertEqual(len(user_collections), 1)
        # Fetch entries for collection
        col_entries = (
            self.session.query(CollectionEntry)
            .filter_by(collection_id=collection.id)
            .all()
        )
        self.assertEqual(len(col_entries), 1)
        # Fetch entries for game
        game_entries = (
            self.session.query(CollectionEntry).filter_by(game_id=game.id).all()
        )
        self.assertEqual(len(game_entries), 1)
        # Check entry fields
        self.assertEqual(col_entries[0].status, "playing")

    def test_cascade_delete_collection(self):
        """Test that deleting a collection cascades to its entries."""
        user = User(email="f@b.com", username="f", hashed_password="pw")
        game = Game(title="Portal", platform="PC")
        self.session.add_all([user, game])
        self.session.commit()
        collection = Collection(user_id=user.id, name="Puzzle")
        self.session.add(collection)
        self.session.commit()
        entry = CollectionEntry(collection_id=collection.id, game_id=game.id)
        self.session.add(entry)
        self.session.commit()
        self.session.delete(collection)
        self.session.commit()
        self.assertEqual(self.session.query(CollectionEntry).count(), 0)

    def test_cascade_delete_user(self):
        """Test that deleting a user cascades to their collections and entries."""
        user = User(email="g@b.com", username="g", hashed_password="pw")
        game = Game(title="Doom", platform="PC")
        self.session.add_all([user, game])
        self.session.commit()
        collection = Collection(user_id=user.id, name="Shooters")
        self.session.add(collection)
        self.session.commit()
        entry = CollectionEntry(collection_id=collection.id, game_id=game.id)
        self.session.add(entry)
        self.session.commit()
        self.session.delete(user)
        self.session.commit()
        self.assertEqual(self.session.query(Collection).count(), 0)
        self.assertEqual(self.session.query(CollectionEntry).count(), 0)

    def test_cascade_delete_game(self):
        """Test that deleting a game cascades to its collection entries."""
        user = User(email="h@b.com", username="h", hashed_password="pw")
        game = Game(title="Tetris", platform="Game Boy")
        self.session.add_all([user, game])
        self.session.commit()
        collection = Collection(user_id=user.id, name="Classics")
        self.session.add(collection)
        self.session.commit()
        entry = CollectionEntry(collection_id=collection.id, game_id=game.id)
        self.session.add(entry)
        self.session.commit()
        self.session.delete(game)
        self.session.commit()
        self.assertEqual(self.session.query(CollectionEntry).count(), 0)


if __name__ == "__main__":
    unittest.main()
