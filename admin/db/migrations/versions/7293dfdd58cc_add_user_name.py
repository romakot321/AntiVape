"""add user name

Revision ID: 7293dfdd58cc
Revises: 636b6b35fadf
Create Date: 2024-08-24 02:15:38.561451

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '7293dfdd58cc'
down_revision = '636b6b35fadf'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('name', sa.String(), nullable=True))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('users', 'name')
    # ### end Alembic commands ###
