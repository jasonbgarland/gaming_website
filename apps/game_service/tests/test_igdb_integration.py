"""
Integration tests for IGDB API endpoints using real IGDB credentials and API.
"""

import os
import unittest

from fastapi.testclient import TestClient
from src.igdb.auth import IGDBAuth
from src.igdb.client import IGDBClient
from src.main import app


class TestIGDBIntegration(unittest.TestCase):
    """Integration tests for IGDB API endpoints using real IGDB credentials and API."""

    def test_batch_games_endpoint_real_api(self):
        """Test /igdb/games endpoint with real IGDB API and known game IDs."""
        # Only run if explicitly enabled and credentials are present
        if not os.getenv("RUN_IGDB_INTEGRATION"):
            self.skipTest("Set RUN_IGDB_INTEGRATION=1 to run this test")
        if not os.getenv("IGDB_CLIENT_ID") or not os.getenv("IGDB_CLIENT_SECRET"):
            self.skipTest("IGDB credentials not set in environment")
        # Use known IGDB game IDs (e.g., 1020 and 7346 for Zelda games)
        client = TestClient(app)
        response = client.get("/igdb/games?ids=1020,7346")
        print(
            "IGDB API Endpoint Results for batch games [1020,7346]:\n", response.json()
        )
        self.assertEqual(200, response.status_code)
        data = response.json()
        self.assertIsInstance(data, list)
        self.assertGreaterEqual(len(data), 1)
        for game in data:
            self.assertIn("id", game)
            self.assertIn("name", game)
            self.assertIn("cover_url", game)
            self.assertIn("summary", game)
            self.assertIn("release_date", game)
            self.assertIn("genres", game)
            self.assertIn("platforms", game)

    def test_genres_endpoint_real_api(self):
        """Test /igdb/genres endpoint with real IGDB API."""
        if not os.getenv("RUN_IGDB_INTEGRATION"):
            self.skipTest("Set RUN_IGDB_INTEGRATION=1 to run this test")
        if not os.getenv("IGDB_CLIENT_ID") or not os.getenv("IGDB_CLIENT_SECRET"):
            self.skipTest("IGDB credentials not set in environment")
        client = TestClient(app)
        response = client.get("/igdb/genres")
        print("IGDB API Endpoint Results for genres:\n", response.json())
        self.assertEqual(200, response.status_code)
        data = response.json()
        self.assertIsInstance(data, list)
        self.assertGreater(len(data), 0)
        self.assertIn("id", data[0])
        self.assertIn("name", data[0])

    def test_platforms_endpoint_real_api(self):
        """Test /igdb/platforms endpoint with real IGDB API."""
        if not os.getenv("RUN_IGDB_INTEGRATION"):
            self.skipTest("Set RUN_IGDB_INTEGRATION=1 to run this test")
        if not os.getenv("IGDB_CLIENT_ID") or not os.getenv("IGDB_CLIENT_SECRET"):
            self.skipTest("IGDB credentials not set in environment")
        client = TestClient(app)
        response = client.get("/igdb/platforms")
        print("IGDB API Endpoint Results for platforms:\n", response.json())
        self.assertEqual(200, response.status_code)
        data = response.json()
        self.assertIsInstance(data, list)
        self.assertGreater(len(data), 0)
        self.assertIn("id", data[0])
        self.assertIn("name", data[0])

    def test_search_games_real_api(self):
        """Test IGDBClient.search_games with real IGDB API and cover_images generation."""
        # Only run if explicitly enabled and credentials are present
        if not os.getenv("RUN_IGDB_INTEGRATION"):
            self.skipTest("Set RUN_IGDB_INTEGRATION=1 to run this test")
        if not os.getenv("IGDB_CLIENT_ID") or not os.getenv("IGDB_CLIENT_SECRET"):
            self.skipTest("IGDB credentials not set in environment")
        auth = IGDBAuth()
        client = IGDBClient(auth=auth)
        results = client.search_games("zelda")
        print("IGDB API Results for 'zelda':\n", results)
        self.assertIsInstance(results, list)
        self.assertGreater(len(results), 0)
        game = results[0]
        self.assertIn("id", game)
        self.assertIn("name", game)
        self.assertIn("cover_url", game)
        self.assertIn("cover_images", game)
        self.assertIn("summary", game)
        self.assertIn("release_date", game)
        self.assertIn("genres", game)
        self.assertIn("platforms", game)

        # Test cover_images responsive functionality
        if game["cover_url"]:
            print(f"Cover URL: {game['cover_url']}")
            print(f"Cover Images: {game['cover_images']}")

            # Should have responsive image URLs
            cover_images = game["cover_images"]
            self.assertIsInstance(cover_images, dict)

            if cover_images:  # Only test if cover_images is populated
                self.assertIn("thumb", cover_images)
                self.assertIn("small", cover_images)
                self.assertIn("medium", cover_images)
                self.assertIn("large", cover_images)

                # Each URL should be properly formatted
                for url in cover_images.values():
                    self.assertIsInstance(url, str)
                    self.assertTrue(url.startswith("https://images.igdb.com"))
                    self.assertTrue(url.endswith(".jpg"))

                # Verify different sizes have different URLs
                urls = list(cover_images.values())
                self.assertEqual(
                    len(set(urls)), len(urls), "All image URLs should be unique"
                )

                # Check specific size mappings
                self.assertIn("t_thumb", cover_images["thumb"])
                self.assertIn("t_cover_small", cover_images["small"])
                self.assertIn("t_cover_big", cover_images["medium"])
                self.assertIn("t_720p", cover_images["large"])

    def test_search_endpoint_real_api(self):
        """Test /igdb/search endpoint with real IGDB API."""
        # Only run if explicitly enabled and credentials are present
        if not os.getenv("RUN_IGDB_INTEGRATION"):
            self.skipTest("Set RUN_IGDB_INTEGRATION=1 to run this test")
        if not os.getenv("IGDB_CLIENT_ID") or not os.getenv("IGDB_CLIENT_SECRET"):
            self.skipTest("IGDB credentials not set in environment")
        client = TestClient(app)
        response = client.get("/igdb/search?q=zelda")
        print("IGDB API Endpoint Results for 'zelda':\n", response.json())
        self.assertEqual(200, response.status_code)
        data = response.json()
        self.assertIsInstance(data, list)
        self.assertGreater(len(data), 0)
        game = data[0]
        self.assertIn("id", game)
        self.assertIn("name", game)
        self.assertIn("cover_url", game)
        self.assertIn("summary", game)
        self.assertIn("release_date", game)
        self.assertIn("genres", game)
        self.assertIn("platforms", game)

    def test_get_game_by_id_endpoint_real_api(self):
        """Test /igdb/games/{id} endpoint with real IGDB API."""
        # Only run if explicitly enabled and credentials are present
        if not os.getenv("RUN_IGDB_INTEGRATION"):
            self.skipTest("Set RUN_IGDB_INTEGRATION=1 to run this test")
        if not os.getenv("IGDB_CLIENT_ID") or not os.getenv("IGDB_CLIENT_SECRET"):
            self.skipTest("IGDB credentials not set in environment")
        # Use a known IGDB game ID (e.g., 1020 for "The Legend of Zelda")
        game_id = 1020
        client = TestClient(app)
        response = client.get(f"/igdb/games/{game_id}")
        print(f"IGDB API Endpoint Results for game id {game_id}:\n", response.json())
        self.assertEqual(200, response.status_code)
        data = response.json()
        self.assertIsInstance(data, dict)
        self.assertEqual(game_id, data["id"])
        self.assertIn("name", data)
        self.assertIn("cover_url", data)
        self.assertIn("summary", data)
        self.assertIn("release_date", data)
        self.assertIn("genres", data)
        self.assertIn("platforms", data)


if __name__ == "__main__":
    unittest.main()
