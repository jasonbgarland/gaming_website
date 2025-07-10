"""
Pydantic schemas for IGDB API responses: genres, platforms, and games.
"""

from pydantic import BaseModel, Field


# pylint: disable=too-few-public-methods
class GenreOut(BaseModel):
    """
    Pydantic schema for a genre returned by the IGDB API.
    """

    id: int = Field(..., description="Unique genre ID from IGDB.")
    name: str = Field(..., description="Name of the genre.")

    class Config:
        """Pydantic config for GenreOut schema."""

        json_schema_extra = {"example": {"id": 4, "name": "Action"}}


class PlatformOut(BaseModel):
    """
    Pydantic schema for a platform returned by the IGDB API.
    """

    id: int = Field(..., description="Unique platform ID from IGDB.")
    name: str = Field(..., description="Name of the platform.")

    class Config:
        """Pydantic config for PlatformOut schema."""

        json_schema_extra = {"example": {"id": 6, "name": "Nintendo Switch"}}


# pylint: disable=too-few-public-methods


class GameOut(BaseModel):
    """
    Pydantic schema for a game returned by the IGDB API.
    """

    id: int = Field(..., description="Unique game ID from IGDB.")
    name: str = Field(..., description="Game title.")
    cover_url: str | None = Field(None, description="URL to the game's cover image.")
    summary: str | None = Field(
        None, description="Short summary or description of the game."
    )
    release_date: int | None = Field(
        None, description="Release date as a Unix timestamp (seconds since epoch)."
    )
    genres: list[str] | None = Field(None, description="List of genre names.")
    platforms: list[str] | None = Field(None, description="List of platform names.")

    class Config:
        """Pydantic config for GameOut schema."""

        json_schema_extra = {
            "description": "A game object with details from IGDB.",
            "examples": [
                {
                    "id": 1022,
                    "name": "The Legend of Zelda",
                    "cover_url": "https://images.igdb.com/igdb/image/upload/t_cover_big/co1r6b.jpg",
                    "summary": "An epic adventure game...",
                    "release_date": 482112000,
                    "genres": ["Adventure", "Action"],
                    "platforms": ["Nintendo Switch", "Wii U"],
                },
                {
                    "id": 1234,
                    "name": "Super Mario Bros.",
                    "cover_url": "https://images.igdb.com/igdb/image/upload/t_cover_big/co2abc.jpg",
                    "summary": "Classic platformer.",
                    "release_date": 468288000,
                    "genres": ["Platformer"],
                    "platforms": ["NES"],
                },
            ],
        }
