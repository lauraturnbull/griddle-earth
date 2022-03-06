"""Add gateways/portals to components which link to other location coordinates

Revision ID: adc241a51911
Revises: 25c331fa3797
Create Date: 2022-03-06 21:15:47.428073

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'adc241a51911'
down_revision = '25c331fa3797'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('component', sa.Column('is_gateway', sa.Boolean(), nullable=False))
    op.add_column('component', sa.Column('transports_to_x_coordinate', sa.Integer(), nullable=True))
    op.add_column('component', sa.Column('transports_to_y_coordinate', sa.Integer(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('component', 'transports_to_y_coordinate')
    op.drop_column('component', 'transports_to_x_coordinate')
    op.drop_column('component', 'is_gateway')
    # ### end Alembic commands ###
