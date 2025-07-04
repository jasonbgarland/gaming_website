# ...existing code...
"""
SQLAlchemy models package for the gaming library database.
Contains User, Game, Collection, and CollectionEntry models.
"""
# Only import Base for Alembic; avoid unused imports for flake8
from .user import Base  # noqa: F401
