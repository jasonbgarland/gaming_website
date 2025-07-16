"""
IGDB API client and related logic for interacting with the IGDB service.
Provides methods for searching, fetching, and mapping game data.
"""

from typing import Any, Dict, List

import httpx


class IGDBClient:
    """
    Client for interacting with the IGDB API.

    Provides methods to search for games, fetch game details, genres, and platforms.
    Handles authentication and response mapping for the gaming microservice.
    """

    def __init__(self, auth, base_url: str = None) -> None:
        """
        Initialize the IGDBClient.

        Args:
            auth: IGDBAuth instance for authentication.
            base_url (str, optional): Override IGDB API base URL.
        """
        self.auth = auth
        self.base_url = base_url or "https://api.igdb.com/v4"

    def _get_games_from_cache(self, game_ids, cache):
        """Return (cached_games, ids_to_fetch) for a list of game_ids."""
        cached = []
        to_fetch = []
        if cache:
            for gid in game_ids:
                game = cache.get(f"game:{gid}")
                if game is not None:
                    cached.append(game)
                else:
                    to_fetch.append(gid)
        else:
            to_fetch = list(game_ids)
        return cached, to_fetch

    def _fetch_games_from_api(self, game_ids):
        """Fetch games from IGDB API and return mapped games."""
        if not game_ids:
            return []
        token = self.auth.get_token()
        headers = {
            "Client-ID": self.auth.client_id,
            "Authorization": f"Bearer {token}",
        }
        ids_str = ",".join(str(i) for i in game_ids)
        fields = (
            "id,name,cover.url,summary,first_release_date,genres.name,platforms.name"
        )
        data = f"where id = ({ids_str}); fields {fields}; limit {len(game_ids)};"
        response = httpx.post(
            f"{self.base_url}/games", headers=headers, data=data, timeout=10
        )
        response.raise_for_status()
        api_results = response.json()
        return [self._map_game(game) for game in api_results]

    def _cache_games(self, games, cache):
        """Cache a list of mapped games by their ID."""
        for game in games:
            cache.set(f"game:{game['id']}", game, ttl=300)

    def get_games_by_ids(self, game_ids: List[int]) -> List[dict]:
        """
        Batch fetch game details by a list of IGDB IDs, using cache for each ID if available.
        """
        if not game_ids:
            return []
        cache = getattr(self, "cache", None)
        cached_games, ids_to_fetch = self._get_games_from_cache(game_ids, cache)
        fetched_games = self._fetch_games_from_api(ids_to_fetch) if ids_to_fetch else []
        if cache and fetched_games:
            self._cache_games(fetched_games, cache)
        # Return results in the same order as requested
        id_to_game = {g["id"]: g for g in cached_games + fetched_games}
        return [id_to_game[gid] for gid in game_ids if gid in id_to_game]

    def get_genres(self) -> List[dict]:
        """
        Fetch all game genres from IGDB, using cache if available.

        Returns:
            List[dict]: List of genre dictionaries with 'id' and 'name'.
        """
        cache = getattr(self, "cache", None)
        cache_key = "genres"
        if cache:
            cached = cache.get(cache_key)
            if cached is not None:
                return cached
        token = self.auth.get_token()
        headers = {
            "Client-ID": self.auth.client_id,
            "Authorization": f"Bearer {token}",
        }
        data = "fields id,name; limit 100;"
        response = httpx.post(
            f"{self.base_url}/genres", headers=headers, data=data, timeout=10
        )
        response.raise_for_status()
        genres = response.json()
        if cache:
            cache.set(cache_key, genres, ttl=86400)  # 24 hours
        return genres

    def get_platforms(self) -> List[dict]:
        """
        Fetch all platforms from IGDB, using cache if available.

        Returns:
            List[dict]: List of platform dictionaries with 'id' and 'name'.
        """
        cache = getattr(self, "cache", None)
        cache_key = "platforms"
        if cache:
            cached = cache.get(cache_key)
            if cached is not None:
                return cached
        token = self.auth.get_token()
        headers = {
            "Client-ID": self.auth.client_id,
            "Authorization": f"Bearer {token}",
        }
        data = "fields id,name; limit 100;"
        response = httpx.post(
            f"{self.base_url}/platforms", headers=headers, data=data, timeout=10
        )
        response.raise_for_status()
        platforms = response.json()
        if cache:
            cache.set(cache_key, platforms, ttl=86400)  # 24 hours
        return platforms

    def get_game_by_id(self, game_id: int) -> dict:
        """
        Get details for a specific game by IGDB ID, using cache if available.
        Includes cover, summary, release date, genres, and platforms.
        """
        cache = getattr(self, "cache", None)
        cached_games, ids_to_fetch = self._get_games_from_cache([game_id], cache)
        if cached_games:
            return cached_games[0]
        fetched_games = self._fetch_games_from_api(ids_to_fetch)
        if not fetched_games:
            raise ValueError(f"Game with id {game_id} not found")
        if cache:
            self._cache_games(fetched_games, cache)
        return fetched_games[0]

    def search_games(self, query: str) -> List[Dict[str, Any]]:
        """
        Search for games using the IGDB API, returning expanded fields. Uses cache if available.

        Args:
            query (str): Search query string.

        Returns:
            List[dict]: List of mapped game data dictionaries.
        """
        cache = getattr(self, "cache", None)
        cache_key = f"search:{query}"
        if cache:
            cached = cache.get(cache_key)
            if cached is not None:
                return cached
        token = self.auth.get_token()
        headers = {
            "Client-ID": self.auth.client_id,
            "Authorization": f"Bearer {token}",
        }
        fields = (
            "id,name,cover.url,summary,first_release_date,genres.name,platforms.name"
        )
        data = f'search "{query}"; fields {fields}; limit 10;'
        response = httpx.post(
            f"{self.base_url}/games", headers=headers, data=data, timeout=10
        )
        response.raise_for_status()
        results = response.json()
        mapped = [self._map_game(game) for game in results]
        if cache:
            cache.set(cache_key, mapped, ttl=300)  # 5 minutes
        return mapped

    def _map_game(self, game: dict) -> dict:
        """
        Map IGDB API game dict to GameOut-compatible dict.

        Args:
            game (dict): Raw IGDB game dictionary.

        Returns:
            dict: Mapped game dictionary for API response.
        """
        return {
            "id": game["id"],
            "name": game.get("name"),
            "cover_url": (
                game.get("cover", {}).get("url") if game.get("cover") else None
            ),
            "summary": game.get("summary"),
            "release_date": game.get("first_release_date"),
            "genres": (
                [g["name"] for g in game.get("genres", []) if "name" in g]
                if game.get("genres")
                else None
            ),
            "platforms": (
                [p["name"] for p in game.get("platforms", []) if "name" in p]
                if game.get("platforms")
                else None
            ),
        }
