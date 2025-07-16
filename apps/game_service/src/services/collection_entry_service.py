"""
Service layer for CollectionEntry CRUD operations.
Implements business logic for creating, reading, updating, and deleting collection entries.
Follows TDD and checklist-driven workflow.
"""

import logging
from typing import Optional

from sqlalchemy.orm import Session

from apps.game_service.src.igdb.client import IGDBClient
from apps.game_service.src.schemas.collection_entry import (
    CollectionEntryCreate,
    CollectionEntryOut,
)
from db.models.collection import Collection, CollectionEntry

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

        # Check if the game exists in IGDB
        if self.igdb_client:
            try:
                game = self.igdb_client.get_game_by_id(entry_data.game_id)
                logger.info("Game found in IGDB: %s", game.get("name", "Unknown"))
            except (ValueError, GameNotFoundError, Exception) as e:
                logger.error(
                    "Game not found in IGDB with id=%s: %s", entry_data.game_id, e
                )
                raise GameNotFoundError("Game not found in IGDB.") from e
        else:
            logger.warning("No IGDB client provided, skipping game validation")

        # Check for duplicate entry
        existing_entry = (
            db.query(CollectionEntry)
            .filter(
                CollectionEntry.collection_id == collection_id,
                CollectionEntry.game_id == entry_data.game_id,
            )
            .first()
        )
        if existing_entry:
            logger.error(
                "Duplicate entry found for collection_id=%s, game_id=%s",
                collection_id,
                entry_data.game_id,
            )
            raise DuplicateEntryError("This game is already in the collection.")

        # Create the new entry
        new_entry = CollectionEntry(
            collection_id=collection_id,
            game_id=entry_data.game_id,
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
