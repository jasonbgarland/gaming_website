"""
FastAPI routes for IGDB endpoints: search, game details, genres, and platforms.
"""

from fastapi import APIRouter, Query, HTTPException, Depends, Path
from src.igdb.auth import IGDBAuth
from src.igdb.client import IGDBClient
from src.igdb.schemas import GameOut, GenreOut, PlatformOut, GameFilters


router = APIRouter()


def get_igdb_client() -> IGDBClient:
    """
    Dependency provider for IGDBClient, using default auth.
    """
    auth = IGDBAuth()
    return IGDBClient(auth=auth)


@router.get(
    "/games",
    response_model=list[GameOut],
    summary="Batch fetch game details by IGDB IDs",
    responses={
        200: {"description": "List of games for the provided IDs."},
        500: {
            "description": "Internal server error.",
            "content": {
                "application/json": {"example": {"detail": "Internal server error."}}
            },
        },
    },
)
def get_games_by_ids(
    ids: str = Query(..., description="Comma-separated list of IGDB game IDs"),
    client: IGDBClient = Depends(get_igdb_client),
):
    """
    Batch fetch game details by IGDB IDs.

    Args:
        ids (str): Comma-separated list of IGDB game IDs.
        client (IGDBClient): Injected IGDB client.

    Returns:
        List[GameOut]: List of game details.
    """
    try:
        # Only allow strictly positive integers
        id_list = [int(i) for i in ids.split(",") if i.strip().isdigit() and int(i) > 0]
        if not id_list:
            return []
        return client.get_games_by_ids(id_list)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) from e


@router.get(
    "/genres",
    response_model=list[GenreOut],
    summary="List all game genres from IGDB",
    responses={
        200: {"description": "List of genres."},
        500: {
            "description": "Internal server error.",
            "content": {
                "application/json": {"example": {"detail": "Internal server error."}}
            },
        },
    },
)
def get_genres(client: IGDBClient = Depends(get_igdb_client)):
    """
    List all game genres from IGDB.

    Args:
        client (IGDBClient): Injected IGDB client.

    Returns:
        List[GenreOut]: List of genres.
    """
    try:
        return client.get_genres()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) from e


@router.get(
    "/platforms",
    response_model=list[PlatformOut],
    summary="List all platforms from IGDB",
    responses={
        200: {"description": "List of platforms."},
        500: {
            "description": "Internal server error.",
            "content": {
                "application/json": {"example": {"detail": "Internal server error."}}
            },
        },
    },
)
def get_platforms(client: IGDBClient = Depends(get_igdb_client)):
    """
    List all platforms from IGDB.

    Args:
        client (IGDBClient): Injected IGDB client.

    Returns:
        List[PlatformOut]: List of platforms.
    """
    try:
        return client.get_platforms()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) from e


@router.get(
    "/games/{game_id}",
    response_model=GameOut,
    summary="Get details for a specific game by IGDB ID",
    responses={
        200: {"description": "Game details for the given ID."},
        404: {
            "description": "Game not found.",
            "content": {
                "application/json": {
                    "example": {"detail": "Game with id 123 not found"}
                }
            },
        },
        422: {"description": "Validation error for negative or zero ID."},
        500: {
            "description": "Internal server error.",
            "content": {
                "application/json": {"example": {"detail": "Internal server error."}}
            },
        },
    },
)
def get_game_by_id(
    game_id: int = Path(
        ..., gt=0, description="IGDB game ID (must be positive integer)"
    ),
    client: IGDBClient = Depends(get_igdb_client),
):
    """
    Get details for a specific game by IGDB ID.

    Args:
        game_id (int): IGDB game ID.
        client (IGDBClient): Injected IGDB client.

    Returns:
        GameOut: Game details.
    """
    try:
        game = client.get_game_by_id(game_id)
        return game
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e)) from e
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) from e


@router.get(
    "/search",
    response_model=list[GameOut],
    summary="Search for games using the IGDB API",
    responses={
        200: {"description": "List of games matching the search query."},
        500: {
            "description": "Internal server error.",
            "content": {
                "application/json": {"example": {"detail": "Internal server error."}}
            },
        },
    },
)
def search_games(
    q: str = Query(..., min_length=1, description="Game search query"),
    client: IGDBClient = Depends(get_igdb_client),
):
    """
    Search for games using the IGDB API.

    Args:
        q (str): Game search query string.
        client (IGDBClient): Injected IGDB client.

    Returns:
        List[GameOut]: List of search results.
    """
    try:
        # Reject queries that are only whitespace
        if not q.strip():
            raise HTTPException(
                status_code=422, detail="Query cannot be empty or whitespace."
            )
        results = client.search_games(q)
        return results
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) from e


# pylint: disable=too-many-arguments,too-many-positional-arguments,too-many-branches
@router.get(
    "/search-enhanced",
    response_model=list[GameOut],
    summary="Enhanced search for games with advanced filters",
    responses={
        200: {"description": "List of games matching the search query and filters."},
        500: {
            "description": "Internal server error.",
            "content": {
                "application/json": {"example": {"detail": "Internal server error."}}
            },
        },
    },
)
def search_games_enhanced(
    q: str = Query(..., min_length=1, description="Game search query"),
    # Platform filters
    platforms: str = Query(
        None, description="Comma-separated platform IDs (e.g., '6,48,130')"
    ),
    # Year filters
    years: str = Query(None, description="Comma-separated years (e.g., '2020,2021')"),
    year_start: int = Query(
        None, description="Start year for range (e.g., 2018)", ge=1970, le=2030
    ),
    year_end: int = Query(
        None, description="End year for range (e.g., 2023)", ge=1970, le=2030
    ),
    # Genre filters
    genres: str = Query(
        None, description="Comma-separated genre IDs (e.g., '4,12,31')"
    ),
    # Rating filters
    min_rating: float = Query(
        None, description="Minimum IGDB rating (0-100)", ge=0.0, le=100.0
    ),
    max_rating: float = Query(
        None, description="Maximum IGDB rating (0-100)", ge=0.0, le=100.0
    ),
    # Theme filters
    themes: str = Query(
        None, description="Comma-separated theme IDs (e.g., '18,17,23')"
    ),
    # Player perspective filters
    player_perspectives: str = Query(
        None, description="Comma-separated perspective IDs (e.g., '1,3')"
    ),
    client: IGDBClient = Depends(get_igdb_client),
):
    """
    Enhanced search for games using the IGDB API with advanced filtering options.

    This endpoint allows filtering by platforms, release years, genres,
    ratings, themes, player perspectives, and more. All filters are optional
    and can be combined.

    Args:
        q (str): Game search query string.
        platforms (str, optional): Comma-separated platform IDs.
        years (str, optional): Comma-separated discrete years.
        year_start (int, optional): Start year for year range filter.
        year_end (int, optional): End year for year range filter.
        genres (str, optional): Comma-separated genre IDs.
        min_rating (float, optional): Minimum IGDB rating.
        max_rating (float, optional): Maximum IGDB rating.
        themes (str, optional): Comma-separated theme IDs.
        player_perspectives (str, optional): Comma-separated perspective IDs.
        client (IGDBClient): Injected IGDB client.

    Returns:
        List[GameOut]: List of search results matching query and filters.
    """
    try:
        # Reject queries that are only whitespace
        if not q.strip():
            raise HTTPException(
                status_code=422, detail="Query cannot be empty or whitespace."
            )

        # Build filters object
        filters_dict = {}

        # Parse platform IDs
        if platforms:
            try:
                filters_dict["platforms"] = [
                    int(p.strip()) for p in platforms.split(",") if p.strip()
                ]
            except ValueError as e:
                raise HTTPException(
                    status_code=422, detail=f"Invalid platform IDs: {platforms}"
                ) from e

        # Parse discrete years
        if years:
            try:
                filters_dict["years"] = [
                    int(y.strip()) for y in years.split(",") if y.strip()
                ]
            except ValueError as e:
                raise HTTPException(
                    status_code=422, detail=f"Invalid years: {years}"
                ) from e

        # Parse year range
        if year_start is not None and year_end is not None:
            if year_start > year_end:
                raise HTTPException(
                    status_code=422, detail="Start year must be <= end year"
                )
            filters_dict["year_range"] = {"start": year_start, "end": year_end}

        # Parse genre IDs
        if genres:
            try:
                filters_dict["genres"] = [
                    int(g.strip()) for g in genres.split(",") if g.strip()
                ]
            except ValueError as e:
                raise HTTPException(
                    status_code=422, detail=f"Invalid genre IDs: {genres}"
                ) from e

        # Add rating filters
        if min_rating is not None:
            filters_dict["min_rating"] = min_rating
        if max_rating is not None:
            filters_dict["max_rating"] = max_rating

        # Parse theme IDs
        if themes:
            try:
                filters_dict["themes"] = [
                    int(t.strip()) for t in themes.split(",") if t.strip()
                ]
            except ValueError as e:
                raise HTTPException(
                    status_code=422, detail=f"Invalid theme IDs: {themes}"
                ) from e

        # Parse player perspective IDs
        if player_perspectives:
            try:
                filters_dict["player_perspectives"] = [
                    int(p.strip()) for p in player_perspectives.split(",") if p.strip()
                ]
            except ValueError as e:
                raise HTTPException(
                    status_code=422,
                    detail=f"Invalid perspective IDs: {player_perspectives}",
                ) from e

        # Create GameFilters object if we have any filters
        filters = None
        if filters_dict:
            filters = GameFilters(**filters_dict)

        # Use enhanced search method
        results = client.search_games_enhanced(q, filters)
        return results
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) from e
