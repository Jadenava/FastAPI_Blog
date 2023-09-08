"""add content column to posts table

Revision ID: 5e58f2894860
Revises: 9cc76d0a5138
Create Date: 2023-09-06 21:41:14.195973

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '5e58f2894860'
down_revision: Union[str, None] = '9cc76d0a5138'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column("posts", sa.Column("content", sa.String, nullable=False))
    pass


def downgrade() -> None:
    op.drop_column("posts", "content")
    pass
