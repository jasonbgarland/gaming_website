"""
Test utilities for game service tests.
"""

# Mock IGDB game response
MOCK_IGDB_GAME = {
    "id": 1,
    "name": "Mock Game",
    "summary": "A mock game for testing",
    "cover": {"url": "//images.igdb.com/igdb/image/upload/t_cover_big/mockcover.jpg"},
    "first_release_date": 1578960000,
    "genres": [{"id": 5, "name": "Shooter"}],
    "platforms": [{"id": 48, "name": "PlayStation 4"}],
}


def setup_mock_igdb_client(mock_client, mock_game_data=None):
    """
    Set up a mock IGDB client for testing purposes.

    Args:
        mock_client: The mock client instance to set up
        mock_game_data: Optional game data to return. Defaults to MOCK_IGDB_GAME.
    """
    if mock_game_data is None:
        mock_game_data = MOCK_IGDB_GAME

    # Set up default behaviors
    mock_client.get_game_by_id.return_value = mock_game_data
    mock_client.search_games.return_value = [mock_game_data]
    mock_client.get_games_by_ids.return_value = [mock_game_data]

    # Add any other IGDB client methods that need mocking
    return mock_client
