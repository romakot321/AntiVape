"""add cascade delete

Revision ID: 1b9435dc9cd7
Revises: 7293dfdd58cc
Create Date: 2024-09-08 10:34:04.946066

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '1b9435dc9cd7'
down_revision = '7293dfdd58cc'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint('rooms_zone_id_fkey', 'rooms', type_='foreignkey')
    op.drop_constraint('rooms_editor_id_fkey', 'rooms', type_='foreignkey')
    op.drop_constraint('rooms_owner_id_fkey', 'rooms', type_='foreignkey')
    op.create_foreign_key(None, 'rooms', 'users', ['editor_id'], ['id'], ondelete='CASCADE')
    op.create_foreign_key(None, 'rooms', 'users', ['owner_id'], ['id'], ondelete='CASCADE')
    op.create_foreign_key(None, 'rooms', 'zones', ['zone_id'], ['id'], ondelete='CASCADE')
    op.drop_constraint('sensor_datas_sensor_guid_fkey', 'sensor_datas', type_='foreignkey')
    op.create_foreign_key(None, 'sensor_datas', 'sensors', ['sensor_guid'], ['guid'], ondelete='CASCADE')
    op.drop_constraint('sensors_room_id_fkey', 'sensors', type_='foreignkey')
    op.drop_constraint('sensors_owner_id_fkey', 'sensors', type_='foreignkey')
    op.drop_constraint('sensors_editor_id_fkey', 'sensors', type_='foreignkey')
    op.create_foreign_key(None, 'sensors', 'users', ['editor_id'], ['id'], ondelete='CASCADE')
    op.create_foreign_key(None, 'sensors', 'users', ['owner_id'], ['id'], ondelete='CASCADE')
    op.create_foreign_key(None, 'sensors', 'rooms', ['room_id'], ['id'], ondelete='CASCADE')
    op.drop_constraint('zones_editor_id_fkey', 'zones', type_='foreignkey')
    op.drop_constraint('zones_owner_id_fkey', 'zones', type_='foreignkey')
    op.create_foreign_key(None, 'zones', 'users', ['owner_id'], ['id'], ondelete='CASCADE')
    op.create_foreign_key(None, 'zones', 'users', ['editor_id'], ['id'], ondelete='CASCADE')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'zones', type_='foreignkey')
    op.drop_constraint(None, 'zones', type_='foreignkey')
    op.create_foreign_key('zones_owner_id_fkey', 'zones', 'users', ['owner_id'], ['id'])
    op.create_foreign_key('zones_editor_id_fkey', 'zones', 'users', ['editor_id'], ['id'])
    op.drop_constraint(None, 'sensors', type_='foreignkey')
    op.drop_constraint(None, 'sensors', type_='foreignkey')
    op.drop_constraint(None, 'sensors', type_='foreignkey')
    op.create_foreign_key('sensors_editor_id_fkey', 'sensors', 'users', ['editor_id'], ['id'])
    op.create_foreign_key('sensors_owner_id_fkey', 'sensors', 'users', ['owner_id'], ['id'])
    op.create_foreign_key('sensors_room_id_fkey', 'sensors', 'rooms', ['room_id'], ['id'])
    op.drop_constraint(None, 'sensor_datas', type_='foreignkey')
    op.create_foreign_key('sensor_datas_sensor_guid_fkey', 'sensor_datas', 'sensors', ['sensor_guid'], ['guid'])
    op.drop_constraint(None, 'rooms', type_='foreignkey')
    op.drop_constraint(None, 'rooms', type_='foreignkey')
    op.drop_constraint(None, 'rooms', type_='foreignkey')
    op.create_foreign_key('rooms_owner_id_fkey', 'rooms', 'users', ['owner_id'], ['id'])
    op.create_foreign_key('rooms_editor_id_fkey', 'rooms', 'users', ['editor_id'], ['id'])
    op.create_foreign_key('rooms_zone_id_fkey', 'rooms', 'zones', ['zone_id'], ['id'])
    # ### end Alembic commands ###