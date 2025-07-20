"""
Unit tests for the IGDBClient class and its methods.

# pylint: disable=duplicate-code
"""

import unittest
from unittest.mock import MagicMock, patch

from src.igdb.auth import IGDBAuth
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

    # We need to reset the IGDBAuth singleton before each test
    def setUp(self):
        IGDBAuth._instance = None  # pylint: disable=protected-access

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

    @patch("src.igdb.auth.httpx.post")
    def test_igdb_auth_token_is_cached(self, mock_post):
        """
        Test that IGDBAuth only fetches a new token once and caches it for subsequent calls.
        """
        # mock token response
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "access_token": "token123",
            "expires_in": 3600,
        }
        mock_post.return_value = mock_response

        auth = IGDBAuth()
        auth.clear_token()  # Ensure clean state

        # Call get_token() multiple times
        token1 = auth.get_token()
        token2 = auth.get_token()

        # httpx.post called only once (token is cached)
        self.assertEqual(token1, "token123")
        self.assertEqual(token2, "token123")
        self.assertEqual(mock_post.call_count, 1)

        # Clear token and call again
        auth.clear_token()
        token3 = auth.get_token()

        # httpx.post called again for new token
        self.assertEqual(token3, "token123")
        self.assertEqual(mock_post.call_count, 2)

    @patch("src.igdb.auth.httpx.post")
    @patch("src.igdb.auth.time.time")
    def test_igdb_auth_token_expires_and_refreshes(self, mock_time, mock_post):
        """
        Test that IGDBAuth fetches a new token after the previous one expires.
        """
        # mock token response with longer expiry to account for 60s buffer
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "access_token": "tokenABC",
            "expires_in": 120,
        }  # 2 minutes
        mock_post.return_value = mock_response

        # Simulate time before creating auth instance
        t0 = 1000000
        mock_time.return_value = t0

        auth = IGDBAuth()
        # Verify initial state - should have no token
        # pylint: disable=protected-access
        self.assertIsNone(auth._access_token)
        self.assertEqual(auth._expires_at, 0)
        # pylint: enable=protected-access

        # Get token (should fetch new)
        token1 = auth.get_token()
        self.assertEqual(token1, "tokenABC")
        self.assertEqual(mock_post.call_count, 1)

        # Get token again before expiry (should use cache)
        mock_time.return_value = t0 + 1  # 1 second later
        token2 = auth.get_token()
        self.assertEqual(token2, "tokenABC")
        self.assertEqual(mock_post.call_count, 1)

        # Get token after expiry (should fetch new)
        mock_response2 = MagicMock()
        mock_response2.status_code = 200
        mock_response2.json.return_value = {
            "access_token": "tokenXYZ",
            "expires_in": 120,
        }
        mock_post.return_value = mock_response2
        mock_time.return_value = (
            t0 + 121
        )  # 121 seconds later, past expiry (120 - 60 buffer = 60s effective)
        token3 = auth.get_token()
        self.assertEqual(token3, "tokenXYZ")
        self.assertEqual(mock_post.call_count, 2)


if __name__ == "__main__":
    unittest.main()
