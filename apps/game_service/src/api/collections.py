"""
API routes for user game collections.
Implements routes:
    POST /collections/ for creating a new collection
    GET /collections/ for listing user's collections.
    GET /collections/{collection_id} for getting details of a specific collection.
    PUT /collections/{collection_id} for updating a collection.
    DELETE /collections/{collection_id} for deleting a collection.
"""

import logging

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from apps.game_service.src.api.dependencies import get_current_user
from apps.game_service.src.core.database import get_db
from apps.game_service.src.schemas.collection import (
    CollectionCreate,
    CollectionOut,
    CollectionUpdate,
)
from apps.game_service.src.services.collection_service import (
    CollectionNotFoundError,
    CollectionService,
)

logger = logging.getLogger("collections_api")

router = APIRouter()


@router.post(
    "/collections/",
    response_model=CollectionOut,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new collection",
    tags=["collections"],
)
def create_collection(
    data: CollectionCreate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    """
    Create a new collection for the authenticated user.
    """
    service = CollectionService()
    try:
        logger.info(
            "Calling create_collection for user_id=%s with data=%s",
            current_user["id"],
            data,
        )
        result = service.create_collection(current_user["id"], data, db)
        logger.info("create_collection result: %s", result)
        return result
    except ValueError as e:
        logger.error("ValueError: %s", e)
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=str(e),
        ) from e
    except Exception as e:
        logger.error("Unhandled exception: %s", e)
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e),
        ) from e


@router.get(
    "/collections/",
    response_model=list[CollectionOut],
    status_code=status.HTTP_200_OK,
    summary="List all collections",
    tags=["collections"],
)
def list_collections(
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    """
    List all collections for the authenticated user.

    Returns a list of collection objects owned by the current user.
    The list will be empty if the user has no collections.
    """
    service = CollectionService()
    try:
        logger.debug(
            "Calling list_collections for user_id=%s",
            current_user["id"],
        )
        collections = service.list_collections(user_id=current_user["id"], db=db)
        logger.debug("Found %d collections for user", len(collections))
        return collections
    except Exception as e:
        logger.error("Error listing collections: %s", e)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred while retrieving collections",
        ) from e


@router.get(
    "/collections/{collection_id}",
    response_model=CollectionOut,
    status_code=status.HTTP_200_OK,
    summary="Get collection details",
    tags=["collections"],
)
def get_collection_details(
    collection_id: int,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    """
    Retrieve details for a specific collection owned by the authenticated user.
    Returns 404 if not found or not owned by user.
    Returns 422 for validation errors.
    """
    service = CollectionService()
    try:
        user_id = int(current_user["id"])
        logger.info(
            "Calling get_collection_by_id for user_id=%s, collection_id=%s",
            user_id,
            collection_id,
        )
        collection = service.get_collection_by_id(collection_id, user_id, db)
        return CollectionOut.model_validate(collection, from_attributes=True)
    except CollectionNotFoundError as e:
        logger.warning("Collection not found: %s", e)
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e),
        ) from e
    except HTTPException as e:
        # Re-raise HTTPException so FastAPI can handle it
        raise e
    except TypeError as e:
        logger.error("TypeError: %s", e)
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=str(e),
        ) from e
    except Exception as e:
        logger.error("Unhandled exception: %s", e)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred while retrieving the collection.",
        ) from e


@router.put(
    "/collections/{collection_id}",
    response_model=CollectionOut,
    status_code=status.HTTP_200_OK,
    summary="Update a collection",
    tags=["collections"],
)
def update_collection(
    collection_id: int,
    data: CollectionUpdate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    """
    Update a specific collection owned by the authenticated user.

    Only fields that are provided will be updated.
    Returns 404 if the collection is not found or not owned by the user.
    Returns 409 if the collection name already exists for the user.
    Returns 422 for validation errors.
    """
    service = CollectionService()
    try:
        user_id = int(current_user["id"])
        logger.info(
            "Calling update_collection for user_id=%s, collection_id=%s with data=%s",
            user_id,
            collection_id,
            data,
        )
        collection = service.update_collection(user_id, collection_id, data, db)
        logger.info("Collection updated: %s", collection)
        return collection
    except CollectionNotFoundError as e:
        logger.warning("Collection not found: %s", e)
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e),
        ) from e
    except ValueError as e:
        logger.warning("Value error: %s", e)
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=str(e),
        ) from e
    except PermissionError as e:
        logger.warning("Permission error: %s", e)
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            # Use 404 instead of 403 to avoid revealing resource existence
            detail="Collection not found or not owned by user.",
        ) from e
    except TypeError as e:
        logger.error("TypeError: %s", e)
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=str(e),
        ) from e
    except Exception as e:
        logger.error("Unhandled exception: %s", e)
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred while updating the collection.",
        ) from e


@router.delete(
    "/collections/{collection_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete a collection",
    tags=["collections"],
)
def delete_collection(
    collection_id: int,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    """
    Delete a collection owned by the authenticated user.

    Returns 204 on successful deletion.
    Returns 404 if the collection is not found or not owned by the user.
    """
    service = CollectionService()
    try:
        user_id = int(current_user["id"])
        logger.info(
            "Calling delete_collection for user_id=%s, collection_id=%s",
            user_id,
            collection_id,
        )
        result = service.delete_collection(user_id, collection_id, db)
        if result:
            logger.info("Collection deleted: id=%s", collection_id)
            return None  # FastAPI will return 204 NO CONTENT
        # Should not reach here as service should raise exceptions for errors
        logger.warning("Collection not deleted: id=%s", collection_id)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to delete collection.",
        )
    except CollectionNotFoundError as e:
        logger.warning("Collection not found: %s", e)
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e),
        ) from e
    except PermissionError as e:
        logger.warning("Permission error: %s", e)
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            # Use 404 instead of 403 to avoid revealing resource existence
            detail="Collection not found or not owned by user.",
        ) from e
    except TypeError as e:
        logger.error("TypeError: %s", e)
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=str(e),
        ) from e
    except Exception as e:
        logger.error("Unhandled exception: %s", e)
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred while deleting the collection.",
        ) from e
