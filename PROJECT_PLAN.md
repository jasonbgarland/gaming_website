# 🎮 Gaming Library Microservices Project

A portfolio project to build a microservices-based web application for managing a personal video game library. Built with **Next.js** (frontend), **FastAPI** (backend), and **PostgreSQL** (database), using **IGDB.com** for game data.

---

## 🧱 Architecture & Infrastructure

- **API Gateway**

  - Routes frontend requests to appropriate microservices
  - Handles CORS, rate limiting, and authentication

- **Service Discovery / DNS**

  - Simple: Docker Compose hostnames
  - Advanced: Consul, Eureka, or Kubernetes DNS

- **Containerization & Orchestration**

  - Docker for each service
  - Kubernetes or ECS for scaling (optional for MVP)

- **Configuration Management**
  - Environment variables (12-factor app)
  - Secrets management (Vault, AWS Secrets Manager)

---

## 🧠 Backend Services

- **Auth Service**

  - JWT-based or OAuth2 authentication
  - Refresh-token flow and token revocation

- **User/Profile Service**

  - PostgreSQL schema migrations via Alembic
  - Profile endpoints, password hashing, email verification

- **Game Data Service**

  - IGDB API wrapper to abstract auth and rate limits
  - Caching layer (Redis) for frequent searches

- **Library Service**

  - CRUD operations on user’s game collections
  - Soft deletes, audit trail (optional)

- **Background Worker**
  - Celery or RQ for:
    - Periodic IGDB metadata sync
    - Sending notification emails

---

## 🗃️ Data & Caching

- **PostgreSQL**

  - Tables: users, games (local cache), collections, play sessions
  - Indexing for fast search and retrieval

- **Redis**
  - Cache for IGDB lookups
  - Optional: session storage

---

## 🎨 Frontend (Next.js)

- **State Management**

  - React Query or SWR for data fetching
  - Context or Redux for auth state

- **Routing & Auth Guards**

  - Next.js middleware for protected routes
  - Public vs. private route handling

- **Styling & Theming**
  - Tailwind CSS or styled-components
  - Dark mode toggle

---

## 🔐 Security & Compliance

- HTTPS with Let’s Encrypt
- Rate limiting per IP/user via API Gateway
- OWASP essentials: input validation, SQL injection protection, XSS
- Secure cookie flags: `HttpOnly`, `Secure`, `SameSite`

---

## 🧪 Testing Strategy

- Unit tests (pytest)
- Integration tests (FastAPI TestClient)
- End-to-end tests (Cypress or Playwright)
- Contract tests for service APIs

---

## ⚙️ CI/CD & DevOps

- **CI Pipeline**

  - Linting (flake8, ESLint), type checks (mypy, TypeScript)
  - Run tests, build Docker images

- **CD Pipeline**

  - Deploy to staging
  - Canary or blue/green deploys for production

- **Monitoring & Logging**
  - Centralized logs (Elastic Stack, Loki)
  - Metrics with Prometheus + Grafana
  - Health/readiness probes

---

## 📚 Documentation & Developer Experience

- Auto-generated OpenAPI docs (FastAPI)
- Postman or Hoppscotch collections
- README with setup steps and architecture diagram

---

## 🚀 Future Enhancements

- Social features: friend lists, game recommendations
- Real-time updates (WebSockets)
- Playtime tracking and statistics dashboards
- Mobile app companion (React Native or Expo)

---

## 🧭 Summary

This project demonstrates modern microservices architecture with a practical, engaging use case. It’s designed to grow over time, showcasing your skills in full-stack development, DevOps, and system design.

# 🎯 Task Breakdown

Below is a set of incremental tasks you can tackle locally. Start with core pieces (API, DB, Frontend), get an early demo running, then iterate. Adjust estimates to fit your schedule.

| ID  | ✓   | Component          | Task                                                                              | Dependencies   | Est. Time  |
| --- | --- | ------------------ | --------------------------------------------------------------------------------- | -------------- | ---------- |
| 1   | [x] | Repository         | Initialize Git repo, add README, install basic tooling                            | –              | 1–2 hours  |
| 2   | [x] | Database           | Spin up local PostgreSQL (Docker), create `games_lib` DB                          | Task 1         | 30 minutes |
| 3   | [x] | Database           | Define schemas & migrations: `users`, `games`, `collections` tables using Alembic | Task 2         | 1–2 hours  |
| 4   | [x] | Backend (Auth)     | Scaffold FastAPI service, install dependencies                                    | Task 1         | 30 minutes |
| 5   | [x] | Backend (Auth)     | Build signup/login endpoints (JWT-based)                                          | Tasks 3, 4     | 2–3 hours  |
| 6   | [x] | Backend (GameData) | Implement IGDB client wrapper with API key support                                | Tasks 4, 5     | 1–2 hours  |
| 7   | [x] | Backend (Library)  | CRUD endpoints for user’s game collection                                         | Tasks 3, 5     | 2–3 hours  |
| 8   | [x] | Frontend (Next.js) | Scaffold Next.js app, install Tailwind CSS                                        | Task 1         | 1 hour     |
| 9   | [x] | Frontend (UI)      | Build auth pages (signup/login) and state management                              | Tasks 5, 8     | 2–3 hours  |
| 10  | [x] | Frontend (UI)      | Build game search page, call IGDB wrapper via API Gateway                         | Tasks 6, 8     | 2–3 hours  |
| 11  | [ ] | Frontend (UI)      | Build “My Library” page, integrate add/remove calls                               | Tasks 7, 9, 10 | 2–3 hours  |
| 12  | [x] | Integration        | Wire up Next.js to FastAPI (CORS, proxy, env vars)                                | Tasks 5–11     | 1–2 hours  |
| 13  | [ ] | Demo & Validation  | Run local demo, manually test signup, search, add games                           | Tasks 1–12     | 1 hour     |
| 14  | [ ] | Polish & Commit    | Write README sections on setup and usage; push to GitHub                          | Task 13        | 1–2 hours  |

---

## 🎯 Post-MVP Enhancements

Once the core MVP is complete and demo-ready, these are valuable next steps to improve quality, reliability, and user experience:

### 🧪 Testing & Quality Assurance

| Priority | Task                                   | Estimated Effort | Benefits                                        |
| -------- | -------------------------------------- | ---------------- | ----------------------------------------------- |
| High     | **E2E Tests for Auth Flow**            | 2-3 hours        | Lock in working signup/login, catch regressions |
| High     | **Integration Tests for Game Service** | 2-3 hours        | Validate IGDB API integration, caching behavior |
| Medium   | **Component Unit Tests**               | 4-6 hours        | Faster feedback, easier refactoring             |
| Medium   | **API Contract Tests**                 | 2-3 hours        | Prevent breaking changes between services       |

### 🎨 User Experience Improvements

| Priority | Task                                | Estimated Effort | Benefits                                    |
| -------- | ----------------------------------- | ---------------- | ------------------------------------------- |
| High     | **Dashboard/Profile Page**          | 3-4 hours        | Better post-login experience than home page |
| High     | **Loading States & Error Handling** | 2-3 hours        | Professional feel, better user feedback     |
| Medium   | **Game Search Autocomplete**        | 2-3 hours        | Faster game discovery                       |
| Medium   | **Dark Mode Toggle**                | 1-2 hours        | Modern UI expectation                       |

### 🔧 Developer Experience

| Priority | Task                                 | Estimated Effort | Benefits                                |
| -------- | ------------------------------------ | ---------------- | --------------------------------------- |
| High     | **Docker Development Setup**         | 1-2 hours        | Consistent dev environment              |
| Medium   | **API Documentation**                | 1-2 hours        | Easier onboarding, external integration |
| Medium   | **VS Code Tasks for Common Actions** | 1 hour           | Streamlined workflow                    |

### 🚀 Performance & Scalability

| Priority | Task                               | Estimated Effort | Benefits                           |
| -------- | ---------------------------------- | ---------------- | ---------------------------------- |
| Medium   | **Redis Caching for IGDB**         | 2-3 hours        | Reduce API calls, faster responses |
| Low      | **Database Indexing Optimization** | 1-2 hours        | Faster queries as data grows       |
| Low      | **Image Optimization & CDN**       | 2-3 hours        | Faster page loads                  |

**Total High Priority Items**: ~12-16 hours of focused work
**Next Logical Sprint**: Focus on E2E tests + Dashboard page for a solid foundation

---

## Monorepo vs Multiple Repositories

Choosing between a monorepo (one repository) or polyrepo (multiple repositories) depends on trade-offs around complexity, collaboration, and deployment.

- Monorepo

  - Simplifies dependency management and versioning across services
  - One CI/CD pipeline, unified code reviews, and consistent tooling
  - Easier refactoring and cross-service changes
  - Can become unwieldy as the number of services grows

- Polyrepo
  - Clear service boundaries, smaller codebases per repo
  - Independent CI/CD pipelines and release cycles
  - Teams can work in isolation without stepping on each other
  - More overhead in coordinating versions, shared libraries, and cross-service changes
