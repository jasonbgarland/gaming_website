"""Pydantic schema for user signup request."""

from pydantic import BaseModel, EmailStr, Field


# pylint: disable=too-few-public-methods
# Reason: Pydantic models are data containers and typically do not require public methods.
class UserSignup(BaseModel):
    """Schema for user signup data. Used for validating user registration requests."""

    username: str = Field(..., min_length=3, max_length=50)
    email: EmailStr
    password: str = Field(..., min_length=8, max_length=128)

    class Config:
        """Pydantic config for OpenAPI example generation."""

        json_schema_extra = {
            "example": {
                "username": "testuser",
                "email": "testuser@example.com",
                "password": "StrongPassword123",
            }
        }
