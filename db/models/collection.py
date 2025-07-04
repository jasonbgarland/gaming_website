"""
Collection and CollectionEntry model definitions for the gaming library database.

Defines the Collection and CollectionEntry classes and their relationships.
"""

from sqlalchemy import (
    Column,
    Integer,
    String,
    DateTime,
    ForeignKey,
    Text,
    UniqueConstraint,
    func,
)
from sqlalchemy.orm import relationship
from .user import Base


class Collection(Base):
    """
    SQLAlchemy model for a user's collection of games.
    Represents a collection owned by a user, containing multiple games.
    """

    __tablename__ = "collections"

    id: int = Column(Integer, primary_key=True)
    user_id: int = Column(
        Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True
    )
    name: str = Column(String, nullable=False)
    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,  # pylint: disable=not-callable
    )
    updated_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),  # pylint: disable=not-callable
        onupdate=func.now(),  # pylint: disable=not-callable
        nullable=False,
    )

    __table_args__ = (
        UniqueConstraint("user_id", "name", name="uq_user_collection_name"),
    )

    entries = relationship(
        "CollectionEntry", back_populates="collection", cascade="all, delete-orphan"
    )

    def __repr__(self) -> str:
        """String representation for debugging purposes."""
        return f"<Collection(id={self.id}, user_id={self.user_id}, name={self.name})>"


class CollectionEntry(Base):
    """
    SQLAlchemy model for an entry in a collection.
    Represents the association between a collection and a game.
    """

    __tablename__ = "collection_entries"

    id: int = Column(Integer, primary_key=True)
    collection_id: int = Column(
        Integer,
        ForeignKey("collections.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    game_id: int = Column(
        Integer, ForeignKey("games.id", ondelete="CASCADE"), nullable=False, index=True
    )
    status: str = Column(String, nullable=True)  # e.g., 'playing', 'completed'
    rating: int = Column(Integer, nullable=True)  # 1-10
    notes: str = Column(Text, nullable=True)
    added_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,  # pylint: disable=not-callable
    )
    updated_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),  # pylint: disable=not-callable
        onupdate=func.now(),  # pylint: disable=not-callable
        nullable=False,
    )

    __table_args__ = (
        UniqueConstraint("collection_id", "game_id", name="uq_collection_game"),
    )

    collection = relationship("Collection", back_populates="entries")

    def __repr__(self) -> str:
        return f"<CollectionEntry(id={self.id}, collection_id={self.collection_id}, game_id={self.game_id})>"
