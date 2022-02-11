"""make columns non nullable

Revision ID: 653b31fb507a
Revises: b86663c397fe
Create Date: 2022-02-11 20:36:11.879672

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '653b31fb507a'
down_revision = 'b86663c397fe'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('component', 'name',
               existing_type=sa.VARCHAR(),
               nullable=False)
    op.alter_column('component', 'description',
               existing_type=sa.VARCHAR(),
               nullable=False)
    op.alter_column('game', 'health_points',
               existing_type=sa.INTEGER(),
               nullable=False)
    op.alter_column('game', 'created',
               existing_type=postgresql.TIMESTAMP(),
               nullable=False)
    op.alter_column('item', 'name',
               existing_type=sa.VARCHAR(),
               nullable=False)
    op.alter_column('item', 'item_type',
               existing_type=sa.VARCHAR(),
               nullable=False)
    op.alter_column('item', 'health_points',
               existing_type=sa.INTEGER(),
               nullable=False)
    op.alter_column('item', 'collection_method',
               existing_type=sa.VARCHAR(),
               nullable=False)
    op.alter_column('items', 'quantity',
               existing_type=sa.INTEGER(),
               nullable=False)
    op.alter_column('location', 'x_coordinate',
               existing_type=sa.INTEGER(),
               nullable=False)
    op.alter_column('location', 'y_coordinate',
               existing_type=sa.INTEGER(),
               nullable=False)
    op.alter_column('location', 'name',
               existing_type=sa.VARCHAR(),
               nullable=False)
    op.alter_column('location', 'description',
               existing_type=sa.VARCHAR(),
               nullable=False)
    op.alter_column('location', 'region',
               existing_type=sa.VARCHAR(),
               nullable=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('location', 'region',
               existing_type=sa.VARCHAR(),
               nullable=True)
    op.alter_column('location', 'description',
               existing_type=sa.VARCHAR(),
               nullable=True)
    op.alter_column('location', 'name',
               existing_type=sa.VARCHAR(),
               nullable=True)
    op.alter_column('location', 'y_coordinate',
               existing_type=sa.INTEGER(),
               nullable=True)
    op.alter_column('location', 'x_coordinate',
               existing_type=sa.INTEGER(),
               nullable=True)
    op.alter_column('items', 'quantity',
               existing_type=sa.INTEGER(),
               nullable=True)
    op.alter_column('item', 'collection_method',
               existing_type=sa.VARCHAR(),
               nullable=True)
    op.alter_column('item', 'health_points',
               existing_type=sa.INTEGER(),
               nullable=True)
    op.alter_column('item', 'item_type',
               existing_type=sa.VARCHAR(),
               nullable=True)
    op.alter_column('item', 'name',
               existing_type=sa.VARCHAR(),
               nullable=True)
    op.alter_column('game', 'created',
               existing_type=postgresql.TIMESTAMP(),
               nullable=True)
    op.alter_column('game', 'health_points',
               existing_type=sa.INTEGER(),
               nullable=True)
    op.alter_column('component', 'description',
               existing_type=sa.VARCHAR(),
               nullable=True)
    op.alter_column('component', 'name',
               existing_type=sa.VARCHAR(),
               nullable=True)
    # ### end Alembic commands ###
