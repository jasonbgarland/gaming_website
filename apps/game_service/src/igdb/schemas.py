"""
Pydantic schemas for IGDB API responses and requests: genres, platforms, games, and filters.
"""

from typing import List, Optional
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


class CoverImages(BaseModel):
    """
    Pydantic schema for different sizes of cover images.
    """

    thumb: str | None = Field(None, description="Thumbnail size image URL (90x128).")
    small: str | None = Field(None, description="Small size image URL (227x320).")
    medium: str | None = Field(None, description="Medium size image URL (264x374).")
    large: str | None = Field(None, description="Large size image URL (1280x720).")


class GameOut(BaseModel):
    """
    Pydantic schema for a game returned by the IGDB API.
    """

    id: int = Field(..., description="Unique game ID from IGDB.")
    name: str = Field(..., description="Game title.")
    cover_url: str | None = Field(None, description="URL to the game's cover image.")
    cover_images: CoverImages | None = Field(
        None, description="Multiple sizes of cover images."
    )
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


class YearRange(BaseModel):
    """
    Pydantic schema for year range filter.
    """

    start: int = Field(..., ge=1970, le=2030, description="Start year (inclusive)")
    end: int = Field(..., ge=1970, le=2030, description="End year (inclusive)")


class GameFilters(BaseModel):
    """
    Pydantic schema for game search filters.

    Supports multiple filter types that can be combined:
    - Platform filtering by IGDB platform IDs
    - Year filtering by discrete years or year ranges

    Can be created from:
    - Direct instantiation: GameFilters(platforms=[6, 48])
    - JSON dict: GameFilters.model_validate({"platforms": [6, 48]})
    - FastAPI query params: GameFilters(**request_params)
    """

    platforms: Optional[List[int]] = Field(
        None, description="List of IGDB platform IDs to filter by", example=[6, 48, 130]
    )

    years: Optional[List[int]] = Field(
        None,
        description="List of discrete years to filter by",
        example=[2020, 2021, 2022],
    )

    year_range: Optional[YearRange] = Field(
        None,
        description="Year range filter (inclusive)",
        example={"start": 2018, "end": 2022},
    )

    genres: Optional[List[int]] = Field(
        None,
        description="List of IGDB genre IDs to filter by",
        example=[4, 12, 31],  # Action, RPG, Adventure
    )

    ratings: Optional[List[int]] = Field(
        None,
        description="List of IGDB age rating IDs to filter by",
        example=[6, 8],  # Everyone, Teen
    )

    game_modes: Optional[List[int]] = Field(
        None,
        description="List of IGDB game mode IDs to filter by",
        example=[1, 2],  # Single-player, Multiplayer
    )

    themes: Optional[List[int]] = Field(
        None,
        description="List of IGDB theme IDs to filter by (Horror, Sci-Fi, Fantasy, etc.)",
        example=[18, 17, 23],  # Horror, Sci-Fi, Fantasy
    )

    player_perspectives: Optional[List[int]] = Field(
        None,
        description="List of IGDB player perspective IDs (First-person, Third-person, etc.)",
        example=[1, 3],  # First-person, Third-person
    )

    release_status: Optional[List[int]] = Field(
        None,
        description="List of IGDB release status IDs (Released, Coming Soon, Early Access, etc.)",
        example=[0, 2, 3],  # Released, Alpha, Beta
    )

    franchises: Optional[List[int]] = Field(
        None,
        description="List of IGDB franchise IDs to filter by",
        example=[170, 421],  # Example franchise IDs
    )

    companies: Optional[List[int]] = Field(
        None,
        description="List of IGDB company IDs to filter by (developers/publishers)",
        example=[70, 1],  # Example company IDs
    )

    keywords: Optional[List[int]] = Field(
        None,
        description="List of IGDB keyword IDs to filter by (Open World, Battle Royale, etc.)",
        example=[270, 310],  # Example keyword IDs
    )

    multiplayer_modes: Optional[List[int]] = Field(
        None,
        description="List of IGDB multiplayer mode IDs (Online, Local, etc.)",
        example=[1, 2, 3],  # Example multiplayer mode IDs
    )

    min_rating: Optional[float] = Field(
        None, ge=0.0, le=100.0, description="Minimum IGDB rating (0-100)", example=75.0
    )

    max_rating: Optional[float] = Field(
        None, ge=0.0, le=100.0, description="Maximum IGDB rating (0-100)", example=95.0
    )

    min_metacritic: Optional[int] = Field(
        None, ge=0, le=100, description="Minimum Metacritic score (0-100)", example=70
    )

    max_metacritic: Optional[int] = Field(
        None, ge=0, le=100, description="Maximum Metacritic score (0-100)", example=90
    )

    esrb_ratings: Optional[List[int]] = Field(
        None,
        description="List of ESRB rating IDs (separate from general age ratings)",
        example=[6, 7, 8],  # E, E10+, T
    )

    game_engines: Optional[List[int]] = Field(
        None,
        description="List of IGDB game engine IDs (Unity, Unreal, etc.)",
        example=[1, 2],  # Example engine IDs
    )

    collections: Optional[List[int]] = Field(
        None,
        description="List of IGDB collection IDs (game series/collections)",
        example=[1, 2],  # Example collection IDs
    )

    class Config:
        """Pydantic config for GameFilters schema."""

        json_schema_extra = {
            "example": {
                "platforms": [6, 48, 130],
                "years": [2020, 2021],
                "year_range": {"start": 2018, "end": 2022},
                "genres": [4, 12, 31],
                "ratings": [6, 8],
                "game_modes": [1, 2],
                "themes": [18, 17, 23],
                "player_perspectives": [1, 3],
                "release_status": [0, 2],
                "franchises": [170, 421],
                "companies": [70, 1],
                "keywords": [270, 310],
                "multiplayer_modes": [1, 2, 3],
                "min_rating": 75.0,
                "max_rating": 95.0,
                "min_metacritic": 70,
                "max_metacritic": 90,
                "esrb_ratings": [6, 7, 8],
                "game_engines": [1, 2],
                "collections": [1, 2],
            }
        }
