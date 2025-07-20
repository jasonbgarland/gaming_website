# Gaming Library Monorepo

This repository contains all services and shared code for the Gaming Library project - a microservice-based gaming collection management platform.

## Monorepo Structure

- `apps/auth_service/` — FastAPI microservice for authentication (signup, login, JWT, user info)
- `apps/game_service/` — FastAPI microservice for game data (IGDB integration, search, collections)
- `apps/frontend/` — Next.js React frontend application
- `db/` — Shared SQLAlchemy models and DB migrations
- `shared/` — Shared utilities (JWT utils, etc.) used across services
- `gateway/` — (Planned) API gateway and orchestration
- `migrations/` — Alembic migration scripts
- `docker-compose.yml` — Docker Compose configuration for all services
- `.pre-commit-config.yaml` — Linting and formatting hooks for all Python code

## Quick Start with Docker Compose

### 1. Clone and Set Up Environment

```sh
git clone <repo-url>
cd gaming_website
cp .env.example .env
# Fill in required environment variables (see .env.example for details)
```

### 2. Run All Services with Docker Compose

```sh
# Build and start all services (PostgreSQL, auth service, game service, frontend)
docker-compose up --build

# Or run in detached mode
docker-compose up -d --build
```

This will start:

- **PostgreSQL Database** on port 5432
- **Auth Service** on port 8000
- **Game Service** on port 8001
- **Frontend** on port 3000

### 3. Access the Application

- **Frontend**: http://localhost:3000
- **Auth Service API**: http://localhost:8000/docs (Swagger UI)
- **Game Service API**: http://localhost:8001/docs (Swagger UI)

## Development Setup (Local)

For local development without Docker:

### 1. Install Dependencies

```sh
# Install root dependencies
poetry install

# Install service-specific dependencies
cd apps/auth_service && poetry install && cd ../..
cd apps/game_service && poetry install && cd ../..
cd apps/frontend && npm install && cd ../..
```

### 2. Set Up Database

```sh
# Run database migrations
poetry run alembic upgrade head
```

### 3. Run Services Individually

- **Auth Service**: See `apps/auth_service/README.md`
- **Game Service**: See `apps/game_service/README.md`
- **Frontend**: See `apps/frontend/README.md`

### 4. Run Tests

Use VS Code tasks for comprehensive testing:

- **All Services**: Run the "All Checks" task in VS Code
- **Individual Services**:
  - **DB models**: `poetry run python -m unittest discover -s db/tests`
  - **Auth service**: `cd apps/auth_service && PYTHONPATH=../.. poetry run python -m unittest discover -s tests`
  - **Game service**: `cd apps/game_service && poetry run python -m unittest discover -s tests`
  - **Frontend**: `cd apps/frontend && npm test`

### 5. Linting & Formatting

- Pre-commit hooks run Black, Flake8, and Pylint for Python code.
- Use VS Code tasks for linting individual services.
- To run manually:
  ```sh
  poetry run pre-commit run --all-files
  ```

## Architecture Overview

This is a microservice architecture with:

- **Frontend (Next.js)**: User interface and client-side logic
- **Auth Service (FastAPI)**: User authentication, JWT tokens, user management
- **Game Service (FastAPI)**: IGDB integration, game search, collections management
- **Shared Database (PostgreSQL)**: Centralized data storage
- **Shared Code**: JWT utilities, database models

Services communicate via HTTP APIs and share a common database schema.

## Contributing

- Each service has its own README with specific development instructions
- Use pre-commit hooks before pushing code
- Follow the established patterns for new features
- Write tests following the TDD approach outlined in `.github/copilot-instructions.md`

## Future Roadmap

- API Gateway with request routing and rate limiting
- User game collections and wishlist features
- Social features (friends, recommendations)
- CI/CD pipeline with automated testing and deployment
- Kubernetes deployment configuration

---

For more details, see the README in each app folder.
