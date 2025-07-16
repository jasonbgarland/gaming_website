# Create Collection Entry API Route

This section documents the `/collections/{collection_id}/entries/` endpoint for adding a game to a collection in the Game Service API.

## Endpoint

- **POST** `/collections/{collection_id}/entries/`

## Authentication

- Requires a valid JWT in the `Authorization` header (Bearer token).

## Path Parameters

- `collection_id` (integer, required): The unique ID of the collection to add an entry to.

## Request Body

- Content-Type: `application/json`
- Fields:
  - `game_id` (integer, required): The IGDB ID of the game to add. Must exist in IGDB.
  - `notes` (string, optional): User notes about the game.
  - `status` (string, optional): Status (e.g., "playing", "completed").
  - `rating` (integer, optional): User rating for the game.
  - `custom_tags` (object, optional): Custom tags as key-value pairs.

### Example

```json
{
  "game_id": 12345,
  "notes": "My favorite RPG!",
  "status": "playing",
  "rating": 10,
  "custom_tags": { "favorite": true, "genre": "RPG" }
}
```

## Validation Rules

- `game_id` is required and must be a valid IGDB game ID.
- Only the owner of the collection can add entries.
- Duplicate entries (same game in the same collection) are not allowed.
- All fields are validated according to the schema; extra/unexpected fields may be rejected.

## Responses

- **201 Created**: Entry created successfully. Returns the new collection entry object.
- **401 Unauthorized**: Missing or invalid JWT.
- **403 Forbidden**: User does not own the collection.
- **404 Not Found**: Collection does not exist, or game not found in IGDB.
- **409 Conflict**: Game already exists in the collection.
- **422 Unprocessable Entity**: Validation errors (missing/invalid fields).
- **500 Internal Server Error**: Unexpected server error.

### Success Response Example

```json
{
  "id": 1,
  "collection_id": 1,
  "game_id": 12345,
  "notes": "My favorite RPG!",
  "status": "playing",
  "rating": 10,
  "custom_tags": { "favorite": true, "genre": "RPG" },
  "added_at": "2025-07-15T18:00:00"
}
```

## Notes

- Only the collection owner can add entries.
- Game data is validated against IGDB using a real API client with OAuth.
- All error cases are covered by unit and integration tests (see `test_api_collections_entry.py`).
- The route follows RESTful conventions and returns clear error messages for all failure modes.

# List Collection Entries API Route

This section documents the `/collections/{collection_id}/entries/` endpoint for listing all entries in a collection.

## Endpoint

- **GET** `/collections/{collection_id}/entries/`

## Authentication

- Requires a valid JWT in the `Authorization` header (Bearer token).

## Path Parameters

- `collection_id` (integer, required): The unique ID of the collection to list entries for.

## Responses

- **200 OK**: Returns a list of collection entry objects, ordered by `added_at` (newest first).
- **401 Unauthorized**: Missing or invalid JWT.
- **403 Forbidden**: User does not own the collection.
- **404 Not Found**: Collection does not exist.
- **500 Internal Server Error**: Unexpected server error.

### Success Response Example

```json
[
  {
    "id": 1,
    "collection_id": 1,
    "game_id": 12345,
    "notes": "My favorite RPG!",
    "status": "playing",
    "rating": 10,
    "custom_tags": { "favorite": true, "genre": "RPG" },
    "added_at": "2025-07-15T18:00:00"
  },
  {
    "id": 2,
    "collection_id": 1,
    "game_id": 67890,
    "notes": "Another entry",
    "status": "completed",
    "rating": 8,
    "custom_tags": { "favorite": false },
    "added_at": "2025-07-14T15:00:00"
  }
]
```

## Notes

- Only the collection owner can view entries.
- Entries are returned in descending order by `added_at` (newest first).
- All error cases are covered by unit and integration tests (see `test_api_collections_entry.py`).
- The route follows RESTful conventions and returns clear error messages for all failure modes.

# Get Collection Entry Details API Route

This section documents the `/collections/{collection_id}/entries/{entry_id}` endpoint for retrieving details of a specific entry in a collection.

## Endpoint

- **GET** `/collections/{collection_id}/entries/{entry_id}`

## Authentication

- Requires a valid JWT in the `Authorization` header (Bearer token).

## Path Parameters

- `collection_id` (integer, required): The unique ID of the collection.
- `entry_id` (integer, required): The unique ID of the entry within the collection.

## Responses

- **200 OK**: Returns the collection entry object.
- **401 Unauthorized**: Missing or invalid JWT.
- **403 Forbidden**: User does not own the collection.
- **404 Not Found**: Entry does not exist, or does not belong to the specified collection.
- **422 Unprocessable Entity**: Invalid path parameter format (e.g., non-integer).
- **500 Internal Server Error**: Unexpected server error.

### Success Response Example

```json
{
  "id": 1,
  "collection_id": 1,
  "game_id": 12345,
  "notes": "My favorite RPG!",
  "status": "playing",
  "rating": 10,
  "custom_tags": { "favorite": true, "genre": "RPG" },
  "added_at": "2025-07-15T18:00:00"
}
```

## Notes

- Only the collection owner can view entry details.
- Entry must belong to the specified collection.
- All error cases are covered by unit and integration tests (see test_api_collections_entry.py).
- The route follows RESTful conventions and returns clear error messages for all failure modes.

# Update Collection Entry API Route

This section documents the `/collections/{collection_id}/entries/{entry_id}` endpoint for updating a game entry in a collection in the Game Service API.

## Endpoint

- **PUT** `/collections/{collection_id}/entries/{entry_id}`

## Authentication

- Requires a valid JWT in the `Authorization` header (Bearer token).

## Path Parameters

- `collection_id` (integer, required): The unique ID of the collection containing the entry.
- `entry_id` (integer, required): The unique ID of the entry to update.

## Request Body

- Content-Type: `application/json`
- All fields are optional; only provided fields will be updated.
  - `notes` (string or null, optional): User notes about the game.
  - `status` (string or null, optional): Status (e.g., "playing", "completed").
  - `rating` (integer or null, optional): User rating for the game.
  - `custom_tags` (object or null, optional): Custom tags as key-value pairs.

### Example

```json
{
  "notes": "Updated notes",
  "status": "completed",
  "rating": 9,
  "custom_tags": { "favorite": true }
}
```

## Validation Rules

- Only the owner of the collection can update entries.
- Fields not included in the request body remain unchanged.
- Setting a field to `null` will clear its value.
- Entry must belong to the specified collection.

## Responses

- **200 OK**: Entry updated successfully. Returns the updated collection entry object.
- **401 Unauthorized**: Missing or invalid JWT.
- **403 Forbidden**: User does not own the collection or entry.
- **404 Not Found**: Collection or entry does not exist.
- **422 Unprocessable Entity**: Validation errors (invalid path or body format).
- **500 Internal Server Error**: Unexpected server error.

### Success Response Example

```json
{
  "id": 1,
  "collection_id": 1,
  "game_id": 12345,
  "notes": "Updated notes",
  "status": "completed",
  "rating": 9,
  "custom_tags": { "favorite": true },
  "added_at": "2025-07-15T18:00:00",
  "updated_at": "2025-07-15T18:10:00"
}
```

### Error Response Examples

```json
{ "detail": "Missing or invalid Authorization header" }
{ "detail": "Permission denied" }
{ "detail": "Collection not found" }
{ "detail": "Entry not found" }
```

## Notes

- Only the collection owner can update entries.
- All error cases are covered by unit and integration tests (see `test_api_collections_entry.py`).
- The route follows RESTful conventions and returns clear error messages for all failure modes.

# Delete Collection Entry API Route

This section documents the `/collections/{collection_id}/entries/{entry_id}` endpoint for deleting a game entry from a collection in the Game Service API.

## Endpoint

- **DELETE** `/collections/{collection_id}/entries/{entry_id}`

## Authentication

- Requires a valid JWT in the `Authorization` header (Bearer token).

## Path Parameters

- `collection_id` (integer, required): The unique ID of the collection containing the entry.
- `entry_id` (integer, required): The unique ID of the entry to delete.

## Responses

- **204 No Content**: Entry deleted successfully. No response body.
- **401 Unauthorized**: Missing or invalid JWT.
- **403 Forbidden**: User does not own the collection or entry.
- **404 Not Found**: Collection or entry does not exist.
- **422 Unprocessable Entity**: Invalid path parameter format (e.g., non-integer).
- **500 Internal Server Error**: Unexpected server error.

### Error Response Examples

```json
{ "detail": "Missing or invalid Authorization header" }
{ "detail": "Permission denied" }
{ "detail": "Collection not found" }
{ "detail": "Entry not found" }
```

## Notes

- Only the collection owner can delete entries.
- All error cases are covered by unit and integration tests (see `test_api_collections_entry.py`).
- The route follows RESTful conventions and returns clear error messages for all failure modes.
