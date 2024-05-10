"""add new column to posts

Revision ID: 5e5221dd1549
Revises: 6b6aaf281149
Create Date: 2024-05-07 10:22:52.850849

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '5e5221dd1549'
down_revision: Union[str, None] = '6b6aaf281149'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column(
        'posts',
        sa.Column('published', sa.Boolean(), nullable=False, server_default='TRUE'),
        )
    pass


def downgrade() -> None:
    op.drop_column('posts', 'published')
    pass
