"""create post table

Revision ID: fd2516a815da
Revises: 
Create Date: 2026-10-31 20:44:40.304323

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy import Column, Integer
from app import model


# revision identifiers, used by Alembic.
revision: str = 'fd2516a815da'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "posts_test",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("title", sa.String(), nullable=False),
        sa.Column("content", sa.String(), nullable=False),
    )  
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
