"""empty message

Revision ID: 1a711e984adf
Revises: 
Create Date: 2024-03-19 02:24:48.532137

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '1a711e984adf'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('customers',
    sa.Column('customer_id', sa.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('customer_name', sa.TEXT(), nullable=False),
    sa.Column('created_at', sa.TIMESTAMP(), nullable=False),
    sa.Column('updated_at', sa.TIMESTAMP(), nullable=False),
    sa.PrimaryKeyConstraint('customer_id'),
    sa.UniqueConstraint('customer_name')
    )
    op.create_table('devices',
    sa.Column('device_id', sa.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('device_mac_address', sa.TEXT(), nullable=False),
    sa.Column('device_ip_v4_address', sa.TEXT(), nullable=False),
    sa.Column('device_category', sa.Enum('ROUTER', 'SWITCH', 'BRIDGE', 'REPEATER', 'WIRELESS_ACCESS_POINT', 'NETWORK_INTERFACE_CARD', 'FIREWALL', 'HUB', 'MODEM', 'GATEWAY', name='devicecategory', native_enum=False), nullable=False),
    sa.Column('device_status', sa.Enum('ACTIVE', 'NOT_ACTIVE', 'DISABLED', name='devicestatus', native_enum=False), nullable=False),
    sa.Column('created_at', sa.TIMESTAMP(), nullable=False),
    sa.Column('updated_at', sa.TIMESTAMP(), nullable=False),
    sa.Column('customer_id', sa.INTEGER(), nullable=True),
    sa.ForeignKeyConstraint(['customer_id'], ['customers.customer_id'], ),
    sa.PrimaryKeyConstraint('device_id'),
    sa.UniqueConstraint('device_mac_address')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('devices')
    op.drop_table('customers')
    # ### end Alembic commands ###
