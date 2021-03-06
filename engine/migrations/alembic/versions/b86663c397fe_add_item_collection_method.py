"""Add item collection method

Revision ID: b86663c397fe
Revises: 6b0968883c7b
Create Date: 2022-02-09 22:21:39.160614

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'b86663c397fe'
down_revision = '6b0968883c7b'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('item', sa.Column('collection_method', sa.String(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('item', 'collection_method')
    # ### end Alembic commands ###
