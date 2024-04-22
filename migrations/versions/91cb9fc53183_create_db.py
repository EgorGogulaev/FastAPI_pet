"""create db

Revision ID: 91cb9fc53183
Revises: 
Create Date: 2024-04-14 11:47:23.544684

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '91cb9fc53183'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('operations',
    sa.Column('id', sa.BigInteger(), nullable=False),
    sa.Column('quantity', sa.String(), nullable=True),
    sa.Column('figi', sa.String(), nullable=True),
    sa.Column('instrument_type', sa.String(), nullable=False),
    sa.Column('type', sa.String(), nullable=True),
    sa.Column('operation_datetime', sa.DateTime(), nullable=True),
    sa.Column('create_at', sa.DateTime(), server_default=sa.text('now()'), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.add_column('user', sa.Column('role_id', sa.SmallInteger(), nullable=True))
    op.create_foreign_key(None, 'user', 'role', ['role_id'], ['id'], onupdate='CASCADE', ondelete='CASCADE')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'user', type_='foreignkey')
    op.drop_column('user', 'role_id')
    op.drop_table('operations')
    # ### end Alembic commands ###
