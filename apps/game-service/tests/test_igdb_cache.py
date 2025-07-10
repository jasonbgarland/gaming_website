"""
Unit tests for IGDBClient caching behavior.
"""

# pylint: disable=duplicate-code
import unittest
from unittest.mock import MagicMock, patch
from src.igdb.client import IGDBClient
from src.igdb.cache import InMemoryCache


class TestIGDBClientCaching(unittest.TestCase):
    """Test that IGDBClient uses cache for get_game_by_id."""

    def setUp(self):
        self.mock_auth = MagicMock()
        self.mock_auth.get_token.return_value = "fake-token"
        self.mock_auth.client_id = "fake-client-id"
        self.cache = InMemoryCache()
        self.client = IGDBClient(auth=self.mock_auth, base_url="http://fake-igdb.com")
        self.client.cache = self.cache  # We'll inject this attribute for testing

    @patch("httpx.post")
    def test_get_game_by_id_caches_result(self, mock_post):
        """Test that get_game_by_id caches the result after the first API call."""

        # pylint: disable=missing-class-docstring,missing-function-docstring
        class FakeResponse:
            def raise_for_status(self):
                pass

            def json(self):
                return [{"id": 42, "name": "Test Game"}]

        mock_post.return_value = FakeResponse()

        # First call: should hit API and cache result
        result1 = self.client.get_game_by_id(42)
        self.assertEqual(result1["id"], 42)

        # Second call: should hit cache, not API
        mock_post.side_effect = Exception("Should not call API again")
        result2 = self.client.get_game_by_id(42)
        self.assertEqual(result2["id"], 42)


if __name__ == "__main__":
    unittest.main()
