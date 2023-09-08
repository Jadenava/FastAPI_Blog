"""create posts table

Revision ID: 9cc76d0a5138
Revises: 
Create Date: 2023-09-06 21:18:31.313365

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '9cc76d0a5138'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table("posts", sa.Column("id", sa.Integer, nullable=False, primary_key=True), sa.Column("title", sa.String, nullable=False))
    pass


def downgrade() -> None:
    op.drop_table("posts")
    pass
