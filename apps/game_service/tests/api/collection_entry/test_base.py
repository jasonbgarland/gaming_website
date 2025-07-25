"""
Base test class for collection entry API endpoints.
"""

# pylint: disable=wrong-import-order

from tests.test_base import TestDBBase

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


class BaseCollectionEntryAPITest(TestDBBase):
    """Base test class for collection entry API tests with common setup."""

    def setUp(self):
        # pylint: disable=duplicate-code
        super().setUp()
        self.headers = {"Authorization": MOCK_JWT}
        # Create user with id=1
        self.add_user(
            username="testuser",
            email="testuser@example.com",
            password="$2b$12$KIXQJQbQhQJQbQhQJQbQhOQJQbQhQJQbQhQJQbQhQJQbQhQJQbQhO",
        )

        # Create a collection for the user
        self.test_collection = self.add_collection(
            user_id=1, name="Test Collection", description="Test Description"
        )

        # Patch for IGDB client setup could be added here if needed by all tests
        # Patch for IGDB client setup could be added here if needed by all tests
        # Patch for IGDB client setup could be added here if needed by all tests
        # Patch for IGDB client setup could be added here if needed by all tests
        # Patch for IGDB client setup could be added here if needed by all tests
        # Patch for IGDB client setup could be added here if needed by all tests
