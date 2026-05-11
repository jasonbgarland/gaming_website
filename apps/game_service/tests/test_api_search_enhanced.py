"""
Unit tests for the /igdb/search-enhanced API endpoint.
Tests parameter parsing, filter construction, validation, and error handling.
"""

# pylint: disable=too-few-public-methods, broad-exception-raised
import unittest
from unittest.mock import patch
from fastapi.testclient import TestClient
from src.main import app
from src.api.igdb import get_igdb_client


class MockIGDBClientEnhanced:
    """Mock implementation of IGDBClient with search_games_enhanced support."""

    def search_games_enhanced(self, query, filters=None):
        """Mock enhanced search returning filtered results."""
        if query == "empty":
            return []
        if query == "error":
            raise Exception("Mock enhanced search error")
        # Return a base set of results; tests can inspect filters arg
        results = [
            {
                "id": 1,
                "name": "Mock Enhanced Game 1",
                "cover_url": "https://mock.url/cover1.jpg",
                "summary": "An enhanced mock summary 1.",
                "release_date": 1577836800,  # 2020-01-01
                "genres": ["Action", "Shooter"],
                "platforms": ["PC", "PlayStation 4"],
            },
            {
                "id": 2,
                "name": "Mock Enhanced Game 2",
                "cover_url": "https://mock.url/cover2.jpg",
                "summary": "An enhanced mock summary 2.",
                "release_date": 1609459200,  # 2021-01-01
                "genres": ["RPG"],
                "platforms": ["PlayStation 5", "Xbox Series X"],
            },
        ]
        return results


# Use the base mock for standard endpoints + enhanced
class MockIGDBClient(MockIGDBClientEnhanced):
    """Full mock with both standard and enhanced search methods."""

    def get_games_by_ids(self, game_ids):
        if not game_ids:
            return []
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
        return [{"id": 1, "name": "Action"}, {"id": 2, "name": "Adventure"}]

    def get_platforms(self):
        return [{"id": 1, "name": "PC"}, {"id": 2, "name": "Switch"}]

    def search_games(self, query):
        if query == "empty":
            return []
        if query == "error":
            raise Exception("Mock search error")
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
        ]

    def get_game_by_id(self, game_id):
        if game_id == 404:
            raise ValueError("Game not found")
        return {
            "id": game_id,
            "name": f"Mock Game {game_id}",
            "cover_url": f"https://mock.url/cover{game_id}.jpg",
            "summary": f"A mock summary {game_id}.",
            "release_date": 1111111111,
            "genres": ["RPG"],
            "platforms": ["PlayStation"],
        }


class BaseEnhancedSearchApiTest(unittest.TestCase):
    """Base test class for enhanced search API tests."""

    def setUp(self):
        app.dependency_overrides[get_igdb_client] = MockIGDBClient
        self.client = TestClient(app)

    def tearDown(self):
        app.dependency_overrides = {}


class TestEnhancedSearchSuccess(BaseEnhancedSearchApiTest):
    """Tests for successful /igdb/search-enhanced requests."""

    def test_basic_search_no_filters(self):
        """Test enhanced search with just a query returns results."""
        response = self.client.get("/igdb/search-enhanced?q=halo")
        self.assertEqual(200, response.status_code)
        data = response.json()
        self.assertIsInstance(data, list)
        self.assertEqual(2, len(data))

    def test_search_with_platform_filter(self):
        """Test enhanced search with platform filter returns results."""
        response = self.client.get("/igdb/search-enhanced?q=halo&platforms=6,48")
        self.assertEqual(200, response.status_code)
        data = response.json()
        self.assertIsInstance(data, list)

    def test_search_with_single_platform(self):
        """Test enhanced search with a single platform ID."""
        response = self.client.get("/igdb/search-enhanced?q=zelda&platforms=130")
        self.assertEqual(200, response.status_code)
        data = response.json()
        self.assertIsInstance(data, list)

    def test_search_with_year_filter(self):
        """Test enhanced search with discrete year filter."""
        response = self.client.get("/igdb/search-enhanced?q=halo&years=2020,2021")
        self.assertEqual(200, response.status_code)
        data = response.json()
        self.assertIsInstance(data, list)

    def test_search_with_single_year(self):
        """Test enhanced search with a single year."""
        response = self.client.get("/igdb/search-enhanced?q=halo&years=2023")
        self.assertEqual(200, response.status_code)
        data = response.json()
        self.assertIsInstance(data, list)

    def test_search_with_year_range(self):
        """Test enhanced search with year_start and year_end range filter."""
        response = self.client.get(
            "/igdb/search-enhanced?q=halo&year_start=2018&year_end=2022"
        )
        self.assertEqual(200, response.status_code)
        data = response.json()
        self.assertIsInstance(data, list)

    def test_search_with_genre_filter(self):
        """Test enhanced search with genre filter."""
        response = self.client.get("/igdb/search-enhanced?q=halo&genres=4,12")
        self.assertEqual(200, response.status_code)
        data = response.json()
        self.assertIsInstance(data, list)

    def test_search_with_min_rating(self):
        """Test enhanced search with minimum rating filter."""
        response = self.client.get("/igdb/search-enhanced?q=halo&min_rating=80")
        self.assertEqual(200, response.status_code)
        data = self.json() if hasattr(self, "json") else response.json()
        self.assertIsInstance(data, list)

    def test_search_with_max_rating(self):
        """Test enhanced search with maximum rating filter."""
        response = self.client.get("/igdb/search-enhanced?q=halo&max_rating=90")
        self.assertEqual(200, response.status_code)
        data = response.json()
        self.assertIsInstance(data, list)

    def test_search_with_rating_range(self):
        """Test enhanced search with both min and max rating."""
        response = self.client.get(
            "/igdb/search-enhanced?q=halo&min_rating=70&max_rating=90"
        )
        self.assertEqual(200, response.status_code)
        data = response.json()
        self.assertIsInstance(data, list)

    def test_search_with_theme_filter(self):
        """Test enhanced search with theme filter."""
        response = self.client.get("/igdb/search-enhanced?q=horror&themes=19,18")
        self.assertEqual(200, response.status_code)
        data = response.json()
        self.assertIsInstance(data, list)

    def test_search_with_player_perspectives(self):
        """Test enhanced search with player perspective filter."""
        response = self.client.get(
            "/igdb/search-enhanced?q=halo&player_perspectives=1,2"
        )
        self.assertEqual(200, response.status_code)
        data = response.json()
        self.assertIsInstance(data, list)

    def test_search_with_all_filters_combined(self):
        """Test enhanced search with multiple filter types combined."""
        response = self.client.get(
            "/igdb/search-enhanced?q=halo"
            "&platforms=6,48"
            "&years=2020"
            "&genres=4,5"
            "&min_rating=75"
            "&max_rating=95"
            "&themes=18"
            "&player_perspectives=1"
        )
        self.assertEqual(200, response.status_code)
        data = response.json()
        self.assertIsInstance(data, list)

    def test_search_empty_results(self):
        """Test enhanced search returns empty list when query matches nothing."""
        response = self.client.get("/igdb/search-enhanced?q=empty")
        self.assertEqual(200, response.status_code)
        data = response.json()
        self.assertEqual([], data)

    def test_search_result_structure(self):
        """Test that each result has the expected GameOut fields."""
        response = self.client.get("/igdb/search-enhanced?q=halo")
        self.assertEqual(200, response.status_code)
        data = response.json()
        for game in data:
            self.assertIn("id", game)
            self.assertIn("name", game)
            self.assertIn("cover_url", game)
            self.assertIn("summary", game)
            self.assertIn("release_date", game)
            self.assertIn("genres", game)
            self.assertIn("platforms", game)


class TestEnhancedSearchValidation(BaseEnhancedSearchApiTest):
    """Tests for input validation on /igdb/search-enhanced."""

    def test_missing_query_param(self):
        """Test that missing q parameter returns 422."""
        response = self.client.get("/igdb/search-enhanced")
        self.assertEqual(422, response.status_code)

    def test_empty_query_param(self):
        """Test that empty q parameter returns 422."""
        response = self.client.get("/igdb/search-enhanced?q=")
        self.assertEqual(422, response.status_code)

    def test_whitespace_only_query(self):
        """Test that whitespace-only query returns 422."""
        response = self.client.get("/igdb/search-enhanced?q=   ")
        self.assertEqual(422, response.status_code)

    def test_invalid_platform_ids(self):
        """Test that non-numeric platform IDs return 422."""
        response = self.client.get("/igdb/search-enhanced?q=halo&platforms=abc,def")
        self.assertEqual(422, response.status_code)

    def test_invalid_year_ids(self):
        """Test that non-numeric year values return 422."""
        response = self.client.get("/igdb/search-enhanced?q=halo&years=abc")
        self.assertEqual(422, response.status_code)

    def test_invalid_genre_ids(self):
        """Test that non-numeric genre IDs return 422."""
        response = self.client.get("/igdb/search-enhanced?q=halo&genres=not,a,number")
        self.assertEqual(422, response.status_code)

    def test_invalid_theme_ids(self):
        """Test that non-numeric theme IDs return 422."""
        response = self.client.get("/igdb/search-enhanced?q=halo&themes=abc")
        self.assertEqual(422, response.status_code)

    def test_invalid_player_perspective_ids(self):
        """Test that non-numeric perspective IDs return 422."""
        response = self.client.get(
            "/igdb/search-enhanced?q=halo&player_perspectives=abc"
        )
        self.assertEqual(422, response.status_code)

    def test_year_start_after_year_end(self):
        """Test that year_start > year_end returns 422."""
        response = self.client.get(
            "/igdb/search-enhanced?q=halo&year_start=2023&year_end=2020"
        )
        self.assertEqual(422, response.status_code)

    def test_min_rating_out_of_range_high(self):
        """Test that min_rating > 100 returns 422."""
        response = self.client.get("/igdb/search-enhanced?q=halo&min_rating=150")
        self.assertEqual(422, response.status_code)

    def test_min_rating_out_of_range_negative(self):
        """Test that negative min_rating returns 422."""
        response = self.client.get("/igdb/search-enhanced?q=halo&min_rating=-5")
        self.assertEqual(422, response.status_code)

    def test_max_rating_out_of_range(self):
        """Test that max_rating > 100 returns 422."""
        response = self.client.get("/igdb/search-enhanced?q=halo&max_rating=200")
        self.assertEqual(422, response.status_code)

    def test_year_start_out_of_range(self):
        """Test that year_start < 1970 returns 422."""
        response = self.client.get(
            "/igdb/search-enhanced?q=halo&year_start=1800&year_end=2020"
        )
        self.assertEqual(422, response.status_code)

    def test_year_end_out_of_range(self):
        """Test that year_end > 2030 returns 422."""
        response = self.client.get(
            "/igdb/search-enhanced?q=halo&year_start=2020&year_end=2050"
        )
        self.assertEqual(422, response.status_code)

    def test_empty_platform_string_ignored(self):
        """Test that empty platform string is treated as no filter."""
        response = self.client.get("/igdb/search-enhanced?q=halo&platforms=")
        self.assertEqual(200, response.status_code)

    def test_empty_year_string_ignored(self):
        """Test that empty year string is treated as no filter."""
        response = self.client.get("/igdb/search-enhanced?q=halo&years=")
        self.assertEqual(200, response.status_code)


class TestEnhancedSearchErrors(BaseEnhancedSearchApiTest):
    """Tests for error handling on /igdb/search-enhanced."""

    def test_client_error_returns_500(self):
        """Test that a client exception returns 500."""
        response = self.client.get("/igdb/search-enhanced?q=error")
        self.assertEqual(500, response.status_code)
        data = response.json()
        self.assertIn("detail", data)

    def test_content_type_json(self):
        """Test that response content type is JSON."""
        response = self.client.get("/igdb/search-enhanced?q=halo")
        self.assertEqual(
            "application/json", response.headers["content-type"].split(";")[0]
        )


class TestEnhancedSearchFilterPassing(BaseEnhancedSearchApiTest):
    """Tests verifying that filters are correctly parsed and passed to the client."""

    def test_platforms_parsed_to_list(self):
        """Test that comma-separated platforms are parsed into a list of ints."""
        with patch.object(
            MockIGDBClient, "search_games_enhanced", return_value=[]
        ) as mock_search:
            # Re-override with our patched mock
            app.dependency_overrides[get_igdb_client] = MockIGDBClient
            self.client.get("/igdb/search-enhanced?q=halo&platforms=6,48,130")

            mock_search.assert_called_once()
            call_args = mock_search.call_args
            filters = call_args[0][1]  # second positional arg = filters
            self.assertEqual(filters.platforms, [6, 48, 130])

    def test_years_parsed_to_list(self):
        """Test that comma-separated years are parsed into a list of ints."""
        with patch.object(
            MockIGDBClient, "search_games_enhanced", return_value=[]
        ) as mock_search:
            app.dependency_overrides[get_igdb_client] = MockIGDBClient
            self.client.get("/igdb/search-enhanced?q=halo&years=2020,2021")

            mock_search.assert_called_once()
            call_args = mock_search.call_args
            filters = call_args[0][1]
            self.assertEqual(filters.years, [2020, 2021])

    def test_year_range_parsed(self):
        """Test that year_start and year_end are parsed into a YearRange."""
        with patch.object(
            MockIGDBClient, "search_games_enhanced", return_value=[]
        ) as mock_search:
            app.dependency_overrides[get_igdb_client] = MockIGDBClient
            self.client.get(
                "/igdb/search-enhanced?q=halo&year_start=2018&year_end=2022"
            )

            mock_search.assert_called_once()
            call_args = mock_search.call_args
            filters = call_args[0][1]
            self.assertEqual(filters.year_range.start, 2018)
            self.assertEqual(filters.year_range.end, 2022)

    def test_genres_parsed_to_list(self):
        """Test that comma-separated genres are parsed into a list of ints."""
        with patch.object(
            MockIGDBClient, "search_games_enhanced", return_value=[]
        ) as mock_search:
            app.dependency_overrides[get_igdb_client] = MockIGDBClient
            self.client.get("/igdb/search-enhanced?q=halo&genres=4,12,31")

            mock_search.assert_called_once()
            call_args = mock_search.call_args
            filters = call_args[0][1]
            self.assertEqual(filters.genres, [4, 12, 31])

    def test_rating_parsed_to_float(self):
        """Test that min_rating and max_rating are parsed correctly."""
        with patch.object(
            MockIGDBClient, "search_games_enhanced", return_value=[]
        ) as mock_search:
            app.dependency_overrides[get_igdb_client] = MockIGDBClient
            self.client.get(
                "/igdb/search-enhanced?q=halo&min_rating=75.5&max_rating=90.0"
            )

            mock_search.assert_called_once()
            call_args = mock_search.call_args
            filters = call_args[0][1]
            self.assertEqual(filters.min_rating, 75.5)
            self.assertEqual(filters.max_rating, 90.0)

    def test_themes_parsed_to_list(self):
        """Test that comma-separated themes are parsed into a list of ints."""
        with patch.object(
            MockIGDBClient, "search_games_enhanced", return_value=[]
        ) as mock_search:
            app.dependency_overrides[get_igdb_client] = MockIGDBClient
            self.client.get("/igdb/search-enhanced?q=horror&themes=18,19")

            mock_search.assert_called_once()
            call_args = mock_search.call_args
            filters = call_args[0][1]
            self.assertEqual(filters.themes, [18, 19])

    def test_player_perspectives_parsed(self):
        """Test that player perspectives are parsed correctly."""
        with patch.object(
            MockIGDBClient, "search_games_enhanced", return_value=[]
        ) as mock_search:
            app.dependency_overrides[get_igdb_client] = MockIGDBClient
            self.client.get("/igdb/search-enhanced?q=halo&player_perspectives=1,2,7")

            mock_search.assert_called_once()
            call_args = mock_search.call_args
            filters = call_args[0][1]
            self.assertEqual(filters.player_perspectives, [1, 2, 7])

    def test_no_filters_passes_none(self):
        """Test that no filter params passes None as filters to the client."""
        with patch.object(
            MockIGDBClient, "search_games_enhanced", return_value=[]
        ) as mock_search:
            app.dependency_overrides[get_igdb_client] = MockIGDBClient
            self.client.get("/igdb/search-enhanced?q=halo")

            mock_search.assert_called_once()
            call_args = mock_search.call_args
            filters = call_args[0][1]
            self.assertIsNone(filters)

    def test_combined_filters_all_parsed(self):
        """Test that all filter params are parsed into the GameFilters object."""
        with patch.object(
            MockIGDBClient, "search_games_enhanced", return_value=[]
        ) as mock_search:
            app.dependency_overrides[get_igdb_client] = MockIGDBClient
            self.client.get(
                "/igdb/search-enhanced?q=halo"
                "&platforms=6,48"
                "&years=2020"
                "&year_start=2018&year_end=2022"
                "&genres=4"
                "&min_rating=80"
                "&max_rating=95"
                "&themes=18"
                "&player_perspectives=1"
            )

            mock_search.assert_called_once()
            call_args = mock_search.call_args
            filters = call_args[0][1]
            self.assertEqual(filters.platforms, [6, 48])
            self.assertEqual(filters.years, [2020])
            self.assertEqual(filters.year_range.start, 2018)
            self.assertEqual(filters.year_range.end, 2022)
            self.assertEqual(filters.genres, [4])
            self.assertEqual(filters.min_rating, 80.0)
            self.assertEqual(filters.max_rating, 95.0)
            self.assertEqual(filters.themes, [18])
            self.assertEqual(filters.player_perspectives, [1])


if __name__ == "__main__":
    unittest.main()
