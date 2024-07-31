"""create company

Revision ID: 0bd94f8298e2
Revises: 910e5891fd93
Create Date: 2024-07-22 22:39:16.361692

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '0bd94f8298e2'
down_revision: Union[str, None] = '910e5891fd93'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        'company',
        sa.Column('id', sa.UUID(), nullable=False),
        sa.Column('name', sa.String(length=50), nullable=False),
        sa.Column('description', sa.String(), nullable=True),
        sa.Column('created_at', sa.DateTime(), server_default=sa.text("TIMEZONE('utc', now())"), nullable=False),
        sa.Column('updated_at', sa.DateTime(), server_default=sa.text("TIMEZONE('utc', now())"), nullable=False),
        sa.PrimaryKeyConstraint('id')
    )
    op.add_column('user', sa.Column('created_at', sa.DateTime(), server_default=sa.text("TIMEZONE('utc', now())"), nullable=False))
    op.add_column('user', sa.Column('updated_at', sa.DateTime(), server_default=sa.text("TIMEZONE('utc', now())"), nullable=False))
    op.add_column('user', sa.Column('company_id', sa.UUID(), nullable=False))
    op.create_foreign_key(None, 'user', 'company', ['company_id'], ['id'])
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'user', type_='foreignkey')
    op.drop_column('user', 'company_id')
    op.drop_column('user', 'updated_at')
    op.drop_column('user', 'created_at')
    op.drop_table('company')
    # ### end Alembic commands ###
