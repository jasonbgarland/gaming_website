# Project Instructions

- Do not commit without permission — show staged changes and wait for go-ahead
- Working docs and temporary AI plans go in `.ai/` (gitignored)
- Update `.ai/HANDOFF.md` after completing tasks and before ending a session — see `handoff` skill
- I want to learn — provide explanations, break solutions into steps, confirm before proceeding

## Workflow

- Checklist-driven: maintain `PROJECT_PLAN.md` (high-level) and `TASK_PLAN.md` (session-level), work top to bottom
- Modified TDD workflow — see `modified-tdd` skill for full process. Summary: define acceptance criteria → write test suite first (drives interface design) → implement → run full suite → refactor review → document

## Python

- Use `unittest` (not pytest); run with `PYTHONPATH=../..` from service directory
- No `__all__` in `__init__.py` files; prefer explicit imports
- SQLite test isolation: each test class creates its own in-memory engine/session in setUp/tearDown
- Assert order: `assertEqual(expected, actual)`

## Frontend (Next.js)

- Tests in `__tests__/` folders inside feature directories, not colocated with components
- Jest + React Testing Library, TypeScript for everything
