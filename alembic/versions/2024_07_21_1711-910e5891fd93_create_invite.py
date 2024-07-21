"""create invite

Revision ID: 910e5891fd93
Revises: 7c8a8972793e
Create Date: 2024-07-21 17:11:11.512406

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '910e5891fd93'
down_revision: Union[str, None] = '7c8a8972793e'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('invite',
    sa.Column('id', sa.UUID(), nullable=False),
    sa.Column('token', sa.Integer(), nullable=False),
    sa.Column('account_id', sa.UUID(), nullable=False),
    sa.ForeignKeyConstraint(['account_id'], ['account.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('invite')
    # ### end Alembic commands ###
