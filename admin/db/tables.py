import datetime as dt
import uuid
from fastapi_users.db import SQLAlchemyBaseUserTable

from sqlalchemy import bindparam
from sqlalchemy import CheckConstraint
from sqlalchemy import Column
from sqlalchemy import ForeignKey
from sqlalchemy import Table
from sqlalchemy import text
from sqlalchemy import UniqueConstraint
from sqlalchemy import UUID
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.ext.declarative import declared_attr
from sqlalchemy.orm import Mapped as M
from sqlalchemy.orm import mapped_column as column
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from sqlalchemy.sql.expression import false

from admin.db.base import Base


class BaseMixin:
    @declared_attr.directive
    def __tablename__(cls):
        letters = ['_' + i.lower() if i.isupper() else i for i in cls.__name__]
        return ''.join(letters).lstrip('_') + 's'

    created_at: M[dt.datetime] = column(server_default=func.now())
    updated_at: M[dt.datetime] = column(
        server_default=func.now(), onupdate=func.now()
    )
    id: M[int] = column(primary_key=True, index=True)


class OwnableObjectMixin(BaseMixin):
    creator_id: M[int] = column(ForeignKey('users.id'))  # aka owner
    editor_id: M[int | None] = column(ForeignKey('users.id'), nullable=True)

    @declared_attr
    def creator(cls) -> M['User']:
        return relationship("User", foreign_keys=[cls.creator_id], lazy='selectin')

    @declared_attr
    def editor(cls) -> M['User']:
        return relationship("User", foreign_keys=[cls.editor_id], lazy='selectin')


class User(SQLAlchemyBaseUserTable[int], Base):
    __tablename__ = 'users'
    id: M[int] = column(primary_key=True, index=True)


class Sensor(OwnableObjectMixin, Base):
    guid: M[str] = column(index=True, unique=True)
    room_id: M[int | None] = column(ForeignKey('rooms.id'), nullable=True)

    room: M['Room'] = relationship(back_populates="sensors", lazy='selectin', cascade='all, delete')
    data: M[list['SensorData']] = relationship(back_populates="sensor", lazy='selectin')


class SensorData(BaseMixin, Base):
    co2: M[int]
    tvoc: M[int]
    batteryCharge: M[int]
    sensor_guid: M[str] = column(ForeignKey('sensors.guid'))

    sensor: M['Sensor'] = relationship(back_populates='data', lazy='selectin', cascade='all, delete')


class Room(OwnableObjectMixin, Base):
    name: M[str]
    zone_id: M[int] = column(ForeignKey('zones.id'))

    zone: M['Zone'] = relationship(back_populates="rooms", lazy='selectin', cascade='all, delete')
    sensors: M[list['Sensor']] = relationship(back_populates='room', lazy='selectin')


class Zone(OwnableObjectMixin, Base):
    name: M[str]

    rooms: M[list['Room']] = relationship(back_populates='zone', lazy='selectin')

