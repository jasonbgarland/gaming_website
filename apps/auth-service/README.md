# Auth Service

This service provides authentication for the Gaming Library project, including user signup, login (with JWT), and a protected `/me` endpoint.

## Features

- FastAPI-based microservice
- JWT authentication (production-ready)
- Signup, login, and `/me` endpoints
- Password hashing with Passlib (bcrypt)
- SQLAlchemy/PostgreSQL integration
- Comprehensive unit tests for all endpoints and edge cases

## API Endpoints

### `POST /signup`

Create a new user account.

**Request:**

```json
{
  "username": "testuser",
  "email": "testuser@example.com",
  "password": "StrongPassword123"
}
```

**Response (201):**

```json
{
  "username": "testuser",
  "email": "testuser@example.com"
}
```

**Error (409):** Username or email already exists.

### `POST /login`

Authenticate and receive a JWT access token.

**Request:**

```json
{
  "username": "testuser",
  "password": "StrongPassword123"
}
```

**Response (200):**

```json
{
  "access_token": "<JWT>",
  "token_type": "bearer"
}
```

**Error (401):** Invalid username or password.

### `GET /me`

Get info about the authenticated user. Requires `Authorization: Bearer <token>` header.

**Response (200):**

```json
{
  "username": "testuser",
  "email": "testuser@example.com"
}
```

**Error (401/403/404):** Invalid, missing, expired, or tampered token; user not found.

### `GET /health`

Health check endpoint. Returns `{ "status": "ok" }` if the service is running.

## JWT Usage

- On successful login, use the returned `access_token` as a Bearer token in the `Authorization` header for protected endpoints (e.g., `/me`).
- Tokens expire after 30 minutes by default. Expired or tampered tokens will result in a 401 error.

## Error Handling

- All endpoints return clear error messages and appropriate HTTP status codes for invalid input, authentication failures, and edge cases.
- Example error response:

```json
{
  "detail": "Token has expired"
}
```

## Environment Variables

- `JWT_SECRET_KEY`: Secret key for signing JWTs (**required**, set in `.env`)
- `DATABASE_URL`: SQLAlchemy database URL (**required**)
- `ACCESS_TOKEN_EXPIRE_MINUTES`: (optional) JWT token lifetime in minutes. Defaults to 30 if not set. Increase or decrease to control how long login sessions last.

## Development

### Run Locally

```bash
uvicorn src.main:app --reload
```

### Run Tests

```bash
PYTHONPATH=../.. poetry run python -m unittest discover -s tests
```

### Linting & Formatting

- This service uses [pre-commit](https://pre-commit.com/) hooks for linting and formatting.
- Hooks run Black, Flake8, and Pylint for both DB and auth-service code, using the correct Poetry environment for each.
- To run manually:
  ```sh
  poetry run pre-commit run --all-files
  ```

See the root README for more details on monorepo structure and development workflow.

## Structure

- `src/api/` - Route handlers
- `src/core/` - Auth logic, security utilities
- `src/models/` - Database models
- `src/schemas/` - Pydantic schemas
- `src/main.py` - FastAPI app entrypoint
- `tests/` - Unit and integration tests (shared in-memory SQLite for speed)

## Security Notes

- Passwords are hashed using bcrypt before storage.
- JWTs are signed with a strong secret and have a short expiration.
- All user input is validated with Pydantic.

## TODO / Future Enhancements

- Rate limiting or brute-force protection for login endpoint
- Add refresh token support for longer sessions
- Add email verification or password reset endpoints
- Centralized error response model for consistent API errors
- Production deployment scripts or Docker Compose improvements
- CI/CD pipeline for automated testing and linting

---

> The auth-service currently imports database models from the shared `db` package using PYTHONPATH for local development. For production deployment, package the `db` models as a Python package and install it as a dependency in each service that requires it.
