# Collections API Documentation

This document describes all REST API endpoints for managing game collections in the Game Service API.

## Endpoints

- **POST** `/collections/` — Create a new collection
- **GET** `/collections/` — List all collections for the authenticated user
- **GET** `/collections/{collection_id}` — Get a specific collection by ID
- **PUT** `/collections/{collection_id}` — Update a specific collection
- **DELETE** `/collections/{collection_id}` — Delete a specific collection

---

# Create Collection API Route

This document describes the `/collections/` endpoint for creating a new game collection in the Game Service API.

## Endpoint

- **POST** `/collections/`

## Authentication

- Requires a valid JWT in the `Authorization` header (Bearer token).

## Request Body

- Content-Type: `application/json`
- Fields:
  - `name` (string, required): The name of the collection. Must be non-empty, unique per user, and may have length/character restrictions.
  - `description` (string, optional): A description of the collection. May have length restrictions.

### Example

```json
{
  "name": "Library",
  "description": "My main game collection"
}
```

## Validation Rules

- `name` is required and must:
  - Be non-empty
  - Not exceed maximum length (e.g., 255 chars)
  - Not contain invalid/special characters
  - Be unique for the user
- `description` is optional, but if provided:
  - Must not exceed maximum length (e.g., 1000 chars)
- Extra/unexpected fields may be ignored or rejected (see tests for behavior).

## Responses

- **201 Created**: Collection created successfully. Returns the new collection object.
- **400/409**: Duplicate collection name for the user.
- **401 Unauthorized**: Missing or invalid JWT.
- **422 Unprocessable Entity**: Validation errors (missing name, invalid characters, too long, etc.).
- **400/422**: Non-JSON payload or malformed request.

### Success Response Example

```json
{
  "id": 1,
  "user_id": 1,
  "name": "Library",
  "description": "My main game collection"
}
```

---

# List Collections API Route

This document describes the `/collections/` endpoint for listing a user's game collections in the Game Service API.

## Endpoint

- **GET** `/collections/`

## Authentication

- Requires a valid JWT in the `Authorization` header (Bearer token).

## Request

- No request body required.
- Must include the `Authorization` header.

## Responses

- **200 OK**: Returns a list of collection objects owned by the authenticated user. If the user has no collections, returns an empty list.
- **401 Unauthorized**: Missing or invalid JWT.
- **500 Internal Server Error**: Unexpected server error.

### Success Response Example

```json
[
  {
    "id": 1,
    "user_id": 1,
    "name": "Library",
    "description": "My main game collection"
  },
  {
    "id": 2,
    "user_id": 1,
    "name": "Backlog",
    "description": "Games to play later"
  }
]
```

## Notes

- Only collections belonging to the authenticated user are returned.
- The list is empty if the user has no collections.
- See tests for edge cases and validation behavior.

---

# Get Collection by ID API Route

This section documents the `/collections/{collection_id}` endpoint for retrieving a specific game collection by its ID in the Game Service API.

## Endpoint

- **GET** `/collections/{collection_id}`

## Authentication

- Requires a valid JWT in the `Authorization` header (Bearer token).

## Path Parameters

- `collection_id` (integer, required): The unique ID of the collection to retrieve.

## Responses

- **200 OK**: Returns the collection object if it exists and belongs to the authenticated user.
- **401 Unauthorized**: Missing or invalid JWT.
- **404 Not Found**: Collection does not exist or does not belong to the user.
- **422 Unprocessable Entity**: Invalid `collection_id` (e.g., not an integer, negative, or malformed).
- **500 Internal Server Error**: Unexpected server error (e.g., DB error).

### Success Response Example

```json
{
  "id": 1,
  "user_id": 1,
  "name": "Library",
  "description": "My main game collection"
}
```

## Validation & Edge Cases

- Only collections owned by the authenticated user are accessible.
- Requests for collections owned by other users return 404.
- Requests with invalid or special-character IDs return 422.
- Large or non-existent IDs return 404.
- All error cases are covered by unit and integration tests.

## Example Request

```sh
curl -H "Authorization: Bearer <jwt>" \
     http://localhost:8000/collections/1
```

## Notes

- See `test_api_collections.py` for comprehensive test coverage of this route, including edge cases and error handling.
- The route follows RESTful conventions and returns clear error messages for all failure modes.

---

# Update Collection API Route

This section documents the `/collections/{collection_id}` endpoint for updating a specific game collection in the Game Service API.

## Endpoint

- **PUT** `/collections/{collection_id}`

## Authentication

- Requires a valid JWT in the `Authorization` header (Bearer token).

## Path Parameters

- `collection_id` (integer, required): The unique ID of the collection to update.

## Request Body

- Content-Type: `application/json`
- Fields:
  - `name` (string, optional): The new name for the collection. Must be non-empty, unique per user, and may have length/character restrictions.
  - `description` (string, optional): The new description for the collection. May have length restrictions.

### Example

```json
{
  "name": "Updated Collection",
  "description": "Updated description"
}
```

## Validation Rules

- If provided, `name` must:
  - Be non-empty
  - Not exceed maximum length (e.g., 100 chars)
  - Not contain invalid/special characters
  - Be unique for the user
- If provided, `description` must not exceed maximum length (e.g., 500 chars)
- Extra/unexpected fields may be ignored or rejected (see tests for behavior).

## Responses

- **200 OK**: Collection updated successfully. Returns the updated collection object.
- **404 Not Found**: Collection does not exist or does not belong to the user.
- **409 Conflict**: Duplicate collection name for the user.
- **401 Unauthorized**: Missing or invalid JWT.
- **422 Unprocessable Entity**: Validation errors (invalid name, too long, etc.).

### Success Response Example

```json
{
  "id": 1,
  "user_id": 1,
  "name": "Updated Collection",
  "description": "Updated description"
}
```

## Example Request

```sh
curl -X PUT -H "Authorization: Bearer <jwt>" \
     -H "Content-Type: application/json" \
     -d '{"name": "Updated Collection", "description": "Updated description"}' \
     http://localhost:8000/collections/1
```

---

# Delete Collection API Route

This section documents the `/collections/{collection_id}` endpoint for deleting a specific game collection in the Game Service API.

## Endpoint

- **DELETE** `/collections/{collection_id}`

## Authentication

- Requires a valid JWT in the `Authorization` header (Bearer token).

## Path Parameters

- `collection_id` (integer, required): The unique ID of the collection to delete.

## Responses

- **204 No Content**: Collection deleted successfully.
- **404 Not Found**: Collection does not exist or does not belong to the user.
- **401 Unauthorized**: Missing or invalid JWT.
- **422 Unprocessable Entity**: Invalid `collection_id` (e.g., not an integer, negative, or malformed).
- **500 Internal Server Error**: Unexpected server error.

## Example Request

```sh
curl -X DELETE -H "Authorization: Bearer <jwt>" \
     http://localhost:8000/collections/1
```

## Notes

- Only collections owned by the authenticated user can be updated or deleted.
- All error cases are covered by unit and integration tests.
- See `test_api_collections.py` for comprehensive test coverage of these routes, including edge cases and error handling.
- The routes follow RESTful conventions and return clear error messages for all failure modes.

# Create Collection Entry API Route

See [COLLECTIONS_ENTRY_API.MD](./COLLECTIONS_ENTRY_API.MD) for documentation of the `/collections/{collection_id}/entries/` endpoints.
