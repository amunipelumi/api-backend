"""add foreign key to posts table

Revision ID: b631e002789f
Revises: 7a190769c737
Create Date: 2024-05-08 10:29:51.169864

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'b631e002789f'
down_revision: Union[str, None] = '7a190769c737'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('posts', sa.Column('owner_id', sa.Integer(), nullable=False))
    op.create_foreign_key('post_user_fk', 
                          source_table='posts', 
                          referent_table='users', 
                          local_cols=['owner_id'],
                          remote_cols=['id'],
                          ondelete='CASCADE')
    pass


def downgrade() -> None:
    op.drop_constraint('post_user_fk', table_name='posts')
    op.drop_column('posts', column_name='owner_id')
    pass
