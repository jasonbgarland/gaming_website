# Gaming Library Monorepo

This repository contains all services and shared code for the Gaming Library project.

## Monorepo Structure

- `apps/auth_service/` — FastAPI microservice for authentication (signup, login, JWT, user info)
- `db/` — Shared SQLAlchemy models and DB migrations
- `gateway/` — (Planned) API gateway and orchestration
- `migrations/` — Alembic migration scripts
- `.pre-commit-config.yaml` — Linting and formatting hooks for all Python code

## Quick Start

### 1. Clone and Install

```sh
git clone <repo-url>
cd gaming_website
poetry install
```

### 2. Set Up Environment

- Copy `.env.example` to `.env` and fill in required secrets (see each service's README for details).

### 3. Run Services

- See `apps/auth_service/README.md` for running the auth service.

### 4. Run Tests

- **DB models:**
  ```sh
  poetry run python -m unittest discover -s db/tests
  ```
- **Auth service:**
  ```sh
  cd apps/auth_service
  PYTHONPATH=../.. poetry run python -m unittest discover -s tests
  ```

### 5. Linting & Formatting

- Pre-commit hooks run Black, Flake8, and Pylint for both DB and auth_service code.
- To run manually:
  ```sh
  poetry run pre-commit run --all-files
  ```

## Contributing

- Please see each service's README for details on development, testing, and API usage.
- Use pre-commit hooks before pushing code.

## Future

- More services (game catalog, user collections, gateway)
- CI/CD and deployment scripts

---

For more details, see the README in each app folder.
