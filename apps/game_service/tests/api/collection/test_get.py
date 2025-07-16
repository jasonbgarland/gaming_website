"""
Tests for the get collection by ID API endpoints.
"""

# pylint: disable=duplicate-code,wrong-import-order

from unittest.mock import patch

from apps.game_service.tests.api.collection.test_base import (
    BaseCollectionAPITest,
    generate_mock_jwt,
)


class TestGetCollectionById(BaseCollectionAPITest):
    """
    Integration tests for GET /collections/{collection_id} API route.
    """

    def setUp(self):
        super().setUp()
        self.user_id = 1
        self.other_user_id = 2
        # Create user with id=1 already done in BaseCollectionAPITest
        self.add_user(username="user2", email="user2@example.com", password="pw2")
        # Create a collection for user1
        payload = {"name": "Library", "description": "User1's collection"}
        response = self.client.post("/collections/", json=payload, headers=self.headers)
        self.collection_id = response.json()["id"]

    def test_get_collection_by_id_success(self):
        """Authenticated user can fetch their own collection by ID."""
        response = self.client.get(
            f"/collections/{self.collection_id}", headers=self.headers
        )
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data["id"], self.collection_id)
        self.assertEqual(data["name"], "Library")
        self.assertEqual(data["user_id"], self.user_id)

    def test_get_collection_by_id_not_found(self):
        """Authenticated user gets 404 for non-existent collection."""
        response = self.client.get("/collections/99999", headers=self.headers)
        self.assertEqual(response.status_code, 404)

    def test_get_collection_by_id_wrong_user(self):
        """Authenticated user gets 404 for a collection they don't own."""
        # Create a collection for other user
        jwt_other = generate_mock_jwt(str(self.other_user_id))
        headers_other = {"Authorization": jwt_other}
        payload = {"name": "OtherUserColl", "description": "Other user's collection"}
        response = self.client.post(
            "/collections/", json=payload, headers=headers_other
        )
        other_collection_id = response.json()["id"]
        # Try to access as self
        response = self.client.get(
            f"/collections/{other_collection_id}", headers=self.headers
        )
        self.assertEqual(response.status_code, 404)

    def test_get_collection_by_id_invalid_id(self):
        """Invalid collection_id (string) returns 422."""
        response = self.client.get("/collections/not-an-int", headers=self.headers)
        self.assertEqual(response.status_code, 422)

    def test_get_collection_by_id_unauthenticated(self):
        """Unauthenticated request returns 401."""
        response = self.client.get(f"/collections/{self.collection_id}")
        self.assertEqual(response.status_code, 401)

    def test_get_collection_details_invalid_id_type_returns_422(self):
        """Should return 422 for non-integer collection_id, 404 for negative integer."""
        for invalid_id in ["abc", 3.14, "!@#"]:
            response = self.client.get(
                f"/collections/{invalid_id}", headers=self.headers
            )
            self.assertEqual(response.status_code, 422)
        response = self.client.get("/collections/-1", headers=self.headers)
        self.assertEqual(response.status_code, 404)

    def test_get_collection_details_unauthenticated_returns_401(self):
        """Should return 401 when no auth header is provided."""
        response = self.client.get("/collections/1")
        self.assertEqual(response.status_code, 401)

    def test_get_collection_details_db_error_returns_500(self):
        """Should return 500 when the service layer raises an exception."""
        # pylint: disable=line-too-long
        with patch(
            "apps.game_service.src.services.collection_service.CollectionService.get_collection_by_id",
            side_effect=Exception("DB error"),
        ):
            response = self.client.get("/collections/1", headers=self.headers)
            self.assertEqual(response.status_code, 500)

    def test_get_collection_details_wrong_user_returns_404(self):
        """Should return 404 when the collection does not belong to the user."""
        # Create a collection for other user
        jwt_other = generate_mock_jwt(str(self.other_user_id))
        headers_other = {"Authorization": jwt_other}
        payload = {"name": "OtherUserColl", "description": "Other user's collection"}
        response = self.client.post(
            "/collections/", json=payload, headers=headers_other
        )
        other_collection_id = response.json()["id"]
        # Try to access as self
        response = self.client.get(
            f"/collections/{other_collection_id}", headers=self.headers
        )
        self.assertEqual(response.status_code, 404)

    def test_get_collection_details_special_char_id_returns_422(self):
        """Should return 422 when collection_id contains special characters."""
        response = self.client.get("/collections/!@#", headers=self.headers)
        self.assertEqual(response.status_code, 422)

    def test_get_collection_details_large_id_returns_404(self):
        """Should return 404 when collection_id is a very large integer not present in DB."""
        response = self.client.get(f"/collections/{2**31}", headers=self.headers)
        self.assertEqual(response.status_code, 404)
