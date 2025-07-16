"""Pydantic schema for user info returned by API."""

from pydantic import BaseModel


# pylint: disable=too-few-public-methods
# Reason: Pydantic models are data containers and typically do not require public methods.
class UserOut(BaseModel):
    """Response schema for user info (returned by /signup and /me endpoints)."""

    username: str
    email: str

    class Config:
        """Pydantic config for OpenAPI example generation."""

        json_schema_extra = {
            "example": {"username": "testuser", "email": "testuser@example.com"}
        }
