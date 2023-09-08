"""add foreign-key to posts table

Revision ID: 3c6a30ed10b5
Revises: 6c3a33ae9ff6
Create Date: 2023-09-07 12:08:00.824752

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '3c6a30ed10b5'
down_revision: Union[str, None] = '6c3a33ae9ff6'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column("posts", sa.Column("user_id", sa.Integer(), nullable=False))
    op.create_foreign_key("posts_users_fk", source_table="posts",
                        referent_table="users", local_cols=["user_id"],
                        remote_cols=["id"], ondelete="CASCADE")
    pass


def downgrade() -> None:
    op.drop_constraint("posts_users_fk", table_name="posts")
    op.drop_column("posts", "user_id")
    pass
