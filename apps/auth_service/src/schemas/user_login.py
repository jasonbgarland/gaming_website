"""Pydantic schema for user login request."""

from pydantic import BaseModel, EmailStr, Field


# pylint: disable=too-few-public-methods
# Reason: Pydantic models are data containers and typically do not require public methods.
class UserLogin(BaseModel):
    """Schema for user login credentials. Used for validating login requests."""

    email: EmailStr = Field(..., description="User's email address")
    password: str = Field(..., min_length=8, max_length=128)

    class Config:
        """Pydantic config for OpenAPI example generation."""

        json_schema_extra = {
            "example": {"email": "user@example.com", "password": "LoginPass123"}
        }
