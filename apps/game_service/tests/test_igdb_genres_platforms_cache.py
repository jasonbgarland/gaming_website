"""
Unit tests for IGDBClient caching of genres and platforms.

"""

# pylint: disable=duplicate-code
import unittest
from unittest.mock import MagicMock, patch
from src.igdb.client import IGDBClient
from src.igdb.cache import InMemoryCache


class TestIGDBClientGenresPlatformsCaching(unittest.TestCase):
    """Unit tests for IGDBClient caching of genres and platforms."""

    def setUp(self):
        """Set up a mock IGDBClient with in-memory cache for each test."""
        self.mock_auth = MagicMock()
        self.mock_auth.get_token.return_value = "fake-token"
        self.mock_auth.client_id = "fake-client-id"
        self.cache = InMemoryCache()
        self.client = IGDBClient(auth=self.mock_auth, base_url="http://fake-igdb.com")
        self.client.cache = self.cache

    @patch("httpx.post")
    def test_get_genres_caches_result(self, mock_post):
        """Test that get_genres caches the result after the first API call."""

        # pylint: disable=missing-class-docstring,missing-function-docstring
        class FakeResponse:
            def raise_for_status(self):
                pass

            def json(self):
                return [{"id": 1, "name": "Action"}]

        mock_post.return_value = FakeResponse()

        # First call: should hit API and cache result
        result1 = self.client.get_genres()
        self.assertEqual(result1[0]["name"], "Action")

        # Second call: should hit cache, not API
        mock_post.side_effect = Exception("Should not call API again")
        result2 = self.client.get_genres()
        self.assertEqual(result2[0]["name"], "Action")

    @patch("httpx.post")
    def test_get_platforms_caches_result(self, mock_post):
        """Test that get_platforms caches the result after the first API call."""

        # pylint: disable=missing-class-docstring,missing-function-docstring
        class FakeResponse:
            def raise_for_status(self):
                pass

            def json(self):
                return [{"id": 2, "name": "PC"}]

        mock_post.return_value = FakeResponse()

        # First call: should hit API and cache result
        result1 = self.client.get_platforms()
        self.assertEqual(result1[0]["name"], "PC")

        # Second call: should hit cache, not API
        mock_post.side_effect = Exception("Should not call API again")
        result2 = self.client.get_platforms()
        self.assertEqual(result2[0]["name"], "PC")


if __name__ == "__main__":
    unittest.main()
