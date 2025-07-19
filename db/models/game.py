"""
Game model definition for the gaming library database.

Defines the Game class and its relationships.
"""

from sqlalchemy import Column, Date, Integer, String, UniqueConstraint

from .user import Base


class Game(Base):
    """
    SQLAlchemy model for a game in the gaming library.
    Represents a game that can be added to collections.
    """

    __tablename__ = "games"

    id = Column(Integer, primary_key=True, index=True)
    igdb_id = Column(Integer, unique=True, nullable=True)
    name = Column(String, nullable=False, index=True)
    platform = Column(String, nullable=False, index=True)
    release_date = Column(Date, nullable=True)
    cover_url = Column(String, nullable=True)
    genre = Column(String, nullable=True)  # Comma-separated list of genres

    __table_args__ = (UniqueConstraint("name", "platform", name="uq_name_platform"),)

    def __repr__(self) -> str:
        """String representation for debugging purposes."""
        return f"<Game(id={self.id}, name={self.name}, platform={self.platform})>"
