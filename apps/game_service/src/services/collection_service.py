"""
Service layer for Collection CRUD operations.
Implements business logic for creating, reading, updating, and deleting collections.
Follows TDD and checklist-driven workflow.
"""

import logging
from typing import List

from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from sqlalchemy.orm import Session
from src.schemas.collection import CollectionCreate, CollectionOut, CollectionUpdate

from db.models.collection import Collection  # pylint: disable=wrong-import-order

logger = logging.getLogger("collection_service")


class CollectionNotFoundError(Exception):
    """Raised when a collection is not found for the given user."""


class CollectionService:
    """
    Service class for managing user game collections.
    """

    def create_collection(
        self, user_id: int, data: CollectionCreate, db: Session
    ) -> CollectionOut:
        """Create a new collection for the user."""
        # Convert dict to Pydantic model if needed
        if isinstance(data, dict):
            data = CollectionCreate(**data)

        logger.info("Creating collection for user_id=%s with data=%s", user_id, data)
        new_collection = Collection(
            user_id=user_id,
            name=data.name,
            description=getattr(data, "description", None),  # Optional field
        )
        db.add(new_collection)
        try:
            db.commit()
            db.refresh(new_collection)
            logger.info("Collection created: %s", new_collection)
            return CollectionOut.model_validate(new_collection, from_attributes=True)
        except IntegrityError as e:
            logger.error("IntegrityError: %s", e)
            db.rollback()
            # Raise a custom error for the API to handle
            raise ValueError("Collection name already exists for this user.") from e
        except SQLAlchemyError as e:
            logger.error("SQLAlchemyError: %s", e)
            db.rollback()
            raise

    def get_collection_by_id(
        self, collection_id: int, user_id: int, db: Session
    ) -> Collection | None:
        """
        Retrieve a collection by its ID and user ID.
        Returns the Collection object if found and owned by the user, else None.
        """
        logger.debug(
            "get_collection_by_id called with collection_id=%s, user_id=%s",
            collection_id,
            user_id,
        )
        if not isinstance(collection_id, int):
            logger.error("collection_id must be int, got %s", type(collection_id))
            raise TypeError("collection_id must be an integer")
        if not isinstance(user_id, int):
            logger.error("user_id must be int, got %s", type(user_id))
            raise TypeError("user_id must be an integer")
        collection = (
            db.query(Collection).filter_by(id=collection_id, user_id=user_id).first()
        )
        if not collection:
            logger.info(
                "Collection not found or not owned by user: id=%s, user_id=%s",
                collection_id,
                user_id,
            )
            raise CollectionNotFoundError(
                f"Collection id={collection_id} not found for user id={user_id}."
            )
        logger.info("Collection found: %s", collection)
        return collection

    def list_collections(self, user_id: int, db: Session) -> List[CollectionOut]:
        """List all collections for the user."""
        logger.debug("list_collections called with user_id=%s", user_id)
        collections = db.query(Collection).filter_by(user_id=user_id).all()
        logger.debug("Found %d collections for user_id=%s", len(collections), user_id)
        return [
            CollectionOut.model_validate(c, from_attributes=True) for c in collections
        ]

    def update_collection(
        self, user_id: int, collection_id: int, data: CollectionUpdate, db: Session
    ) -> CollectionOut:
        """Update a collection owned by the user. Only non-None fields are updated."""
        # Convert dict to Pydantic model if needed
        if isinstance(data, dict):
            data = CollectionUpdate(**data)

        logger.info(
            "Updating collection: id=%s, user_id=%s, data=%s",
            collection_id,
            user_id,
            data,
        )

        # Validate types
        if not isinstance(collection_id, int):
            raise TypeError("collection_id must be an integer")
        if not isinstance(user_id, int):
            raise TypeError("user_id must be an integer")

        collection = db.query(Collection).filter_by(id=collection_id).first()
        if not collection:
            logger.info("Collection not found: id=%s", collection_id)
            raise CollectionNotFoundError("Collection not found.")
        if collection.user_id != user_id:
            logger.info("User %s does not own collection %s", user_id, collection_id)
            raise PermissionError("User does not own this collection.")

        # Only update fields that are not None AND different from current value
        fields_updated = False
        if data.name is not None and data.name != collection.name:
            # Check for duplicate name for this user (excluding current collection)
            duplicate = (
                db.query(Collection)
                .filter(
                    Collection.user_id == user_id,
                    Collection.name == data.name,
                    Collection.id != collection_id,
                )
                .first()
            )
            if duplicate:
                logger.info("Duplicate collection name for user: %s", data.name)
                raise ValueError("Collection name already exists for this user.")
            collection.name = data.name
            fields_updated = True

        if data.description is not None and data.description != collection.description:
            collection.description = data.description
            fields_updated = True

        if not fields_updated:
            logger.warning(
                "No fields provided for update on collection id=%s", collection_id
            )
            return CollectionOut.model_validate(collection, from_attributes=True)

        try:
            db.commit()
            db.refresh(collection)
            logger.info("Collection updated: %s", collection)
            return CollectionOut.model_validate(collection, from_attributes=True)
        except SQLAlchemyError as e:
            logger.error("SQLAlchemyError during update: %s", e)
            db.rollback()
            raise

    def delete_collection(self, user_id: int, collection_id: int, db: Session) -> bool:
        """
        Delete a collection owned by the user.

        Args:
            user_id (int): The ID of the user who owns the collection.
            collection_id (int): The ID of the collection to delete.
            db (Session): SQLAlchemy database session.

        Returns:
            bool: True if the collection was deleted, False otherwise.

        Raises:
            ValueError: If the collection is not found.
            PermissionError: If the user does not own the collection.
            TypeError: If collection_id or user_id are not integers.
        """
        logger.info("Deleting collection id=%s for user_id=%s", collection_id, user_id)

        # Validate types
        if not isinstance(collection_id, int):
            raise TypeError("collection_id must be an integer")
        if not isinstance(user_id, int):
            raise TypeError("user_id must be an integer")

        # Get collection to verify ownership
        collection = db.query(Collection).filter_by(id=collection_id).first()

        if not collection:
            logger.info("Collection not found: id=%s", collection_id)
            raise CollectionNotFoundError(f"Collection id={collection_id} not found.")

        if collection.user_id != user_id:
            logger.info("User %s does not own collection %s", user_id, collection_id)
            raise PermissionError("User does not own this collection.")

        try:
            # Delete collection entries first (cascading delete also works but this is explicit)
            # If collection entries are implemented, uncomment this code
            # db.query(CollectionEntry).filter_by(collection_id=collection_id).delete()

            # Delete the collection
            db.delete(collection)
            db.commit()
            logger.info("Collection deleted: id=%s", collection_id)
            return True
        except SQLAlchemyError as e:
            logger.error("Error deleting collection: %s", e)
            db.rollback()
            raise
