"""add adventure logs

Revision ID: 36dc23330424
Revises: 0db346b0362b
Create Date: 2022-02-06 21:15:27.347180

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '36dc23330424'
down_revision = '0db346b0362b'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('adventure_log',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('discovered_locations_id', sa.Integer(), nullable=True),
    sa.Column('discoverable_locations_id', sa.Integer(), nullable=True),
    sa.Column('discovered_items_id', sa.Integer(), nullable=True),
    sa.Column('discoverable_items_id', sa.Integer(), nullable=True),
    sa.Column('game_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['discoverable_items_id'], ['item.id'], name=op.f('fk_adventure_log_discoverable_items_id_item')),
    sa.ForeignKeyConstraint(['discoverable_locations_id'], ['location.id'], name=op.f('fk_adventure_log_discoverable_locations_id_location')),
    sa.ForeignKeyConstraint(['discovered_items_id'], ['item.id'], name=op.f('fk_adventure_log_discovered_items_id_item')),
    sa.ForeignKeyConstraint(['discovered_locations_id'], ['location.id'], name=op.f('fk_adventure_log_discovered_locations_id_location')),
    sa.ForeignKeyConstraint(['game_id'], ['game.id'], name=op.f('fk_adventure_log_game_id_game')),
    sa.PrimaryKeyConstraint('id', name=op.f('pk_adventure_log'))
    )
    op.create_index(op.f('ix_adventure_log_id'), 'adventure_log', ['id'], unique=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_adventure_log_id'), table_name='adventure_log')
    op.drop_table('adventure_log')
    # ### end Alembic commands ###
