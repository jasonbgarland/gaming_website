"""
Configuration loader for IGDB credentials and other settings.
"""

import os
from dotenv import load_dotenv

# Load environment variables from .env file (if present)
load_dotenv()


# pylint: disable=too-few-public-methods
class Settings:
    """Loads environment variables and secrets for the game service."""

    IGDB_CLIENT_ID: str = os.getenv("IGDB_CLIENT_ID", "")
    IGDB_CLIENT_SECRET: str = os.getenv("IGDB_CLIENT_SECRET", "")
    IGDB_BASE_URL: str = os.getenv("IGDB_BASE_URL", "https://api.igdb.com/v4")
