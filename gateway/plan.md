# 🚪 FastAPI Gateway Feature Roadmap (with Testing in Every Phase)

This roadmap outlines the iterative development of a custom API Gateway using FastAPI. Each phase includes essential features and corresponding tests to ensure reliability as the project grows.

---

## ✅ Phase 1: MVP – Routing & Authentication

### Features

- [ ] Project scaffolding (`gateway/`, `main.py`)
- [ ] Install dependencies: `fastapi`, `uvicorn`, `httpx`, `python-dotenv`
- [ ] Basic reverse proxy routing:
  - `/api/auth` → `auth_service`
  - `/api/games` → `game_service`
  - `/api/library` → `library-service`
- [ ] JWT authentication middleware:
  - Extract and validate JWT from `Authorization` header
  - Inject user info into headers for downstream services
- [ ] CORS middleware
- [ ] Load config from `.env` using `pydantic.BaseSettings`

### Testing

- [ ] Unit test JWT validation logic
- [ ] Integration test for routing to each backend service
- [ ] Test 401 response for missing/invalid tokens
- [ ] Test CORS headers on responses

---

## 🔧 Phase 2: Developer Experience & Observability

### Features

- [ ] Logging middleware:
  - Log method, path, status code, and response time
  - Generate unique request IDs
- [ ] `/health` endpoint:
  - Ping each downstream service and return status
- [ ] Centralized error handling:
  - Catch and format downstream errors
  - Return consistent error structure

### Testing

- [ ] Test `/health` endpoint with mock service responses
- [ ] Test logging output (optional: use log capture)
- [ ] Test error formatting for 4xx and 5xx responses

---

## 🚦 Phase 3: Resilience & Performance

### Features

- [ ] Rate limiting:
  - Use Redis or in-memory store
  - Limit requests per IP or user
- [ ] Retry logic:
  - Retry failed requests (e.g., 502, 504) with exponential backoff
- [ ] Timeout handling:
  - Set timeouts for downstream requests
  - Return 504 Gateway Timeout on failure

### Testing

- [ ] Test rate limit enforcement (429 response)
- [ ] Test retry behavior with simulated failures
- [ ] Test timeout handling with delayed downstream responses

---

## 🔐 Phase 4: Advanced Security

### Features

- [ ] Token introspection or revocation support
- [ ] Role-based access control (RBAC):
  - Define route-level permissions
  - Return 403 Forbidden for unauthorized roles

### Testing

- [ ] Test revoked/expired token handling
- [ ] Test RBAC enforcement for protected routes

---

## 🧪 Continuous Testing & Quality

Throughout all phases:

- [ ] Use `pytest` for unit and integration tests
- [ ] Use `httpx.AsyncClient` for async test client
- [ ] Add `mypy`, `ruff`, and `black` for type checking and linting
- [ ] (Optional) Add pre-commit hooks for formatting and safety

---

## 🧭 Summary

| Phase | Focus         | Key Features                             | Testing Highlights                       |
| ----- | ------------- | ---------------------------------------- | ---------------------------------------- |
| 1     | MVP           | Routing, JWT auth, CORS                  | Auth logic, route proxying, CORS headers |
| 2     | Observability | Logging, health checks, error formatting | Health checks, error structure           |
| 3     | Resilience    | Rate limiting, retries, timeouts         | 429s, retry logic, timeout behavior      |
| 4     | Security      | Token revocation, RBAC                   | Role enforcement, token edge cases       |

This structure ensures you always have a working, testable gateway while layering in complexity and robustness over time.
