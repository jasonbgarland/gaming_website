"""
Pydantic schemas for CollectionEntry.
"""

# pylint: disable=too-few-public-methods
from datetime import date, datetime
from typing import Any, Dict, Optional

from pydantic import BaseModel, Field


class GameOut(BaseModel):
    """Schema for returning game details in collection entries."""

    id: int
    igdb_id: Optional[int] = None
    name: str
    platform: str
    release_date: Optional[date] = None
    cover_url: Optional[str] = None
    genre: Optional[str] = None

    class Config:
        """Pydantic config for ORM mode (from_attributes)."""

        from_attributes = True


class CollectionEntryBase(BaseModel):
    """Base schema for CollectionEntry (shared fields)."""

    game_id: int = Field(..., description="ID of the game")
    notes: Optional[str] = Field(None, max_length=1000)
    status: Optional[str] = Field(None, max_length=50)
    rating: Optional[int] = Field(None, ge=0, le=10)
    custom_tags: Optional[Dict[str, Any]] = Field(
        None, description="Custom tags as key-value pairs"
    )


class CollectionEntryCreate(CollectionEntryBase):
    """Schema for creating a new collection entry. Inherits all fields from CollectionEntryBase."""

    # No additional fields; docstring only for clarity.


class CollectionEntryUpdate(BaseModel):
    """Schema for updating a collection entry (all fields optional)."""

    notes: Optional[str] = Field(None, max_length=1000)
    status: Optional[str] = Field(None, max_length=50)
    rating: Optional[int] = Field(None, ge=0, le=10)
    custom_tags: Optional[Dict[str, Any]] = Field(None)


class CollectionEntryOut(CollectionEntryBase):
    """Schema for returning a collection entry (output)."""

    id: int
    collection_id: int
    added_at: datetime
    game: GameOut  # Include full game details

    class Config:
        """Pydantic config for ORM mode (from_attributes)."""

        from_attributes = True
