"""Pydantic schema for user login request."""

from pydantic import BaseModel, Field


# pylint: disable=too-few-public-methods
# Reason: Pydantic models are data containers and typically do not require public methods.
class UserLogin(BaseModel):
    """Schema for user login credentials. Used for validating login requests."""

    username: str = Field(..., min_length=3, max_length=50)
    password: str = Field(..., min_length=8, max_length=128)

    class Config:
        """Pydantic config for OpenAPI example generation."""

        json_schema_extra = {
            "example": {"username": "loginuser", "password": "LoginPass123"}
        }
