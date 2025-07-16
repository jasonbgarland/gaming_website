"""
Pydantic schemas for Collection and CollectionEntry.
"""

# pylint: disable=too-few-public-methods
from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field


class CollectionBase(BaseModel):
    """Base schema for Collection (shared fields)."""

    name: str = Field(
        ...,
        min_length=2,  # Minimum length of 2 characters
        max_length=100,
        pattern=r"^[A-Za-z0-9 ]+$",
        description="Collection name (alphanumeric and spaces only)",
    )
    description: Optional[str] = Field(
        None, max_length=500, description="Optional description"
    )


class CollectionCreate(CollectionBase):
    """Schema for creating a new collection. Inherits all fields from CollectionBase."""

    # No additional fields; docstring only for clarity.


class CollectionUpdate(BaseModel):
    """Schema for updating a collection (all fields optional)."""

    name: Optional[str] = Field(None, min_length=1, max_length=100)
    description: Optional[str] = Field(None, max_length=500)


class CollectionOut(CollectionBase):
    """Schema for returning a collection (output)."""

    id: int
    user_id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        """Pydantic config for ORM mode (from_attributes)."""

        from_attributes = True
