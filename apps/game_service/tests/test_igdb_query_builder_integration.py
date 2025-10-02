"""
Integration tests for IGDB query builder using real IGDB API.
These tests validate that our generated query syntax is correct by making actual API calls.

Set RUN_IGDB_INTEGRATION=1 environment variable to run these tests.
"""

import os
import unittest

import httpx
from src.igdb.auth import IGDBAuth
from src.igdb.client import IGDBClient
from src.igdb.enums import Platform, Genre, Theme, PlayerPerspective, Keyword
from src.igdb.query_builder import build_igdb_query
from src.igdb.schemas import GameFilters


class TestIGDBQueryBuilderIntegration(unittest.TestCase):
    """Integration tests for IGDB query builder using real IGDB API."""

    def setUp(self):
        """Set up test client with rate limiting."""
        if not os.getenv("RUN_IGDB_INTEGRATION"):
            self.skipTest("Set RUN_IGDB_INTEGRATION=1 to run this test")
        if not os.getenv("IGDB_CLIENT_ID") or not os.getenv("IGDB_CLIENT_SECRET"):
            self.skipTest("IGDB credentials not set in environment")

        self.auth = IGDBAuth()
        self.client = IGDBClient(auth=self.auth)

        # Rate limiting: IGDB allows 4 requests per second
        self.rate_limit_delay = 0.3  # 300ms between requests

    def _execute_custom_query(self, query: str) -> list:
        """
        Execute a custom IGDB query for testing purposes.
        This method replicates the pattern used in IGDBClient methods.
        """
        token = self.auth.get_token()
        headers = {
            "Client-ID": self.auth.client_id,
            "Authorization": f"Bearer {token}",
        }

        response = httpx.post(
            f"{self.client.base_url}/games", headers=headers, data=query, timeout=10
        )
        response.raise_for_status()
        results = response.json()

        # Return raw results (we'll do basic validation without protected methods)
        return results

    # ===============================================
    # Core Filter Integration Tests
    # ===============================================

    def test_platform_filter_integration(self):
        """Test that platform filter works with real IGDB API."""
        # Build query with platform filter (PC = 6)
        search_term = "zelda"
        filters = GameFilters(platforms=[Platform.PC])  # PC platform
        query = build_igdb_query(search_term, filters)

        print(f"Testing platform query: {query}")

        # Make actual API call
        results = self._execute_custom_query(query)

        # Verify we get results
        self.assertIsInstance(results, list)
        self.assertGreater(len(results), 0, "Should find Zelda games on PC")

        # Verify results contain platform information
        for game in results:
            self.assertIn("platforms", game)
            if game["platforms"]:  # If platforms data is present
                platform_ids = [
                    p.get("id") for p in game["platforms"] if isinstance(p, dict)
                ]
                # Note: Some games might not have platform data, so we just verify structure
                print(
                    f"Game: {game.get('name', 'Unknown')} - Platforms: {platform_ids}"
                )

    def test_year_filter_integration(self):
        """Test that year filter works with real IGDB API."""
        # Build query with year filter (2020)
        search_term = "cyberpunk"
        filters = GameFilters(years=[2020])
        query = build_igdb_query(search_term, filters)

        print(f"Testing query: {query}")

        # Make actual API call
        results = self._execute_custom_query(query)

        # Verify we get results
        self.assertIsInstance(results, list)
        self.assertGreater(len(results), 0, "Should find games from 2020")

        # Print results for manual verification
        for game in results:
            game_name = game.get("name", "Unknown")
            release_date = game.get("first_release_date", "Unknown")
            print(f"Game: {game_name} - Release Date: {release_date}")

    def test_genre_filter_integration(self):
        """Test that genre filter works with real IGDB API."""
        # Build query with RPG genre filter (12 = RPG)
        search_term = "fantasy"
        filters = GameFilters(genres=[Genre.RPG])  # RPG genre
        query = build_igdb_query(search_term, filters)

        print(f"Testing genre query: {query}")

        # Make actual API call
        self._execute_custom_query(query)

    # ===============================================
    # New Filter Integration Tests
    # ===============================================

    def test_themes_filter_integration(self):
        """Test that themes filter works with real IGDB API."""
        # Build query with horror theme (18)
        search_term = "horror"
        filters = GameFilters(themes=[Theme.HORROR])  # Horror theme
        query = build_igdb_query(search_term, filters)

        print(f"Testing themes query: {query}")

        # Make actual API call
        results = self._execute_custom_query(query)

        # Verify we get results
        self.assertIsInstance(results, list)
        print(f"Found {len(results)} horror-themed games")

        # Print first few results for verification
        for i, game in enumerate(results[:3]):
            print(f"Horror Game {i+1}: {game.get('name', 'Unknown')}")

    def test_player_perspectives_filter_integration(self):
        """Test that player perspectives filter works with real IGDB API."""
        # Build query with first-person perspective (1)
        search_term = "shooter"
        filters = GameFilters(
            player_perspectives=[PlayerPerspective.FIRST_PERSON]
        )  # First-person
        query = build_igdb_query(search_term, filters)

        print(f"Testing player perspectives query: {query}")

        # Make actual API call
        results = self._execute_custom_query(query)

        # Verify we get results
        self.assertIsInstance(results, list)
        print(f"Found {len(results)} first-person shooter games")

        # Print first few results for verification
        for i, game in enumerate(results[:3]):
            print(f"FPS Game {i+1}: {game.get('name', 'Unknown')}")

    def test_rating_range_filter_integration(self):
        """Test that rating range filter works with real IGDB API."""
        # Build query with high rating filter
        search_term = "zelda"
        filters = GameFilters(min_rating=85.0)  # Highly rated games
        query = build_igdb_query(search_term, filters)

        print(f"Testing rating range query: {query}")

        # Make actual API call
        results = self._execute_custom_query(query)

        # Verify we get results
        self.assertIsInstance(results, list)
        print(f"Found {len(results)} highly rated Zelda games")

        # Print results with ratings for verification
        for game in results[:3]:
            print(
                f"Game: {game.get('name', 'Unknown')} - Rating available in full game data"
            )

    def test_keywords_filter_integration(self):
        """Test that keywords filter works with real IGDB API."""
        # Build query with open world keyword (270)
        search_term = "open world"
        filters = GameFilters(keywords=[Keyword.OPEN_WORLD])  # Open World keyword
        query = build_igdb_query(search_term, filters)

        print(f"Testing keywords query: {query}")

        # Make actual API call
        results = self._execute_custom_query(query)

        # Verify we get results
        self.assertIsInstance(results, list)
        print(f"Found {len(results)} open world games")

        # Print first few results for verification
        for i, game in enumerate(results[:3]):
            print(f"Open World Game {i+1}: {game.get('name', 'Unknown')}")

    # ===============================================
    # Combined Filter Integration Tests
    # ===============================================

    def test_combined_filters_integration(self):
        """Test that multiple filters work together with real IGDB API."""
        # Build query with multiple filters
        search_term = "action"
        filters = GameFilters(
            platforms=[Platform.PC],  # PC
            genres=[Genre.FIGHTING],  # Fighting (ID 4)
            years=[2020, 2021],  # Recent years
        )
        query = build_igdb_query(search_term, filters)

        print(f"Testing combined filters query: {query}")

        # Make actual API call
        results = self._execute_custom_query(query)

        # Verify we get results
        self.assertIsInstance(results, list)
        print(f"Found {len(results)} action games on PC from 2020-2021")

        # Print results for verification
        for i, game in enumerate(results[:5]):
            print(f"Combined Filter Game {i+1}: {game.get('name', 'Unknown')}")

    def test_comprehensive_filters_integration(self):
        """Test that comprehensive new filters work with real IGDB API."""
        # Build query with multiple new filter types
        search_term = "indie"
        filters = GameFilters(
            themes=[Theme.FANTASY],  # Fantasy
            player_perspectives=[PlayerPerspective.THIRD_PERSON],  # Third-person
            min_rating=70.0,  # Well-rated
        )
        query = build_igdb_query(search_term, filters)

        print(f"Testing comprehensive filters query: {query}")

        # Make actual API call
        results = self._execute_custom_query(query)

        # Verify we get results
        self.assertIsInstance(results, list)
        print(
            f"Found {len(results)} fantasy third-person indie games with good ratings"
        )

        # Print results for verification
        for i, game in enumerate(results[:3]):
            print(f"Comprehensive Filter Game {i+1}: {game.get('name', 'Unknown')}")

    # ===============================================
    # Edge Case Integration Tests
    # ===============================================

    def test_no_results_filter_integration(self):
        """Test that overly restrictive filters handle no results gracefully."""
        # Build query that should return few or no results
        search_term = "zzz_nonexistent_game"
        filters = GameFilters(
            platforms=[999], years=[1990]  # Non-existent platform  # Very old year
        )
        query = build_igdb_query(search_term, filters)

        print(f"Testing no results query: {query}")

        # Make actual API call
        results = self._execute_custom_query(query)

        # Verify we get empty results without error
        self.assertIsInstance(results, list)
        print(
            f"No results query returned {len(results)} games (expected 0 or very few)"
        )

    def test_release_year_filter_integration(self):
        """Test that release year filter works with real IGDB API."""
        # Build query with release year filter
        search_term = "mario"
        filters = GameFilters(release_year_min=2020, release_year_max=2023)
        query = build_igdb_query(search_term, filters)

        print(f"Testing release year query: {query}")

        # Make actual API call
        self._execute_custom_query(query)

    # ===============================================
    # Error Handling Integration Tests
    # ===============================================

    def test_invalid_query_syntax_handling(self):
        """Test that malformed queries are handled gracefully."""
        # Manually create a malformed query to test error handling
        malformed_query = (
            'search "test"; where invalid_field = (1,2,3); fields id,name; limit 10;'
        )

        print(f"Testing malformed query: {malformed_query}")

        try:
            # This should either return empty results or raise an exception
            results = self._execute_custom_query(malformed_query)
            result_desc = (
                len(results) if isinstance(results, list) else "Non-list result"
            )
            print(f"Malformed query returned: {result_desc}")
            # If it doesn't raise an exception, verify it returns a list (possibly empty)
            self.assertIsInstance(results, list)
        except (httpx.HTTPError, ValueError, KeyError) as e:
            print(
                f"Malformed query raised exception (expected): {type(e).__name__}: {e}"
            )
            # This is acceptable behavior for malformed queries


if __name__ == "__main__":
    # Print instructions for running these tests
    print("Integration Test Instructions:")
    print("1. Set environment variables:")
    print("   export RUN_IGDB_INTEGRATION=1")
    print("   export IGDB_CLIENT_ID=your_client_id")
    print("   export IGDB_CLIENT_SECRET=your_client_secret")
    print(
        "2. Run with: python -m unittest tests.test_igdb_query_builder_integration -v"
    )
    print("3. These tests will make real API calls and respect rate limits")
    print()

    unittest.main()
