# Copilot Instructions

## General

- Explain suggestions so I can learn; break solutions into steps and confirm before proceeding.
- Prefer iterative solutions; start small and iterate.
- Use VS Code tasks for repeatable operations.
- For new features: start with interface/API design, include logging for debugging.

## Agent Delegation

- After making any code changes, always delegate test verification to the `test-runner` agent.
- When tests are failing and need to be fixed, delegate to the `fix-failures` agent.
- When fixing lint findings, delegate to the `lint-and-fix` agent.
- Do not run tests or linting directly — use the specialist agents so results stay compact.

## Workflow

- Maintain `PROJECT_PLAN.md` (high-level milestones) and `TASK_PLAN.md` (session-level atomic steps). Work top to bottom, check off as you go.
- Follow TDD: write failing test → confirm it fails → implement → confirm it passes → refactor → confirm still passes → verify docs and pylint are clean before moving on.

## Python

- Use `unittest` (not pytest); xUnit style.
- No `__all__` in `__init__.py`; prefer explicit imports.
- Assert order: `assertEqual(expected, actual)`.
- Validation: pydantic.

### SQLite Test Isolation

In-memory SQLite (`sqlite:///:memory:`) is per-connection. Each test class must create its own engine/session in `setUp` and tear it down in `tearDown`:

```python
def setUp(self):
    self.engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(self.engine)
    self.SessionLocal = sessionmaker(bind=self.engine)
    self.db = self.SessionLocal()

def tearDown(self):
    self.db.close()
    self.engine.dispose()
```

## Frontend (Next.js)

- Tests in `__tests__/` inside each feature directory — not colocated with components.
- Jest + React Testing Library; TypeScript for all components and tests.

## Tech Stack

- Frontend: React / Next.js — Backend: Python — Validation: pydantic
- Databases: PostgreSQL, MongoDB, Redis — Cloud: Azure — Tooling: Docker, CI/CD

## Security

- Always validate user input; never commit secrets or API keys.
