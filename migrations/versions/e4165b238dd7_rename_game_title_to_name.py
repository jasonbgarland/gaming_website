"""rename_game_title_to_name

Revision ID: e4165b238dd7
Revises: 8ab933b33b7f
Create Date: 2025-07-19 14:11:37.294371

"""

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = "e4165b238dd7"
down_revision: Union[str, Sequence[str], None] = "8ab933b33b7f"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###

    # First, add the new column as nullable
    op.add_column("games", sa.Column("name", sa.String(), nullable=True))

    # Copy data from title to name
    op.execute("UPDATE games SET name = title WHERE title IS NOT NULL")

    # Now make the column non-nullable
    op.alter_column("games", "name", nullable=False)

    # Drop old constraints and indexes
    op.drop_index(op.f("ix_games_title"), table_name="games")
    op.drop_constraint(op.f("uq_title_platform"), "games", type_="unique")

    # Create new constraints and indexes
    op.create_index(op.f("ix_games_name"), "games", ["name"], unique=False)
    op.create_unique_constraint("uq_name_platform", "games", ["name", "platform"])

    # Finally, drop the old column
    op.drop_column("games", "title")
    # ### end Alembic commands ###


def downgrade() -> None:
    """Downgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###

    # Add the old column as nullable
    op.add_column(
        "games", sa.Column("title", sa.VARCHAR(), autoincrement=False, nullable=True)
    )

    # Copy data from name to title
    op.execute("UPDATE games SET title = name WHERE name IS NOT NULL")

    # Make title non-nullable
    op.alter_column("games", "title", nullable=False)

    # Drop new constraints and indexes
    op.drop_constraint("uq_name_platform", "games", type_="unique")
    op.drop_index(op.f("ix_games_name"), table_name="games")

    # Create old constraints and indexes
    op.create_unique_constraint(
        op.f("uq_title_platform"),
        "games",
        ["title", "platform"],
        postgresql_nulls_not_distinct=False,
    )
    op.create_index(op.f("ix_games_title"), "games", ["title"], unique=False)

    # Drop the new column
    op.drop_column("games", "name")
    # ### end Alembic commands ###
