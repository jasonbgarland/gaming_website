# Game Data Service (IGDB)

This microservice provides a FastAPI-based interface to the IGDB API, handling authentication, game search, and other game data queries for the gaming library application.

## Structure

- `src/main.py`: FastAPI app entrypoint
- `src/api/igdb.py`: API routes for IGDB endpoints
- `src/igdb/client.py`: IGDB API wrapper class
- `src/igdb/auth.py`: IGDB OAuth/token logic
- `src/igdb/schemas.py`: Pydantic models for IGDB requests/responses
- `src/core/config.py`: Configuration loader
- `tests/`: Unit tests

## Setup

1. Install dependencies:
   ```sh
   poetry install
   ```
2. Set environment variables for IGDB credentials in your `.env` file:
   ```env
   IGDB_CLIENT_ID=your_client_id
   IGDB_CLIENT_SECRET=your_client_secret
   ```
3. Run the service:
   ```sh
   poetry run uvicorn src.main:app --reload
   ```


## Caching

This service implements in-memory caching for all IGDB API client methods to improve performance and reduce redundant external API calls. Caching is applied to:

- **Game lookups by ID**: Each game is cached individually for 5 minutes.
- **Batch game lookups**: Each requested game is cached by ID; only missing games are fetched from IGDB.
- **Game search queries**: Search results are cached by query string for 5 minutes.
- **Genres and platforms**: The full list of genres and platforms is cached for 24 hours.

The cache is thread-safe and supports TTL (time-to-live) expiration. All caching logic is unit tested for correctness and performance.

**Note:** For production deployments, it is recommended to use a distributed cache such as Redis. The code is structured to allow easy replacement of the in-memory cache with a Redis backend in the future.

## Usage

### Endpoints

- `GET /igdb/search?q=...` — Search for games by name
- `GET /igdb/games/{id}` — Get details for a specific game
- `GET /igdb/games?ids=1,2,3` — Batch fetch game details
- `GET /igdb/genres` — List all genres
- `GET /igdb/platforms` — List all platforms

### Example Requests

**Search for games:**

```sh
curl 'http://localhost:8000/igdb/search?q=zelda'
```

**Get game by ID:**

```sh
curl 'http://localhost:8000/igdb/games/1020'
```

**Batch fetch games:**

```sh
curl 'http://localhost:8000/igdb/games?ids=1020,7346'
```

**List genres:**

```sh
curl 'http://localhost:8000/igdb/genres'
```

**List platforms:**

```sh
curl 'http://localhost:8000/igdb/platforms'
```

### Environment Variables

- `IGDB_CLIENT_ID`: Your IGDB API client ID
- `IGDB_CLIENT_SECRET`: Your IGDB API client secret


## TODO / Follow-on Work

- **Consider using Redis for caching**: The current implementation uses an in-memory cache for IGDB queries. For production, consider switching to a Redis server to enable distributed caching and persistence.

---

### Testing

Run all unit and integration tests:

```sh
poetry run python -m unittest discover -s tests
```

To run integration tests against the real IGDB API, set environment variables:

```sh
export RUN_IGDB_INTEGRATION=1
export IGDB_CLIENT_ID=your_client_id
export IGDB_CLIENT_SECRET=your_client_secret
poetry run python -m unittest discover -s tests
```
