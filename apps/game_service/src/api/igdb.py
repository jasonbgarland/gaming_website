"""
FastAPI routes for IGDB endpoints: search, game details, genres, and platforms.
"""

from fastapi import APIRouter, Query, HTTPException, Depends, Path
from src.igdb.auth import IGDBAuth
from src.igdb.client import IGDBClient
from src.igdb.schemas import GameOut, GenreOut, PlatformOut


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
