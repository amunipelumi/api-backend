"""finalize posts table

Revision ID: e35eab6dd190
Revises: b631e002789f
Create Date: 2024-05-08 10:53:08.265772

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'e35eab6dd190'
down_revision: Union[str, None] = 'b631e002789f'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('posts', 
                  sa.Column('created_at', 
                            sa.TIMESTAMP(timezone=True), 
                            nullable=False, 
                            server_default=sa.text('now()'))
                  )
    pass


def downgrade() -> None:
    op.drop_column('posts', column_name='created_at')
    pass
