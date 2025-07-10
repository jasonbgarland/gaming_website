"""
IGDB OAuth authentication logic for token retrieval and refresh.
Handles caching and automatic refresh of the IGDB API access token.
"""

import os
import time
import httpx
from dotenv import load_dotenv

load_dotenv()


class IGDBAuth:
    """
    Handles IGDB OAuth token retrieval and refresh.
    Caches the token in memory and refreshes when expired.
    """

    def __init__(self) -> None:
        self.client_id = os.getenv("IGDB_CLIENT_ID")
        self.client_secret = os.getenv("IGDB_CLIENT_SECRET")
        self.token_url = "https://id.twitch.tv/oauth2/token"
        self._access_token = None
        self._expires_at = 0

    def get_token(self) -> str:
        """Returns a valid access token, refreshing if needed."""
        if not self._access_token or time.time() >= self._expires_at:
            self._fetch_token()
        return self._access_token

    def _fetch_token(self) -> None:
        """Fetches a new token from Twitch/IGDB and updates cache."""
        data = {
            "client_id": self.client_id,
            "client_secret": self.client_secret,
            "grant_type": "client_credentials",
        }
        response = httpx.post(self.token_url, data=data, timeout=10)
        response.raise_for_status()
        token_data = response.json()
        self._access_token = token_data["access_token"]
        self._expires_at = (
            time.time() + token_data["expires_in"] - 60
        )  # buffer before expiry

    def clear_token(self) -> None:
        """Clears the cached token (for testing or force refresh)."""
        self._access_token = None
        self._expires_at = 0
