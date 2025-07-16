# pylint: disable=too-few-public-methods
# Reason: Pydantic models are data containers and typically do not require public methods.
"""Pydantic schema for JWT access token response."""
from pydantic import BaseModel


class TokenOut(BaseModel):
    """Response schema for JWT access token (returned by /login endpoint)."""

    access_token: str
    token_type: str

    class Config:
        """Pydantic config for OpenAPI example generation."""

        json_schema_extra = {
            "example": {"access_token": "<JWT>", "token_type": "bearer"}
        }
