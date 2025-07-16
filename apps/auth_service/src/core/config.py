# pylint: disable=too-few-public-methods
"""
Configuration loader for Auth Service.
Loads environment variables and secrets for the auth service using python-dotenv.
"""

import os
from dotenv import load_dotenv

# Load environment variables from .env file (if present)
load_dotenv()


class Settings:
    """
    Settings for the authentication service, loaded from environment variables.
    """

    JWT_SECRET_KEY: str = os.getenv("JWT_SECRET_KEY", "")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = int(
        os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "30")
    )
