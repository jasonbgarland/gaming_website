"""
Unit tests for the IGDBClient class and its methods.

# pylint: disable=duplicate-code
"""

import unittest
from unittest.mock import MagicMock, patch
from src.igdb.client import IGDBClient


# pylint: disable=too-few-public-methods
class MockAuth:
    """Mock authentication class for IGDBClient tests."""

    def __init__(self):
        self.client_id = "mocked_client_id"

    def get_token(self):
        """Return a mocked token string for authentication."""
        return "mocked_token"


class TestIGDBClient(unittest.TestCase):
    """Unit tests for IGDBClient methods using mocked HTTP responses."""

    @patch("src.igdb.client.httpx.post")
    def test_search_games_returns_results(self, mock_post):
        """
        Test IGDBClient.search_games returns a list of games for a valid query.
        This test mocks the HTTPX post call to simulate IGDB API response.
        """
        # Arrange
        mock_auth = MockAuth()
        client = IGDBClient(auth=mock_auth)
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = [
            {"id": 1, "name": "The Legend of Zelda"},
            {"id": 2, "name": "Super Mario Bros."},
        ]
        mock_post.return_value = mock_response

        # Act
        results = client.search_games("zelda")

        # Assert
        self.assertIsInstance(results, list)
        self.assertEqual(2, len(results))
        self.assertEqual("The Legend of Zelda", results[0]["name"])


if __name__ == "__main__":
    unittest.main()
