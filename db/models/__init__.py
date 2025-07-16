"""
SQLAlchemy models package for the gaming library database.
Contains User, Game, Collection, and CollectionEntry models.
"""

# Import all models so Alembic can discover all tables
from .user import Base, User  # noqa: F401
from .game import Game  # noqa: F401
from .collection import Collection, CollectionEntry  # noqa: F401
