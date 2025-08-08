"""
Service layer for CollectionEntry CRUD operations.
Implements business logic for creating, reading, updating, and deleting collection entries.
Follows TDD and checklist-driven workflow.
"""

import logging
from datetime import datetime
from typing import Optional

from sqlalchemy.orm import Session, joinedload

from apps.game_service.src.igdb.client import IGDBClient
from apps.game_service.src.schemas.collection_entry import (
    CollectionEntryCreate,
    CollectionEntryOut,
)
from db.models.collection import Collection, CollectionEntry
from db.models.game import Game

logger = logging.getLogger("collection_entry_service")


class CollectionEntryNotFoundError(Exception):
    """Raised when a collection entry is not found."""


class GameNotFoundError(Exception):
    """Raised when a game is not found."""


class DuplicateEntryError(Exception):
    """Raised when a game is already in the collection."""


class CollectionEntryPermissionError(Exception):
    """Raised when a user does not own the collection (custom, not built-in)."""


class CollectionEntryService:  # pylint: disable=too-few-public-methods
    """
    Service class for managing collection entries (adding games to collections).

    This service follows the single responsibility principle and currently
    only handles creating collection entries. Additional methods may be added
    in the future as the feature set expands.
    """

    def __init__(self, igdb_client: Optional[IGDBClient] = None):
        """
        Initialize the service with an optional IGDB client.

        Args:
            igdb_client (IGDBClient, optional): Client for validating games in IGDB.
        """
        self.igdb_client = igdb_client

    def _extract_platform_from_igdb_data(self, igdb_game_data: dict) -> str:
        """Extract platform from IGDB game data, handling different formats."""
        platforms = igdb_game_data.get("platforms", [])
        if platforms:
            # Handle both raw IGDB format (dicts) and processed format (strings)
            if isinstance(platforms[0], dict):
                return platforms[0].get("name", "Unknown")
            return platforms[0]  # Already a string
        return "Unknown"

    def _extract_genre_from_igdb_data(self, igdb_game_data: dict) -> str:
        """Extract genres from IGDB game data, handling different formats."""
        genres = igdb_game_data.get("genres", [])
        if genres:
            # Handle both raw IGDB format (dicts) and processed format (strings)
            if isinstance(genres[0], dict):
                genre_names = [g.get("name", "") for g in genres if isinstance(g, dict)]
            else:
                genre_names = [g for g in genres if isinstance(g, str)]
            return ", ".join(genre_names) if genre_names else None
        return None

    def _extract_cover_url_from_igdb_data(self, igdb_game_data: dict) -> str:
        """Extract cover URL from IGDB game data, handling different formats."""
        cover_url = igdb_game_data.get("cover_url")
        if not cover_url:
            # Handle raw IGDB format where cover is nested
            cover_data = igdb_game_data.get("cover", {})
            if cover_data:
                cover_url = cover_data.get("url")
        return cover_url

    def _extract_release_date_from_igdb_data(self, igdb_game_data: dict):
        """Extract release date from IGDB game data, handling different formats."""
        release_timestamp = igdb_game_data.get("release_date") or igdb_game_data.get(
            "first_release_date"
        )
        if release_timestamp:
            try:
                return datetime.fromtimestamp(release_timestamp).date()
            except (ValueError, TypeError, OSError):
                pass  # Keep as None if invalid
        return None

    def _get_or_create_game(self, igdb_game_id: int, db: Session) -> Game:
        """
        Get an existing game from the local database or create a new one from IGDB data.

        Args:
            igdb_game_id: The IGDB ID of the game
            db: Database session

        Returns:
            Game: The local game record

        Raises:
            GameNotFoundError: If the game is not found in IGDB
        """
        # Check if game already exists locally (by IGDB ID first, then by name/platform)
        existing_game = db.query(Game).filter(Game.igdb_id == igdb_game_id).first()
        if existing_game:
            logger.info("Game already exists locally: %s", existing_game.name)
            return existing_game

        # Fetch game data from IGDB
        if not self.igdb_client:
            raise GameNotFoundError("No IGDB client available to fetch game data")

        try:
            igdb_game_data = self.igdb_client.get_game_by_id(igdb_game_id)
            logger.info("Game found in IGDB: %s", igdb_game_data.get("name", "Unknown"))
        except (ValueError, GameNotFoundError, Exception) as e:
            logger.error("Game not found in IGDB with id=%s: %s", igdb_game_id, e)
            raise GameNotFoundError("Game not found in IGDB.") from e

        # Create new game record with IGDB data
        platform = self._extract_platform_from_igdb_data(igdb_game_data)
        genre_str = self._extract_genre_from_igdb_data(igdb_game_data)
        cover_url = self._extract_cover_url_from_igdb_data(igdb_game_data)
        release_date = self._extract_release_date_from_igdb_data(igdb_game_data)

        new_game = Game(
            igdb_id=igdb_game_id,
            name=igdb_game_data.get("name", "Unknown Game"),
            platform=platform,
            release_date=release_date,
            cover_url=cover_url,
            genre=genre_str,
        )

        # Check if a game with the same name/platform already exists
        # This handles cases where different IGDB IDs might map to the same game
        existing_by_name_platform = (
            db.query(Game)
            .filter(Game.name == new_game.name, Game.platform == new_game.platform)
            .first()
        )
        if existing_by_name_platform:
            logger.info(
                "Game with same name/platform already exists: %s (local_id=%s)",
                existing_by_name_platform.name,
                existing_by_name_platform.id,
            )
            return existing_by_name_platform

        db.add(new_game)
        db.flush()  # Get the ID without committing
        logger.info(
            "Created new game record: %s (local_id=%s)", new_game.name, new_game.id
        )
        return new_game

    def create_entry(
        self,
        collection_id: int,
        user_id: int,
        entry_data: CollectionEntryCreate,
        db: Session,
    ) -> CollectionEntryOut:
        """
        Add a game to a user's collection.
        Raises custom exceptions for error cases.
        """
        logger.info(
            "Creating collection entry: collection_id=%s, user_id=%s, entry_data=%s",
            collection_id,
            user_id,
            entry_data,
        )
        # Check if the collection exists
        collection = (
            db.query(Collection)
            .filter(
                Collection.id == collection_id,
            )
            .first()
        )
        if not collection:
            logger.error(
                "Collection not found for user_id=%s, collection_id=%s",
                user_id,
                collection_id,
            )
            raise CollectionEntryNotFoundError("Collection not found for this user.")

        # Check collection ownership
        if collection.user_id != user_id:
            logger.error("User %s does not own collection %s", user_id, collection_id)
            raise CollectionEntryPermissionError("You do not own this collection.")

        # Convert dict to Pydantic model if needed
        if isinstance(entry_data, dict):
            # Use the imported CollectionEntryCreate class
            entry_data = CollectionEntryCreate(**entry_data)

        # Get or create the game in our local database
        # This validates the game exists in IGDB and creates/retrieves the local record
        local_game = self._get_or_create_game(entry_data.game_id, db)

        # Check for duplicate entry using local game ID
        existing_entry = (
            db.query(CollectionEntry)
            .filter(
                CollectionEntry.collection_id == collection_id,
                CollectionEntry.game_id == local_game.id,  # Use local game ID
            )
            .first()
        )
        if existing_entry:
            logger.error(
                "Duplicate entry found for collection_id=%s, game_id=%s (local_id=%s)",
                collection_id,
                entry_data.game_id,
                local_game.id,
            )
            raise DuplicateEntryError("This game is already in the collection.")

        # Create the new entry using local game ID
        new_entry = CollectionEntry(
            collection_id=collection_id,
            game_id=local_game.id,  # Use local game ID, not IGDB ID
            notes=entry_data.notes,
            status=entry_data.status,
            rating=entry_data.rating,
            custom_tags=entry_data.custom_tags,
        )
        db.add(new_entry)
        try:
            db.commit()
            db.refresh(new_entry)
            logger.info("Collection entry created: %s", new_entry)
            return CollectionEntryOut.model_validate(new_entry, from_attributes=True)
        except Exception as e:
            logger.error("Error creating collection entry: %s", e)
            db.rollback()
            raise e

    def list_entries(
        self,
        collection_id: int,
        user_id: int,
        db: Session,
    ) -> list[CollectionEntryOut]:
        """
        List all entries for a collection, ordered by added_at descending.
        Raises CollectionEntryNotFoundError if collection does not exist.
        Raises CollectionEntryPermissionError if user does not own the collection.
        """
        # Check if the collection exists
        collection = db.query(Collection).filter(Collection.id == collection_id).first()
        if not collection:
            raise CollectionEntryNotFoundError("Collection not found for this user.")
        # Check collection ownership
        if collection.user_id != user_id:
            raise CollectionEntryPermissionError("You do not own this collection.")
        # Query entries, order by added_at descending
        entries = (
            db.query(CollectionEntry)
            .filter(CollectionEntry.collection_id == collection_id)
            .options(joinedload(CollectionEntry.game))  # Eager load game details
            .order_by(CollectionEntry.added_at.desc(), CollectionEntry.id.desc())
            .all()
        )
        return [
            CollectionEntryOut.model_validate(e, from_attributes=True) for e in entries
        ]

    def get_entry(
        self,
        collection_id: int,
        entry_id: int,
        user_id: int,
        db: Session,
    ) -> CollectionEntryOut:
        """
        Get details for a single collection entry by collection_id and entry_id.
        Raises CollectionEntryNotFoundError if entry does not exist.
        Raises CollectionEntryPermissionError if user does not own the collection.
        """
        # Check if the collection exists
        collection = db.query(Collection).filter(Collection.id == collection_id).first()
        if not collection:
            raise CollectionEntryNotFoundError("Collection not found for this user.")
        # Check collection ownership
        if collection.user_id != user_id:
            raise CollectionEntryPermissionError("You do not own this collection.")
        # Query the entry
        entry = (
            db.query(CollectionEntry)
            .filter(
                CollectionEntry.collection_id == collection_id,
                CollectionEntry.id == entry_id,
            )
            .options(joinedload(CollectionEntry.game))  # Eager load game details
            .first()
        )
        if not entry:
            raise CollectionEntryNotFoundError("Collection entry not found.")
        return CollectionEntryOut.model_validate(entry, from_attributes=True)

    # pylint: disable=too-many-arguments, too-many-positional-arguments
    # API/service layer often needs multiple args for context (user, collection, entry, etc.)
    def update_entry(
        self,
        collection_id: int,
        entry_id: int,
        user_id: int,
        update_data: dict,
        db: Session,
    ) -> CollectionEntryOut:
        """
        Update fields of a collection entry. Only the collection owner can update.
        Raises CollectionEntryNotFoundError or CollectionEntryPermissionError as appropriate.
        """
        # Fetch the collection and check ownership
        collection = db.query(Collection).filter(Collection.id == collection_id).first()
        if not collection:
            raise CollectionEntryNotFoundError("Collection not found.")
        if collection.user_id != user_id:
            raise CollectionEntryPermissionError("User does not own the collection.")

        # Fetch the entry
        entry = (
            db.query(CollectionEntry)
            .filter(
                CollectionEntry.id == entry_id,
                CollectionEntry.collection_id == collection_id,
            )
            .options(joinedload(CollectionEntry.game))  # Eager load game details
            .first()
        )
        if not entry:
            raise CollectionEntryNotFoundError("Collection entry not found.")

        # Update fields if provided
        updated = False
        for field in ["notes", "status", "rating", "custom_tags"]:
            if field in update_data:
                setattr(entry, field, update_data[field])
                updated = True

        if updated:
            db.commit()
            db.refresh(entry)

        return CollectionEntryOut.model_validate(entry, from_attributes=True)

    def delete_entry(
        self,
        collection_id: int,
        entry_id: int,
        user_id: int,
        db: Session,
    ) -> None:
        """
        Delete a collection entry if the user owns the collection.
        Raises CollectionEntryNotFoundError or CollectionEntryPermissionError as appropriate.
        """
        # Type checks
        if not isinstance(collection_id, int):
            raise TypeError("collection_id must be an int")
        if not isinstance(entry_id, int):
            raise TypeError("entry_id must be an int")
        if not isinstance(user_id, int):
            raise TypeError("user_id must be an int")

        # Find the entry first
        entry = (
            db.query(CollectionEntry)
            .filter_by(id=entry_id, collection_id=collection_id)
            .first()
        )  # pylint: disable=line-too-long
        if entry is None:
            raise CollectionEntryNotFoundError("Collection entry not found.")

        # Find the collection and check ownership
        collection = db.query(Collection).filter_by(id=collection_id).first()
        if collection is None:
            raise CollectionEntryNotFoundError("Collection not found for entry.")
        if collection.user_id != user_id:
            raise CollectionEntryPermissionError("You do not own this collection.")

        try:
            db.delete(entry)
            db.commit()
        except Exception as exc:
            db.rollback()
            raise exc
