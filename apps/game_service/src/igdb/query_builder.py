"""
IGDB query builder for constructing API queries.

This module provides functionality to build IGDB API query strings
from search terms and filters.
"""

from datetime import datetime, timezone
from typing import Optional
from src.igdb.schemas import GameFilters


# pylint: disable=too-many-branches,too-many-statements
def build_igdb_query(search_term: str, filters: Optional[GameFilters] = None) -> str:
    """
    Build an IGDB API query string from search term and filters.

    Args:
        search_term: The text to search for
        filters: GameFilters instance with validated filter parameters (optional)

    Returns:
        Complete IGDB query string ready for POST request
    """
    base_fields = (
        "id,name,cover.url,summary,first_release_date,genres.name,platforms.name"
    )
    base_query = f'search "{search_term}"; fields {base_fields}; limit 10;'

    if not filters:
        return base_query

    where_clauses = []

    # Handle platforms filter
    if filters.platforms:
        clause = _build_platforms_clause(filters.platforms)
        if clause:
            where_clauses.append(clause)

    # Handle discrete years filter
    if filters.years:
        clause = _build_years_clause(filters.years)
        if clause:
            where_clauses.append(clause)

    # Handle year range filter
    if filters.year_range:
        clause = _build_year_range_clause(filters.year_range)
        if clause:
            where_clauses.append(clause)

    # Handle genres filter
    if filters.genres:
        clause = _build_genres_clause(filters.genres)
        if clause:
            where_clauses.append(clause)

    # Handle ratings filter
    if filters.ratings:
        clause = _build_ratings_clause(filters.ratings)
        if clause:
            where_clauses.append(clause)

    # Handle game modes filter
    if filters.game_modes:
        clause = _build_game_modes_clause(filters.game_modes)
        if clause:
            where_clauses.append(clause)

    # Handle themes filter
    if filters.themes:
        clause = _build_themes_clause(filters.themes)
        if clause:
            where_clauses.append(clause)

    # Handle player perspectives filter
    if filters.player_perspectives:
        clause = _build_player_perspectives_clause(filters.player_perspectives)
        if clause:
            where_clauses.append(clause)

    # Handle release status filter
    if filters.release_status:
        clause = _build_release_status_clause(filters.release_status)
        if clause:
            where_clauses.append(clause)

    # Handle franchises filter
    if filters.franchises:
        clause = _build_franchises_clause(filters.franchises)
        if clause:
            where_clauses.append(clause)

    # Handle companies filter
    if filters.companies:
        clause = _build_companies_clause(filters.companies)
        if clause:
            where_clauses.append(clause)

    # Handle keywords filter
    if filters.keywords:
        clause = _build_keywords_clause(filters.keywords)
        if clause:
            where_clauses.append(clause)

    # Handle multiplayer modes filter
    if filters.multiplayer_modes:
        clause = _build_multiplayer_modes_clause(filters.multiplayer_modes)
        if clause:
            where_clauses.append(clause)

    # Handle rating range filters
    if filters.min_rating is not None or filters.max_rating is not None:
        clause = _build_rating_range_clause(filters.min_rating, filters.max_rating)
        if clause:
            where_clauses.append(clause)

    # Handle metacritic range filters
    if filters.min_metacritic is not None or filters.max_metacritic is not None:
        clause = _build_metacritic_range_clause(
            filters.min_metacritic, filters.max_metacritic
        )
        if clause:
            where_clauses.append(clause)

    # Handle ESRB ratings filter
    if filters.esrb_ratings:
        clause = _build_esrb_ratings_clause(filters.esrb_ratings)
        if clause:
            where_clauses.append(clause)

    # Handle game engines filter
    if filters.game_engines:
        clause = _build_game_engines_clause(filters.game_engines)
        if clause:
            where_clauses.append(clause)

    # Handle collections filter
    if filters.collections:
        clause = _build_collections_clause(filters.collections)
        if clause:
            where_clauses.append(clause)

    where_clause = ""
    if where_clauses:
        where_clause = f" where {' & '.join(where_clauses)};"

    return f'search "{search_term}";{where_clause} fields {base_fields}; limit 10;'


# ===============================================
# Private Helper Methods
# ===============================================


def _year_to_unix_range(year: int) -> tuple:
    """Convert a year to Unix timestamp range (start of year to start of next year) in UTC."""
    # Use UTC to avoid timezone issues
    start_dt = datetime(year, 1, 1, tzinfo=timezone.utc)
    end_dt = datetime(year + 1, 1, 1, tzinfo=timezone.utc)
    return int(start_dt.timestamp()), int(end_dt.timestamp())


def _build_platforms_clause(platforms) -> str:
    """
    Build WHERE clause for platforms filter.

    Args:
        platforms: List of platform IDs

    Returns:
        WHERE clause string for platforms, or empty string if invalid
    """
    try:
        ids = ",".join(str(int(p)) for p in platforms)
        return f"platforms = ({ids})"
    except (ValueError, TypeError):
        # If conversion fails (non-integer values), ignore the platforms filter
        return ""


def _build_years_clause(years) -> str:
    """
    Build WHERE clause for discrete years filter.

    Args:
        years: List of year integers

    Returns:
        WHERE clause string for years, or empty string if invalid
    """
    year_conditions = []
    try:
        for year in years:
            start_ts, end_ts = _year_to_unix_range(int(year))
            year_conditions.append(
                f"first_release_date >= {start_ts} & first_release_date < {end_ts}"
            )

        if year_conditions:
            if len(year_conditions) == 1:
                # Single year: no parentheses needed
                return year_conditions[0]
            # Multiple years: OR them together with parentheses
            return " | ".join(f"({condition})" for condition in year_conditions)
    except (ValueError, TypeError):
        # If conversion fails, ignore the years filter
        pass
    return ""


def _build_year_range_clause(year_range) -> str:
    """
    Build WHERE clause for year range filter.

    Args:
        year_range: YearRange Pydantic model with 'start' and 'end' attributes

    Returns:
        WHERE clause string for year range, or empty string if invalid
    """
    try:
        # year_range is already validated by Pydantic
        start_year = year_range.start
        end_year = year_range.end
        start_ts, _ = _year_to_unix_range(start_year)
        _, end_ts = _year_to_unix_range(end_year)
        return f"first_release_date >= {start_ts} & first_release_date < {end_ts}"
    except (ValueError, TypeError, AttributeError):
        # If conversion fails, ignore the year_range filter
        pass
    return ""


def _build_genres_clause(genres) -> str:
    """
    Build WHERE clause for genres filter.

    Args:
        genres: List of genre IDs

    Returns:
        WHERE clause string for genres, or empty string if invalid
    """
    try:
        ids = ",".join(str(int(g)) for g in genres)
        return f"genres = ({ids})"
    except (ValueError, TypeError):
        # If conversion fails (non-integer values), ignore the genres filter
        return ""


def _build_ratings_clause(ratings) -> str:
    """
    Build WHERE clause for age ratings filter.

    Args:
        ratings: List of age rating IDs

    Returns:
        WHERE clause string for ratings, or empty string if invalid
    """
    try:
        ids = ",".join(str(int(r)) for r in ratings)
        return f"age_ratings = ({ids})"
    except (ValueError, TypeError):
        # If conversion fails (non-integer values), ignore the ratings filter
        return ""


def _build_game_modes_clause(game_modes) -> str:
    """
    Build WHERE clause for game modes filter.

    Args:
        game_modes: List of game mode IDs

    Returns:
        WHERE clause string for game modes, or empty string if invalid
    """
    try:
        ids = ",".join(str(int(m)) for m in game_modes)
        return f"game_modes = ({ids})"
    except (ValueError, TypeError):
        # If conversion fails (non-integer values), ignore the game modes filter
        return ""


def _build_themes_clause(themes) -> str:
    """
    Build WHERE clause for themes filter.

    Args:
        themes: List of theme IDs

    Returns:
        WHERE clause string for themes, or empty string if invalid
    """
    try:
        ids = ",".join(str(int(t)) for t in themes)
        return f"themes = ({ids})"
    except (ValueError, TypeError):
        return ""


def _build_player_perspectives_clause(player_perspectives) -> str:
    """
    Build WHERE clause for player perspectives filter.

    Args:
        player_perspectives: List of player perspective IDs

    Returns:
        WHERE clause string for player perspectives, or empty string if invalid
    """
    try:
        ids = ",".join(str(int(p)) for p in player_perspectives)
        return f"player_perspectives = ({ids})"
    except (ValueError, TypeError):
        return ""


def _build_release_status_clause(release_status) -> str:
    """
    Build WHERE clause for release status filter.

    Args:
        release_status: List of release status IDs

    Returns:
        WHERE clause string for release status, or empty string if invalid
    """
    try:
        ids = ",".join(str(int(s)) for s in release_status)
        return f"status = ({ids})"
    except (ValueError, TypeError):
        return ""


def _build_franchises_clause(franchises) -> str:
    """
    Build WHERE clause for franchises filter.

    Args:
        franchises: List of franchise IDs

    Returns:
        WHERE clause string for franchises, or empty string if invalid
    """
    try:
        ids = ",".join(str(int(f)) for f in franchises)
        return f"franchises = ({ids})"
    except (ValueError, TypeError):
        return ""


def _build_companies_clause(companies) -> str:
    """
    Build WHERE clause for companies filter.

    Args:
        companies: List of company IDs (developers/publishers)

    Returns:
        WHERE clause string for companies, or empty string if invalid
    """
    try:
        ids = ",".join(str(int(c)) for c in companies)
        # Use involved_companies to catch both developers and publishers
        return f"involved_companies.company = ({ids})"
    except (ValueError, TypeError):
        return ""


def _build_keywords_clause(keywords) -> str:
    """
    Build WHERE clause for keywords filter.

    Args:
        keywords: List of keyword IDs

    Returns:
        WHERE clause string for keywords, or empty string if invalid
    """
    try:
        ids = ",".join(str(int(k)) for k in keywords)
        return f"keywords = ({ids})"
    except (ValueError, TypeError):
        return ""


def _build_multiplayer_modes_clause(multiplayer_modes) -> str:
    """
    Build WHERE clause for multiplayer modes filter.

    Args:
        multiplayer_modes: List of multiplayer mode IDs

    Returns:
        WHERE clause string for multiplayer modes, or empty string if invalid
    """
    try:
        ids = ",".join(str(int(m)) for m in multiplayer_modes)
        return f"multiplayer_modes = ({ids})"
    except (ValueError, TypeError):
        return ""


def _build_rating_range_clause(min_rating, max_rating) -> str:
    """
    Build WHERE clause for IGDB rating range filter.

    Args:
        min_rating: Minimum rating (0-100), optional
        max_rating: Maximum rating (0-100), optional

    Returns:
        WHERE clause string for rating range, or empty string if invalid
    """
    clauses = []
    try:
        if min_rating is not None:
            clauses.append(f"aggregated_rating >= {int(min_rating)}")
        if max_rating is not None:
            clauses.append(f"aggregated_rating <= {int(max_rating)}")
        return " & ".join(clauses) if clauses else ""
    except (ValueError, TypeError):
        return ""


def _build_metacritic_range_clause(min_metacritic, max_metacritic) -> str:
    """
    Build WHERE clause for Metacritic score range filter.

    Args:
        min_metacritic: Minimum Metacritic score (0-100), optional
        max_metacritic: Maximum Metacritic score (0-100), optional

    Returns:
        WHERE clause string for Metacritic range, or empty string if invalid
    """
    clauses = []
    try:
        if min_metacritic is not None:
            clauses.append(f"aggregated_rating >= {int(min_metacritic)}")
        if max_metacritic is not None:
            clauses.append(f"aggregated_rating <= {int(max_metacritic)}")
        return " & ".join(clauses) if clauses else ""
    except (ValueError, TypeError):
        return ""


def _build_esrb_ratings_clause(esrb_ratings) -> str:
    """
    Build WHERE clause for ESRB ratings filter.

    Args:
        esrb_ratings: List of ESRB rating IDs

    Returns:
        WHERE clause string for ESRB ratings, or empty string if invalid
    """
    try:
        ids = ",".join(str(int(r)) for r in esrb_ratings)
        # ESRB ratings are typically stored under age_ratings with specific category
        return f"age_ratings.category = 1 & age_ratings.rating = ({ids})"
    except (ValueError, TypeError):
        return ""


def _build_game_engines_clause(game_engines) -> str:
    """
    Build WHERE clause for game engines filter.

    Args:
        game_engines: List of game engine IDs

    Returns:
        WHERE clause string for game engines, or empty string if invalid
    """
    try:
        ids = ",".join(str(int(e)) for e in game_engines)
        return f"game_engines = ({ids})"
    except (ValueError, TypeError):
        return ""


def _build_collections_clause(collections) -> str:
    """
    Build WHERE clause for collections filter.

    Args:
        collections: List of collection IDs

    Returns:
        WHERE clause string for collections, or empty string if invalid
    """
    try:
        ids = ",".join(str(int(c)) for c in collections)
        return f"collection = ({ids})"
    except (ValueError, TypeError):
        return ""
