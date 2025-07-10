"""
Additional unit tests for IGDBClient and InMemoryCache edge cases and robustness.
"""

# pylint: disable=duplicate-code
import unittest
import time
from unittest.mock import MagicMock, patch
import httpx
from src.igdb.client import IGDBClient
from src.igdb.cache import InMemoryCache


class TestInMemoryCacheExpiry(unittest.TestCase):
    """Test cache expiry (TTL) behavior."""

    def setUp(self):
        """Set up a new cache instance before each test."""
        self.cache = InMemoryCache()

    def test_cache_expiry(self):
        """Test that cache entries expire after TTL."""
        self.cache.set("foo", "bar", ttl=1)
        self.assertEqual(self.cache.get("foo"), "bar")
        time.sleep(1.1)
        self.assertIsNone(self.cache.get("foo"))


class TestIGDBClientCacheMiss(unittest.TestCase):
    """Test cache miss and fallback to API."""

    def setUp(self):
        """Set up IGDBClient with in-memory cache."""
        self.mock_auth = MagicMock()
        self.mock_auth.get_token.return_value = "fake-token"
        self.mock_auth.client_id = "fake-client-id"
        self.cache = InMemoryCache()
        self.client = IGDBClient(auth=self.mock_auth, base_url="http://fake-igdb.com")
        self.client.cache = self.cache

    @patch("httpx.post")
    def test_search_games_cache_miss(self, mock_post):
        """Test that a cache miss triggers an API call."""

        # pylint: disable=missing-class-docstring,missing-function-docstring
        class FakeResponse:
            def raise_for_status(self):
                pass

            def json(self):
                return [{"id": 1, "name": "Game A"}]

        mock_post.return_value = FakeResponse()
        # No cache set, should call API
        result = self.client.search_games("mario")
        self.assertEqual(result[0]["name"], "Game A")


class TestIGDBClientErrorHandling(unittest.TestCase):
    """Test that API errors are not cached and are handled properly."""

    def setUp(self):
        """Set up IGDBClient with in-memory cache."""
        self.mock_auth = MagicMock()
        self.mock_auth.get_token.return_value = "fake-token"
        self.mock_auth.client_id = "fake-client-id"
        self.cache = InMemoryCache()
        self.client = IGDBClient(auth=self.mock_auth, base_url="http://fake-igdb.com")
        self.client.cache = self.cache

    @patch("httpx.post")
    def test_search_games_api_error_not_cached(self, mock_post):
        """Test that API errors are not cached."""
        mock_post.side_effect = httpx.HTTPStatusError(
            "error", request=None, response=None
        )
        with self.assertRaises(httpx.HTTPStatusError):
            self.client.search_games("fail")
        self.assertIsNone(self.cache.get("search:fail"))


class TestIGDBClientCacheIsolation(unittest.TestCase):
    """Test that different queries/IDs do not overwrite each other in the cache."""

    def setUp(self):
        """Set up IGDBClient with in-memory cache."""
        self.mock_auth = MagicMock()
        self.mock_auth.get_token.return_value = "fake-token"
        self.mock_auth.client_id = "fake-client-id"
        self.cache = InMemoryCache()
        self.client = IGDBClient(auth=self.mock_auth, base_url="http://fake-igdb.com")
        self.client.cache = self.cache

    @patch("httpx.post")
    def test_search_games_cache_isolation(self, mock_post):
        """Test that different queries are cached separately."""

        # pylint: disable=missing-class-docstring,missing-function-docstring
        class MarioResponse:
            def raise_for_status(self):
                pass

            def json(self):
                return [{"id": 1, "name": "Mario"}]

        class ZeldaResponse:
            def raise_for_status(self):
                pass

            def json(self):
                return [{"id": 2, "name": "Zelda"}]

        mock_post.return_value = MarioResponse()
        self.client.search_games("mario")
        mock_post.return_value = ZeldaResponse()
        self.client.search_games("zelda")
        self.assertNotEqual(
            self.cache.get("search:mario"), self.cache.get("search:zelda")
        )


class TestIGDBClientCacheConsistency(unittest.TestCase):
    """Test that after updating the cache, the next call returns the cached value."""

    def setUp(self):
        """Set up IGDBClient with in-memory cache."""
        self.mock_auth = MagicMock()
        self.mock_auth.get_token.return_value = "fake-token"
        self.mock_auth.client_id = "fake-client-id"
        self.cache = InMemoryCache()
        self.client = IGDBClient(auth=self.mock_auth, base_url="http://fake-igdb.com")
        self.client.cache = self.cache

    @patch("httpx.post")
    def test_search_games_cache_consistency(self, mock_post):
        """Test that cache updates are reflected in subsequent calls."""

        # pylint: disable=missing-class-docstring,missing-function-docstring
        class FakeResponse:
            def raise_for_status(self):
                pass

            def json(self):
                return [{"id": 1, "name": "Game A"}]

        mock_post.return_value = FakeResponse()
        result1 = self.client.search_games("mario")
        self.assertEqual(result1[0]["name"], "Game A")
        # Now, forcibly change the cache
        self.cache.set("search:mario", [{"id": 1, "name": "Game B"}], ttl=5)
        result2 = self.client.search_games("mario")
        self.assertEqual(result2[0]["name"], "Game B")


class TestIGDBClientEdgeCases(unittest.TestCase):
    """Test edge cases like empty input."""

    def setUp(self):
        """Set up IGDBClient with in-memory cache."""
        self.mock_auth = MagicMock()
        self.mock_auth.get_token.return_value = "fake-token"
        self.mock_auth.client_id = "fake-client-id"
        self.cache = InMemoryCache()
        self.client = IGDBClient(auth=self.mock_auth, base_url="http://fake-igdb.com")
        self.client.cache = self.cache

    @patch("httpx.post")
    def test_get_games_by_ids_empty(self, mock_post):
        """Test that empty input returns an empty list and does not call API."""
        result = self.client.get_games_by_ids([])
        self.assertEqual(result, [])
        mock_post.assert_not_called()

    @patch("httpx.post")
    def test_search_games_empty_query(self, mock_post):
        """Test that empty search query returns empty if API does."""

        # pylint: disable=missing-class-docstring,missing-function-docstring
        class FakeResponse:
            def raise_for_status(self):
                pass

            def json(self):
                return []

        mock_post.return_value = FakeResponse()
        result = self.client.search_games("")
        self.assertEqual(result, [])


if __name__ == "__main__":
    unittest.main()
