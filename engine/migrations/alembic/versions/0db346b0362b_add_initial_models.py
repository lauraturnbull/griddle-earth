"""add initial models

Revision ID: 0db346b0362b
Revises: 
Create Date: 2022-02-04 21:35:18.193376

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '0db346b0362b'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('game',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('health_points', sa.Integer(), nullable=True),
    sa.Column('created', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id', name=op.f('pk_game'))
    )
    op.create_index(op.f('ix_game_id'), 'game', ['id'], unique=False)
    op.create_table('item',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=True),
    sa.Column('item_type', sa.String(), nullable=True),
    sa.Column('health_points', sa.Integer(), nullable=True),
    sa.PrimaryKeyConstraint('id', name=op.f('pk_item'))
    )
    op.create_table('inventory',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('game_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['game_id'], ['game.id'], name=op.f('fk_inventory_game_id_game')),
    sa.PrimaryKeyConstraint('id', name=op.f('pk_inventory'))
    )
    op.create_index(op.f('ix_inventory_id'), 'inventory', ['id'], unique=False)
    op.create_table('map',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('game_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['game_id'], ['game.id'], name=op.f('fk_map_game_id_game')),
    sa.PrimaryKeyConstraint('id', name=op.f('pk_map'))
    )
    op.create_index(op.f('ix_map_id'), 'map', ['id'], unique=False)
    op.create_table('location',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('x_coordinate', sa.Integer(), nullable=True),
    sa.Column('y_coordinate', sa.Integer(), nullable=True),
    sa.Column('name', sa.String(), nullable=True),
    sa.Column('description', sa.String(), nullable=True),
    sa.Column('region', sa.String(), nullable=True),
    sa.Column('game_id', sa.Integer(), nullable=True),
    sa.Column('map_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['game_id'], ['game.id'], name=op.f('fk_location_game_id_game')),
    sa.ForeignKeyConstraint(['map_id'], ['map.id'], name=op.f('fk_location_map_id_map')),
    sa.PrimaryKeyConstraint('id', name=op.f('pk_location'))
    )
    op.create_index(op.f('ix_location_id'), 'location', ['id'], unique=False)
    op.create_table('component',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=True),
    sa.Column('description', sa.String(), nullable=True),
    sa.Column('location_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['location_id'], ['location.id'], name=op.f('fk_component_location_id_location')),
    sa.PrimaryKeyConstraint('id', name=op.f('pk_component'))
    )
    op.create_table('items',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('quantity', sa.Integer(), nullable=True),
    sa.Column('item_id', sa.Integer(), nullable=True),
    sa.Column('component_id', sa.Integer(), nullable=True),
    sa.Column('inventory_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['component_id'], ['component.id'], name=op.f('fk_items_component_id_component')),
    sa.ForeignKeyConstraint(['inventory_id'], ['inventory.id'], name=op.f('fk_items_inventory_id_inventory')),
    sa.ForeignKeyConstraint(['item_id'], ['item.id'], name=op.f('fk_items_item_id_item')),
    sa.PrimaryKeyConstraint('id', name=op.f('pk_items'))
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('items')
    op.drop_table('component')
    op.drop_index(op.f('ix_location_id'), table_name='location')
    op.drop_table('location')
    op.drop_index(op.f('ix_map_id'), table_name='map')
    op.drop_table('map')
    op.drop_index(op.f('ix_inventory_id'), table_name='inventory')
    op.drop_table('inventory')
    op.drop_table('item')
    op.drop_index(op.f('ix_game_id'), table_name='game')
    op.drop_table('game')
    # ### end Alembic commands ###
