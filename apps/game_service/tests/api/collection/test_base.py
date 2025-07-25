"""
Base test class for collection API endpoints.
"""

from tests.test_base import TestDBBase

# pylint: disable=wrong-import-order
from shared.core.jwt_utils import create_access_token


def generate_mock_jwt(username: str = "testuser") -> str:
    """
    Generate a mock JWT for testing purposes.

    Args:
        username (str): The username to include in the JWT payload. Defaults to "testuser".

    Returns:
        str: A mock JWT string prefixed with "Bearer ".
    """
    token = create_access_token({"sub": username})
    return f"Bearer {token}"


MOCK_JWT = generate_mock_jwt()


class BaseCollectionAPITest(TestDBBase):
    """
    Base test class for collection API tests.
    Provides common setup and utility methods for all collection API tests.
    """

    def setUp(self):
        # pylint: disable=duplicate-code
        super().setUp()
        self.headers = {"Authorization": MOCK_JWT}
        # Create user with id=1
        self.add_user(
            username="testuser",
            email="testuser@example.com",
            password="$2b$12$KIXQJQbQhQJQbQhOQJQbQhQJQbQhQJQbQhQJQbQhQJQbQhQJQbQhO",
        )
