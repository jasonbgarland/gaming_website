"""
Unit tests for the IGDB API endpoints and client logic.
"""

# pylint: disable=too-few-public-methods, broad-exception-raised
import unittest
from fastapi.testclient import TestClient
from src.main import app
from src.api.igdb import get_igdb_client


# --- Mock Clients ---
class MockIGDBClient:
    """Mock implementation of the IGDBClient for testing API endpoints."""

    def get_games_by_ids(self, game_ids):
        """Mock batch fetch of games by IDs."""
        if not game_ids:
            return []
        if 500 in game_ids:
            raise Exception(
                "Mock batch error"
            )  # pylint: disable=broad-exception-raised
        return [
            {
                "id": i,
                "name": f"Mock Game {i}",
                "cover_url": f"https://mock.url/cover{i}.jpg",
                "summary": f"A mock summary {i}.",
                "release_date": 1111111111 + i,
                "genres": ["RPG"],
                "platforms": ["PlayStation"],
            }
            for i in game_ids
        ]

    def get_genres(self):
        """Mock fetch of genres."""
        return [{"id": 1, "name": "Action"}, {"id": 2, "name": "Adventure"}]

    # pylint: disable=broad-exception-raised

    # --- All API methods needed for all test classes ---
    def get_platforms(self):
        """Mock fetch of platforms."""
        return [{"id": 1, "name": "PC"}, {"id": 2, "name": "Switch"}]

    # pylint: disable=broad-exception-raised

    def search_games(self, query):
        """Mock search for games by query string."""
        if query == "empty":
            return []
        if query == "error":
            raise Exception(
                "Mock search error"
            )  # pylint: disable=broad-exception-raised
        return [
            {
                "id": 1,
                "name": "Mock Game 1",
                "cover_url": "https://mock.url/cover1.jpg",
                "summary": "A mock summary 1.",
                "release_date": 1234567890,
                "genres": ["Adventure", "Action"],
                "platforms": ["PC", "Switch"],
            },
            {
                "id": 2,
                "name": "Mock Game 2",
                "cover_url": "https://mock.url/cover2.jpg",
                "summary": "A mock summary 2.",
                "release_date": 987654321,
                "genres": ["Puzzle"],
                "platforms": ["Xbox"],
            },
        ]

    def get_game_by_id(self, game_id):
        """Mock fetch of a single game by ID."""
        if game_id == 404:
            raise ValueError("Game not found")
        if game_id == 500:
            raise Exception("Mock get error")  # pylint: disable=broad-exception-raised
        return {
            "id": game_id,
            "name": f"Mock Game {game_id}",
            "cover_url": f"https://mock.url/cover{game_id}.jpg",
            "summary": f"A mock summary {game_id}.",
            "release_date": 1111111111,
            "genres": ["RPG"],
            "platforms": ["PlayStation"],
        }


# pylint: disable=too-few-public-methods
class BaseIGDBApiTest(unittest.TestCase):
    """Base test class for IGDB API tests with shared setup/teardown."""

    def setUp(self):
        """Set up the test client and override dependencies."""
        app.dependency_overrides[get_igdb_client] = MockIGDBClient
        self.client = TestClient(app)

    def tearDown(self):
        """Reset dependency overrides after each test."""
        app.dependency_overrides = {}

    @staticmethod
    def assert_game_dict_structure(testcase, game):
        """Assert that a game dict has all required keys."""
        testcase.assertIn("id", game)
        testcase.assertIn("name", game)
        testcase.assertIn("cover_url", game)
        testcase.assertIn("summary", game)
        testcase.assertIn("release_date", game)
        testcase.assertIn("genres", game)
        testcase.assertIn("platforms", game)


# --- /igdb/games batch, genres, and platforms route tests ---
class TestIGDBBatchGenresPlatformsApi(BaseIGDBApiTest):
    """Unit tests for /igdb/games batch, genres, and platforms endpoints."""

    def test_batch_games_invalid_ids(self):
        """Test /igdb/games with invalid IDs returns only valid results."""
        # Non-integer and negative IDs should be ignored or handled gracefully
        response = self.client.get("/igdb/games?ids=abc,-1,0,2")
        self.assertEqual(200, response.status_code)
        data = response.json()
        # Only '2' is valid and positive
        self.assertEqual(1, len(data))
        self.assertEqual(2, data[0]["id"])

    def test_batch_games_all_invalid(self):
        """Test /igdb/games with all invalid IDs returns empty list."""
        response = self.client.get("/igdb/games?ids=abc,-1,0")
        self.assertEqual(200, response.status_code)
        data = response.json()
        self.assertEqual([], data)

    def test_batch_games_duplicates(self):
        """Test /igdb/games with duplicate IDs returns duplicates in response."""
        response = self.client.get("/igdb/games?ids=2,2,2")
        self.assertEqual(200, response.status_code)
        data = response.json()
        # Should return three results for three valid IDs (duplicates allowed)
        self.assertEqual(3, len(data))
        for game in data:
            self.assertEqual(2, game["id"])

    def test_batch_games_large_list(self):
        """Test /igdb/games with a large list of IDs returns all results."""
        ids = ",".join(str(i) for i in range(1, 51))
        response = self.client.get(f"/igdb/games?ids={ids}")
        self.assertEqual(200, response.status_code)
        data = response.json()
        self.assertEqual(50, len(data))

    def test_genres_empty(self):
        """Test /igdb/genres returns empty list when client returns none."""
        # Patch the client to return empty list
        original = MockIGDBClient.get_genres
        MockIGDBClient.get_genres = lambda self: []
        response = self.client.get("/igdb/genres")
        self.assertEqual(200, response.status_code)
        data = response.json()
        self.assertEqual([], data)
        MockIGDBClient.get_genres = original

    def test_genres_client_error(self):
        """Test /igdb/genres returns 500 on client error."""
        original = MockIGDBClient.get_genres
        # pylint: disable=broad-exception-raised
        MockIGDBClient.get_genres = lambda self: (_ for _ in ()).throw(
            Exception("Mock error")  # pylint: disable=broad-exception-raised
        )
        response = self.client.get("/igdb/genres")
        self.assertEqual(500, response.status_code)
        data = response.json()
        self.assertIn("detail", data)
        MockIGDBClient.get_genres = original

    def test_platforms_empty(self):
        """Test /igdb/platforms returns empty list when client returns none."""
        original = MockIGDBClient.get_platforms
        MockIGDBClient.get_platforms = lambda self: []
        response = self.client.get("/igdb/platforms")
        self.assertEqual(200, response.status_code)
        data = response.json()
        self.assertEqual([], data)
        MockIGDBClient.get_platforms = original

    def test_platforms_client_error(self):
        """Test /igdb/platforms returns 500 on client error."""
        original = MockIGDBClient.get_platforms
        # pylint: disable=broad-exception-raised
        MockIGDBClient.get_platforms = lambda self: (_ for _ in ()).throw(
            Exception("Mock error")  # pylint: disable=broad-exception-raised
        )
        response = self.client.get("/igdb/platforms")
        self.assertEqual(500, response.status_code)
        data = response.json()
        self.assertIn("detail", data)
        MockIGDBClient.get_platforms = original

    def test_batch_games_success(self):
        """Test /igdb/games returns correct data for valid IDs."""
        response = self.client.get("/igdb/games?ids=1,2,3")
        self.assertEqual(200, response.status_code)
        data = response.json()
        self.assertIsInstance(data, list)
        self.assertEqual(3, len(data))
        for i, game in enumerate(data, 1):
            self.assertEqual(i, game["id"])
            self.assertEqual(f"Mock Game {i}", game["name"])
            self.assert_game_dict_structure(self, game)

    def test_batch_games_empty(self):
        """Test /igdb/games with empty IDs returns an empty list."""
        response = self.client.get("/igdb/games?ids=")
        self.assertEqual(200, response.status_code)
        data = response.json()
        self.assertEqual([], data)

    def test_batch_games_client_error(self):
        """Test /igdb/games returns 500 if client raises an error."""
        response = self.client.get("/igdb/games?ids=1,500,3")
        self.assertEqual(500, response.status_code)
        data = response.json()
        self.assertIn("detail", data)

    def test_genres_success(self):
        """Test /igdb/genres returns a list of genres."""
        response = self.client.get("/igdb/genres")
        self.assertEqual(200, response.status_code)
        data = response.json()
        self.assertIsInstance(data, list)
        self.assertEqual(2, len(data))
        self.assertEqual({"id": 1, "name": "Action"}, data[0])

    def test_platforms_success(self):
        """Test /igdb/platforms returns a list of platforms."""
        response = self.client.get("/igdb/platforms")
        self.assertEqual(200, response.status_code)
        data = response.json()
        self.assertIsInstance(data, list)
        self.assertEqual(2, len(data))
        self.assertEqual({"id": 1, "name": "PC"}, data[0])


# --- /igdb/search route tests ---


class TestIGDBSearchApi(BaseIGDBApiTest):
    """Unit tests for /igdb/search endpoint."""

    def test_search_success(self):
        """Test /igdb/search returns a list of games for a valid query."""
        response = self.client.get("/igdb/search?q=zelda")
        self.assertEqual(200, response.status_code)
        data = response.json()
        self.assertIsInstance(data, list)
        self.assertEqual(2, len(data))
        for game in data:
            self.assert_game_dict_structure(self, game)

    def test_search_empty_results(self):
        """Test /igdb/search returns an empty list for a query with no results."""
        response = self.client.get("/igdb/search?q=empty")
        self.assertEqual(200, response.status_code)
        data = response.json()
        self.assertIsInstance(data, list)
        self.assertEqual(0, len(data))
        # If any game is returned, check structure
        for game in data:
            self.assert_game_dict_structure(self, game)

    def test_search_query_too_short(self):
        """Test /igdb/search returns 422 for a too-short query string."""
        response = self.client.get("/igdb/search?q=")
        self.assertEqual(422, response.status_code)

    def test_search_missing_query(self):
        """Test /igdb/search returns 422 if the query parameter is missing."""
        response = self.client.get("/igdb/search")
        self.assertEqual(422, response.status_code)

    def test_search_client_error(self):
        """Test /igdb/search returns 500 if the client raises an error."""
        response = self.client.get("/igdb/search?q=error")
        self.assertEqual(500, response.status_code)


# --- /igdb/games/{id} route tests ---
class TestIGDBGetGameApi(BaseIGDBApiTest):
    """Unit tests for /igdb/games/{id} endpoint and related search edge cases."""

    def test_get_game_negative_id(self):
        """Test /igdb/games/{id} with negative ID returns 422."""
        response = self.client.get("/igdb/games/-1")
        self.assertEqual(422, response.status_code)

    def test_search_special_characters(self):
        """Test /igdb/search with special characters in query returns valid response."""
        response = self.client.get("/igdb/search?q=%23%24%25%5E%26*")  # #$%^&*
        self.assertEqual(200, response.status_code)
        data = response.json()
        self.assertIsInstance(data, list)

    def test_search_very_long_query(self):
        """Test /igdb/search with a very long query string returns valid response."""
        long_query = "a" * 1000
        response = self.client.get(f"/igdb/search?q={long_query}")
        self.assertEqual(200, response.status_code)
        data = response.json()
        self.assertIsInstance(data, list)

    def test_search_whitespace_query(self):
        """Test /igdb/search with whitespace query returns 422."""
        response = self.client.get("/igdb/search?q=   ")
        self.assertEqual(422, response.status_code)

    def test_content_type_json(self):
        """Test /igdb/search returns JSON content type."""
        response = self.client.get("/igdb/search?q=zelda")
        self.assertEqual(
            "application/json", response.headers["content-type"].split(";")[0]
        )

    def test_get_game_success(self):
        """Test /igdb/games/{id} returns correct game data for valid ID."""
        response = self.client.get("/igdb/games/42")
        self.assertEqual(200, response.status_code)
        data = response.json()
        self.assertIsInstance(data, dict)
        self.assertEqual(42, data["id"])
        self.assertEqual("Mock Game 42", data["name"])
        self.assertEqual("https://mock.url/cover42.jpg", data["cover_url"])
        self.assertEqual("A mock summary 42.", data["summary"])
        self.assertEqual(1111111111, data["release_date"])
        self.assertEqual(["RPG"], data["genres"])
        self.assertEqual(["PlayStation"], data["platforms"])

    def test_get_game_not_found(self):
        """Test /igdb/games/{id} with non-existent ID returns 404."""
        response = self.client.get("/igdb/games/404")
        self.assertEqual(404, response.status_code)
        data = response.json()
        self.assertIn("detail", data)
        self.assertIn("not found", data["detail"])

    def test_get_game_invalid_id(self):
        """Test /igdb/games/{id} with invalid (non-integer) ID returns 422."""
        response = self.client.get("/igdb/games/notanint")
        self.assertEqual(422, response.status_code)

    def test_get_game_client_error(self):
        """Test /igdb/games/{id} with client error returns 500."""
        response = self.client.get("/igdb/games/500")
        self.assertEqual(500, response.status_code)
        data = response.json()
        self.assertIn("detail", data)


if __name__ == "__main__":
    unittest.main()
