"""Add user table

Revision ID: 6c3a33ae9ff6
Revises: 5e58f2894860
Create Date: 2023-09-07 11:24:43.717036

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '6c3a33ae9ff6'
down_revision: Union[str, None] = '5e58f2894860'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table("users",
                    sa.Column("id", sa.Integer(), nullable=False), 
                    sa.Column("email", sa.String(), nullable=False),
                    sa.Column("password", sa.String(), nullable=False),
                    sa.Column("created_at", sa.TIMESTAMP(timezone=True),server_default=sa.text("now()"), nullable=False), 
                    sa.PrimaryKeyConstraint("id"), 
                    sa.UniqueConstraint("email")
                    )


    pass


def downgrade() -> None:
    op.drop_table("users")
    pass
