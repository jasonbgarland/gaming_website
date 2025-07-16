# Copilot Instructions

## Code Style & Preferences

### Important General Guidelines

- I want to learn and improve my skills and knowledge, so please provide explanations for your suggestions
- Always break down solutions into steps and confirm before proceeding
- Follow test driven development (TDD) principles as much as possible
  - Write a failing test first with expectations on how we would like to call the code.
  - Run the test to confirm it fails.
  - Write the minimum code to make the test pass.
  - Run the test to confirm it passes.
  - Perform any refactoring and confirm the test still passes.
  - Verify feature is documented appropriately and pylint is passing before continuing to next step.
- Use vs code tasks when possible to get repeatable results.
- Prefer iterative solutions, start small and iterate
- Write comments for complex logic

## Checklist-Driven Workflow

- For every project, create a `PROJECT_PLAN.md` with a high-level checklist of all major tasks/milestones.
- For each work session or major task, create or update a `TASK_PLAN.md` with a sequential checklist of atomic steps.
- Always work from top to bottom in the checklist, checking off items as you go.
- Use these files to track progress and make it easy to pause/resume work at any time.
- Update the checklists as tasks are completed or requirements change.

### Language-Specific Preferences

#### Python

- Follow PEP 8 style guidelines
- Use type hints for function parameters and return values
- Create docstrings for all public functions and classes
- Prefer f-strings for string formatting
- Use descriptive variable names (avoid abbreviations)
- Use xUnit style tests using the built in `unittest` module
- Do not use the `__all__` pattern in `__init__.py` files; importing \* is not a preferred pattern in this project

## Architecture & Patterns

- Prefer composition over inheritance
- Use dependency injection where appropriate
- Follow SOLID principles

## File Organization

- Group related files in appropriate directories
- Use consistent naming conventions for files and folders
- Keep configuration files in the root or a dedicated config directory
- Separate source code from tests and documentation

## Testing Preferences

- Write unit tests for new functions and classes
- Use descriptive test names that explain what is being tested
- Include both positive and negative test cases
- Mock external dependencies in tests
- When asserting equality, the first parameter should be the expected value, and the second should be the actual value

## Documentation

- Include README files for each major component
- Document public APIs and interfaces
- Explain complex algorithms or business logic
- Keep documentation up to date with code changes

## Specific Instructions for Copilot

### When Suggesting Code:

- Suggest meaningful variable names based on context
- Optimize for readability over cleverness

### When Refactoring:

- Maintain existing functionality
- Improve code organization and clarity
- Add missing error handling
- Update documentation if needed
- Suggest breaking changes only when significantly beneficial

### For New Features:

- Start with a clear interface or API design
- Include appropriate logging, especially for debugging purposes.
- Add configuration options where useful

### Technologies I Use:

- Frontend: React
- Backend: Python
- Databases: PostgreSQL, MongoDB, Redis
- Cloud Platforms: Azure
- Development Tools: Docker, CI/CD tools

- Validation: pydantic

## Security Considerations

- Always validate user input
- Don't commit secrets or API keys
- Always validate user input
- Don't commit secrets or API keys

## Project Considerations

### SQLite Testing Best Practice

> **Note:** In-memory SQLite databases (`sqlite:///:memory:`) are per connection.  
> For reliable test isolation, each test class (or test) should create its own engine and schema.

**How to do this:**

- In your test class, use `setUp()` to create a new engine, schema, and session for each test.
- Use `tearDown()` to close the session and dispose the engine.
- Do not share the engine or session across multiple tests.

**Example:**

```python
def setUp(self):
    self.engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(self.engine)
    self.SessionLocal = sessionmaker(bind=self.engine)
    self.db = self.SessionLocal()
    self.service = CollectionService()

def tearDown(self):
    self.db.close()
    self.engine.dispose()
```
