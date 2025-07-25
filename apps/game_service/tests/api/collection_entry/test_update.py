"""
Tests for the PUT (update) collection entry API endpoints.
"""

# pylint: disable=duplicate-code, wrong-import-order

from unittest.mock import Mock, patch

from tests.api.collection_entry.test_base import (
    BaseCollectionEntryAPITest,
    generate_mock_jwt,
)
from tests.conftest import TestingSessionLocal
from tests.utils import MOCK_IGDB_GAME, setup_mock_igdb_client

from db.models.collection import Collection, CollectionEntry


class TestUpdateCollectionEntry(BaseCollectionEntryAPITest):
    """Test cases for PUT /collections/{collection_id}/entries/{entry_id} endpoint."""

    @patch("src.api.collection_entry.IGDBClient")
    def test_update_collection_entry_success(self, mock_igdb_client_class):
        """
        Should successfully update a collection entry via API.
        """
        mock_igdb_client = Mock()
        setup_mock_igdb_client(mock_igdb_client, MOCK_IGDB_GAME)
        mock_igdb_client_class.return_value = mock_igdb_client

        # Create entry
        payload = {"game_id": 1, "notes": "Initial", "status": "playing", "rating": 7}
        create_resp = self.client.post(
            f"/collections/{self.test_collection.id}/entries/",
            json=payload,
            headers=self.headers,
        )
        self.assertEqual(create_resp.status_code, 201)
        entry_id = create_resp.json()["id"]

        # Update entry
        update_payload = {
            "notes": "Updated notes",
            "status": "completed",
            "rating": 9,
            "custom_tags": {"favorite": True},
        }
        update_resp = self.client.put(
            f"/collections/{self.test_collection.id}/entries/{entry_id}",
            json=update_payload,
            headers=self.headers,
        )
        self.assertEqual(update_resp.status_code, 200)
        data = update_resp.json()
        self.assertEqual(data["notes"], "Updated notes")
        self.assertEqual(data["status"], "completed")
        self.assertEqual(data["rating"], 9)
        self.assertEqual(data["custom_tags"], {"favorite": True})

    def test_update_collection_entry_not_found(self):
        """
        Should return 404 if entry does not exist.
        """
        update_payload = {"notes": "Should not work"}
        resp = self.client.put(
            f"/collections/{self.test_collection.id}/entries/9999",
            json=update_payload,
            headers=self.headers,
        )
        self.assertEqual(resp.status_code, 404)
        data = resp.json()
        self.assertEqual(data["detail"], "Entry not found")

    def test_update_collection_entry_permission_denied(self):
        """
        Should return 403 if user does not own the collection.
        """
        # Create entry as user 1
        payload = {"game_id": 1, "notes": "Initial"}
        create_resp = self.client.post(
            f"/collections/{self.test_collection.id}/entries/",
            json=payload,
            headers=self.headers,
        )
        self.assertEqual(create_resp.status_code, 201)
        entry_id = create_resp.json()["id"]
        # Create user 2 and try to update
        self.add_user(
            username="otheruser", email="other@example.com", password="irrelevant"
        )
        other_headers = {"Authorization": generate_mock_jwt("otheruser")}
        update_payload = {"notes": "Should not work"}
        resp = self.client.put(
            f"/collections/{self.test_collection.id}/entries/{entry_id}",
            json=update_payload,
            headers=other_headers,
        )
        self.assertEqual(resp.status_code, 403)
        data = resp.json()
        self.assertEqual(data["detail"], "Permission denied")

    def test_update_collection_entry_wrong_collection(self):
        """
        Should return 404 if entry_id does not belong to the given collection_id.
        """
        payload = {"game_id": 1, "notes": "Initial"}
        create_resp = self.client.post(
            f"/collections/{self.test_collection.id}/entries/",
            json=payload,
            headers=self.headers,
        )
        self.assertEqual(create_resp.status_code, 201)
        entry_id = create_resp.json()["id"]
        # Create another collection for same user
        new_collection = self.add_collection(user_id=1, name="Another Collection")
        update_payload = {"notes": "Should not work"}
        resp = self.client.put(
            f"/collections/{new_collection.id}/entries/{entry_id}",
            json=update_payload,
            headers=self.headers,
        )
        self.assertEqual(resp.status_code, 404)
        data = resp.json()
        self.assertEqual(data["detail"], "Entry not found")

    def test_update_collection_entry_no_fields(self):
        """
        Should not update anything if no fields are provided (returns unchanged).
        """
        payload = {"game_id": 1, "notes": "Initial", "status": "playing"}
        create_resp = self.client.post(
            f"/collections/{self.test_collection.id}/entries/",
            json=payload,
            headers=self.headers,
        )
        self.assertEqual(create_resp.status_code, 201)
        entry_id = create_resp.json()["id"]
        update_payload = {}  # No fields to update
        update_resp = self.client.put(
            f"/collections/{self.test_collection.id}/entries/{entry_id}",
            json=update_payload,
            headers=self.headers,
        )
        self.assertEqual(update_resp.status_code, 200)
        data = update_resp.json()
        self.assertEqual(data["notes"], "Initial")
        self.assertEqual(data["status"], "playing")

    def test_update_collection_entry_invalid_field(self):
        """
        Should ignore invalid fields in update data and not raise error.
        """
        payload = {"game_id": 1, "notes": "Initial", "status": "playing", "rating": 7}
        create_resp = self.client.post(
            f"/collections/{self.test_collection.id}/entries/",
            json=payload,
            headers=self.headers,
        )
        self.assertEqual(create_resp.status_code, 201)
        entry_id = create_resp.json()["id"]
        update_payload = {"game_id": 999, "notes": "Valid update", "foo": "bar"}
        update_resp = self.client.put(
            f"/collections/{self.test_collection.id}/entries/{entry_id}",
            json=update_payload,
            headers=self.headers,
        )
        self.assertEqual(update_resp.status_code, 200)
        data = update_resp.json()
        self.assertEqual(data["notes"], "Valid update")
        self.assertEqual(data["game_id"], 1)  # Should not change

    def test_update_collection_entry_none_value(self):
        """
        Should allow updating a field to None (e.g., clear notes).
        """
        payload = {"game_id": 1, "notes": "Initial", "status": "playing"}
        create_resp = self.client.post(
            f"/collections/{self.test_collection.id}/entries/",
            json=payload,
            headers=self.headers,
        )
        self.assertEqual(create_resp.status_code, 201)
        entry_id = create_resp.json()["id"]
        update_payload = {"notes": None}
        update_resp = self.client.put(
            f"/collections/{self.test_collection.id}/entries/{entry_id}",
            json=update_payload,
            headers=self.headers,
        )
        self.assertEqual(update_resp.status_code, 200)
        data = update_resp.json()
        self.assertIsNone(data["notes"])
        self.assertEqual(data["status"], "playing")

    def test_update_collection_entry_after_delete(self):
        """
        Should return 404 if entry is deleted then updated.
        """
        payload = {"game_id": 1, "notes": "Initial"}
        create_resp = self.client.post(
            f"/collections/{self.test_collection.id}/entries/",
            json=payload,
            headers=self.headers,
        )
        self.assertEqual(create_resp.status_code, 201)
        entry_id = create_resp.json()["id"]
        # Delete the entry directly via DB

        db = TestingSessionLocal()
        db.delete(db.query(CollectionEntry).get(entry_id))
        db.commit()
        db.close()
        update_payload = {"notes": "Should not work"}
        resp = self.client.put(
            f"/collections/{self.test_collection.id}/entries/{entry_id}",
            json=update_payload,
            headers=self.headers,
        )
        self.assertEqual(resp.status_code, 404)
        data = resp.json()
        self.assertEqual(data["detail"], "Entry not found")

    def test_update_collection_entry_after_collection_delete(self):
        """
        Should return 404 if collection is deleted then entry is updated.
        """
        payload = {"game_id": 1, "notes": "Initial"}
        create_resp = self.client.post(
            f"/collections/{self.test_collection.id}/entries/",
            json=payload,
            headers=self.headers,
        )
        self.assertEqual(create_resp.status_code, 201)
        entry_id = create_resp.json()["id"]
        # Delete the collection directly via DB
        db = TestingSessionLocal()
        db.delete(db.query(Collection).get(self.test_collection.id))
        db.commit()
        db.close()
        update_payload = {"notes": "Should not work"}
        resp = self.client.put(
            f"/collections/{self.test_collection.id}/entries/{entry_id}",
            json=update_payload,
            headers=self.headers,
        )
        self.assertEqual(resp.status_code, 404)
        data = resp.json()
        self.assertEqual(data["detail"], "Collection not found")

    def test_update_collection_entry_invalid_jwt(self):
        """
        Should return 401 Unauthorized if JWT is invalid.
        """
        payload = {"game_id": 1, "notes": "Initial"}
        create_resp = self.client.post(
            f"/collections/{self.test_collection.id}/entries/",
            json=payload,
            headers=self.headers,
        )
        self.assertEqual(create_resp.status_code, 201)
        entry_id = create_resp.json()["id"]
        update_payload = {"notes": "Should not work"}
        invalid_headers = {"Authorization": "Bearer invalid.jwt.token"}
        resp = self.client.put(
            f"/collections/{self.test_collection.id}/entries/{entry_id}",
            json=update_payload,
            headers=invalid_headers,
        )
        self.assertEqual(resp.status_code, 401)
        data = resp.json()
        self.assertIn("detail", data)
        self.assertIn("detail", data)
