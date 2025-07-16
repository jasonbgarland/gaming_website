"""
Test utilities and shared mock data for game service tests.
"""

# Mock IGDB game data that can be reused across tests
MOCK_IGDB_GAME = {
    "id": 1,
    "name": "Test Game",
    "cover_url": "https://example.com/cover.jpg",
    "summary": "A test game",
    "release_date": 1234567890,
    "genres": ["Action", "Adventure"],
    "platforms": ["PC", "PlayStation"],
}

# Standard test user data
MOCK_TEST_USER = {
    "username": "testuser",
    "email": "testuser@example.com",
    "password": "$2b$12$KIXQJQbQhQJQbQhQJQbQhOQJQbQhQJQbQhQJQbQhQJQbQhQJQbQhO",
}


def create_mock_igdb_game(game_id: int = 1, name: str = "Test Game") -> dict:
    """Create a mock IGDB game object with customizable id and name."""
    return {
        "id": game_id,
        "name": name,
        "cover_url": "https://example.com/cover.jpg",
        "summary": f"A test game: {name}",
        "release_date": 1234567890,
        "genres": ["Action", "Adventure"],
        "platforms": ["PC", "PlayStation"],
    }


def setup_mock_igdb_client(mock_client, game_data=None):
    """Set up a mock IGDB client with default or custom game data."""
    if game_data is None:
        game_data = MOCK_IGDB_GAME
    mock_client.get_game_by_id.return_value = game_data
    return mock_client


def create_test_user_setup(
    test_instance, username="testuser", email="testuser@example.com"
):
    """Standard test user setup that can be reused across test classes."""
    test_instance.add_user(
        username=username,
        email=email,
        password="$2b$12$KIXQJQbQhQJQbQhQJQbQhOQJQbQhQJQbQhQJQbQhQJQbQhQJQbQhO",
    )
