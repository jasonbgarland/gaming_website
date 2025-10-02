"""
API routes for CollectionEntry.
"""

import logging

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from src.api.dependencies import get_current_user, get_igdb_auth
from src.core.database import get_db
from src.igdb.client import IGDBClient
from src.schemas.collection_entry import (
    CollectionEntryCreate,
    CollectionEntryOut,
    CollectionEntryUpdate,
)

from apps.game_service.src.services.collection_entry_service import (  # pylint: disable=wrong-import-order
    CollectionEntryNotFoundError,
    CollectionEntryPermissionError,
    CollectionEntryService,
    DuplicateEntryError,
    GameNotFoundError,
)
from db.models.collection import Collection  # pylint: disable=wrong-import-order

router = APIRouter(
    prefix="/collections/{collection_id}/entries", tags=["CollectionEntry"]
)

# Set up logger at module level
logger = logging.getLogger("api.collection_entry")


@router.post(
    "/", response_model=CollectionEntryOut, status_code=status.HTTP_201_CREATED
)
def create_collection_entry(
    collection_id: int,
    entry_data: CollectionEntryCreate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user),
    igdb_auth=Depends(get_igdb_auth),
):
    """
    Create a new collection entry for a given collection and user.
    Validates input, checks permissions, and delegates to service layer.
    """
    user_id = int(current_user["id"])
    logger.info(
        "User %s attempting to add game %s to collection %s",
        user_id,
        entry_data.game_id,
        collection_id,
    )

    # Create IGDB client and service
    igdb_client = IGDBClient(auth=igdb_auth)
    service = CollectionEntryService(igdb_client=igdb_client)

    try:
        result = service.create_entry(
            collection_id=collection_id,
            user_id=user_id,
            entry_data=entry_data,
            db=db,
        )
        logger.info("Collection entry created: %s", result)
        return result
    except CollectionEntryNotFoundError as exc:
        logger.warning("Collection %s not found for user %s", collection_id, user_id)
        raise HTTPException(status_code=404, detail="Collection not found") from exc
    except CollectionEntryPermissionError as exc:
        logger.warning(
            "User %s does not have permission for collection %s", user_id, collection_id
        )
        raise HTTPException(status_code=403, detail="Permission denied") from exc
    except DuplicateEntryError as exc:
        logger.warning(
            "Duplicate entry for game %s in collection %s",
            entry_data.game_id,
            collection_id,
        )
        raise HTTPException(
            status_code=409, detail="Game already exists in collection"
        ) from exc
    except GameNotFoundError as exc:
        logger.warning("Game %s not found", entry_data.game_id)
        raise HTTPException(status_code=404, detail="Game not found") from exc
    except Exception as e:
        logger.error("Unexpected error: %s", e)
        raise HTTPException(status_code=500, detail="Internal server error") from e


@router.get(
    "/",
    response_model=list[CollectionEntryOut],
    status_code=status.HTTP_200_OK,
    summary="List collection entries",
    description="List all entries in a collection for the current user",
)
def list_collection_entries(
    collection_id: int,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    """
    List all entries in a collection for the current user.
    """
    user_id = int(current_user["id"])
    service = CollectionEntryService()
    try:
        return service.list_entries(collection_id=collection_id, user_id=user_id, db=db)
    except CollectionEntryNotFoundError as exc:
        logger.warning("Collection %s not found for user %s", collection_id, user_id)
        raise HTTPException(status_code=404, detail="Collection not found") from exc
    except CollectionEntryPermissionError as exc:
        logger.warning(
            "User %s does not have permission for collection %s", user_id, collection_id
        )
        raise HTTPException(status_code=403, detail="Permission denied") from exc
    except Exception as e:
        logger.error("Unexpected error: %s", e)
        raise HTTPException(status_code=500, detail="Internal server error") from e


@router.get(
    "/{entry_id}",
    response_model=CollectionEntryOut,
    status_code=status.HTTP_200_OK,
    summary="Get collection entry details",
    description="Get details for a specific entry in a collection for the current user.",
)
def get_collection_entry_details(
    collection_id: int,
    entry_id: int,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    """
    Get details for a specific entry in a collection for the current user.
    """
    user_id = int(current_user["id"])
    service = CollectionEntryService()
    try:
        return service.get_entry(
            collection_id=collection_id,
            entry_id=entry_id,
            user_id=user_id,
            db=db,
        )
    except CollectionEntryNotFoundError as exc:
        logger.warning(
            "Entry %s not found in collection %s for user %s",
            entry_id,
            collection_id,
            user_id,
        )
        raise HTTPException(status_code=404, detail="Entry not found") from exc
    except CollectionEntryPermissionError as exc:
        logger.warning(
            "User %s does not have permission for collection %s", user_id, collection_id
        )
        raise HTTPException(status_code=403, detail="Permission denied") from exc
    except Exception as e:
        logger.error("Unexpected error: %s", e)
        raise HTTPException(status_code=500, detail="Internal server error") from e


@router.put(
    "/{entry_id}",
    response_model=CollectionEntryOut,
    status_code=status.HTTP_200_OK,
    summary="Update a collection entry",
    description="Update fields of a collection entry owned by the authenticated user.",
)
def update_collection_entry(
    collection_id: int,
    entry_id: int,
    update_data: CollectionEntryUpdate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    """
    Update a collection entry for t
    he authenticated user.
    """
    user_id = int(current_user["id"])
    service = CollectionEntryService()
    # Check if collection exists first
    collection = db.query(Collection).filter(Collection.id == collection_id).first()
    if not collection:
        raise HTTPException(status_code=404, detail="Collection not found")
    try:
        result = service.update_entry(
            collection_id=collection_id,
            entry_id=entry_id,
            user_id=user_id,
            update_data=update_data.model_dump(exclude_unset=True),
            db=db,
        )
        return result
    except CollectionEntryNotFoundError as exc:
        raise HTTPException(status_code=404, detail="Entry not found") from exc
    except CollectionEntryPermissionError as exc:
        raise HTTPException(status_code=403, detail="Permission denied") from exc


@router.delete(
    "/{entry_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete a collection entry",
    description="Delete a collection entry owned by the authenticated user.",
)
def delete_collection_entry(
    collection_id: int,
    entry_id: int,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    """
    Delete a collection entry for the authenticated user.
    """
    user_id = int(current_user["id"])
    service = CollectionEntryService()
    logger.info(
        "User %s attempting to delete entry %s from collection %s",
        user_id,
        entry_id,
        collection_id,
    )

    # Check if collection exists first
    collection = db.query(Collection).filter(Collection.id == collection_id).first()
    if not collection:
        raise HTTPException(status_code=404, detail="Collection not found")

    try:
        service.delete_entry(
            collection_id=collection_id,
            entry_id=entry_id,
            user_id=user_id,
            db=db,
        )
        logger.info(
            "Collection entry %s deleted from collection %s by user %s",
            entry_id,
            collection_id,
            user_id,
        )
        return  # 204 No Content - empty response body
    except CollectionEntryNotFoundError as exc:
        logger.warning(
            "Entry %s not found in collection %s for user %s",
            entry_id,
            collection_id,
            user_id,
        )
        raise HTTPException(status_code=404, detail="Entry not found") from exc
    except CollectionEntryPermissionError as exc:
        logger.warning(
            "User %s does not have permission for collection %s", user_id, collection_id
        )
        raise HTTPException(status_code=403, detail="Permission denied") from exc
    except Exception as e:
        logger.error("Unexpected error deleting entry: %s", e)
        raise HTTPException(status_code=500, detail="Internal server error") from e
