"""
User model definition for the gaming library database.

Defines the User class and its relationships.
"""

from sqlalchemy import Column, Integer, String, DateTime, func
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class User(Base):
    """
    SQLAlchemy model for a user in the gaming library.
    Represents a registered user with collections and games.
    """

    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    username = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),  # pylint: disable=not-callable
        nullable=False,
    )
    is_active = Column(
        Integer, default=1, nullable=False
    )  # 1 for active, 0 for inactive

    def __repr__(self) -> str:
        """String representation for debugging purposes."""
        return f"<User(id={self.id}, email={self.email}, username={self.username})>"
