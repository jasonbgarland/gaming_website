"""
Unit tests for IGDBClient caching of search_games and get_games_by_ids.
"""

# pylint: disable=duplicate-code

import unittest
from unittest.mock import MagicMock, patch
from src.igdb.client import IGDBClient
from src.igdb.cache import InMemoryCache


class TestIGDBClientSearchAndBatchCaching(unittest.TestCase):
    """Test that IGDBClient uses cache for search_games and get_games_by_ids."""

    def setUp(self):
        self.mock_auth = MagicMock()
        self.mock_auth.get_token.return_value = "fake-token"
        self.mock_auth.client_id = "fake-client-id"
        self.cache = InMemoryCache()
        self.client = IGDBClient(auth=self.mock_auth, base_url="http://fake-igdb.com")
        self.client.cache = self.cache

    @patch("httpx.post")
    def test_search_games_caches_result(self, mock_post):
        """Test that search_games caches the result after the first API call."""

        # pylint: disable=missing-class-docstring,missing-function-docstring
        class FakeResponse:
            def raise_for_status(self):
                pass

            def json(self):
                return [{"id": 1, "name": "Game A"}, {"id": 2, "name": "Game B"}]

        mock_post.return_value = FakeResponse()

        # First call: should hit API and cache result
        result1 = self.client.search_games("zelda")
        self.assertEqual(result1[0]["name"], "Game A")

        # Second call: should hit cache, not API
        mock_post.side_effect = Exception("Should not call API again")
        result2 = self.client.search_games("zelda")
        self.assertEqual(result2[0]["name"], "Game A")

    @patch("httpx.post")
    def test_get_games_by_ids_caches_each_game(self, mock_post):
        """Test that get_games_by_ids caches each game and uses cache for subsequent calls."""

        # pylint: disable=missing-class-docstring,missing-function-docstring
        class FakeResponse:
            def raise_for_status(self):
                pass

            def json(self):
                return [{"id": 10, "name": "Game X"}, {"id": 20, "name": "Game Y"}]

        mock_post.return_value = FakeResponse()

        # First call: should hit API and cache both
        result1 = self.client.get_games_by_ids([10, 20])
        self.assertEqual(result1[0]["name"], "Game X")
        self.assertEqual(result1[1]["name"], "Game Y")

        # Second call: should hit cache for both, not API
        mock_post.side_effect = Exception("Should not call API again")
        result2 = self.client.get_games_by_ids([10, 20])
        self.assertEqual(result2[0]["name"], "Game X")
        self.assertEqual(result2[1]["name"], "Game Y")

        # Third call: one cached, one new
        mock_post.side_effect = None

        class FakeResponse2:
            def raise_for_status(self):
                pass

            def json(self):
                return [{"id": 30, "name": "Game Z"}]

        mock_post.return_value = FakeResponse2()
        result3 = self.client.get_games_by_ids([10, 30])
        self.assertEqual(result3[0]["name"], "Game X")  # from cache
        self.assertEqual(result3[1]["name"], "Game Z")  # from API


if __name__ == "__main__":
    unittest.main()
