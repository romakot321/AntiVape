from sqlalchemy import select, exists, func
import datetime as dt

from .base import BaseRepository
from admin.db.tables import Sensor, Room, SensorData


class SensorRepository(BaseRepository):
    base_table = Sensor

    async def create(self, model: Sensor) -> Sensor:
        return await self._create(model)

    async def get_one(self, sensor_id: int | None = None, sensor_guid: str | None = None) -> Sensor:
        filters = {k: v for k, v in (('id', sensor_id), ('guid', sensor_guid)) if v is not None}
        return await self._get_one(
            **filters,
            select_in_load=[{'parent': Sensor.room, 'children': [Room.zone]}]
        )

    async def get_many(
            self,
            active: bool = False,
            zone_id: int | None = None,
            guid: str | None = None,
            **filters
    ) -> list[Sensor]:
        query = self._get_many_query(**filters)
        if guid is not None:
            query = self._query_like_filter(query, guid=guid)
        if zone_id is not None:
            query = query.filter(Sensor.zone.has(id=zone_id))
        if active:
            query = query.filter(Sensor.data.any())
            query = query.filter(~self._check_sensor_active_query())
        return list(await self.session.scalars(query))

    async def update(self, sensor_id: int, **fields) -> Sensor:
        return await self._update(sensor_id, **fields)

    async def delete(self, sensor_id: int) -> None:
        await self._delete(sensor_id)

    async def get_creator_id(self, sensor_id: int | None = None, sensor_guid: str | None = None) -> int | None:
        filters = {k: v for k, v in (('id', sensor_id), ('guid', sensor_guid)) if v is not None}
        query = select(Sensor.creator_id).filter_by(**filters)
        return await self.session.scalar(query)

    async def count_sensors(self, zone_id: int | None = None, room_id: int | None = None, active: bool = False) -> int:
        query = select(func.count(Sensor.id))
        if zone_id is not None:
            query = query.filter(Sensor.zone.has(id=zone_id))
        if room_id is not None:
            query = query.filter(Sensor.room_id == room_id)
        if active:
            query = query.filter(self._check_sensor_active_query())
        return await self.session.scalar(query)

    @staticmethod
    def _check_sensor_active_query():
        max_old_time = dt.datetime.now() - dt.timedelta(minutes=60)
        return exists(
            select(SensorData)
                .filter(SensorData.created_at > max_old_time)
                .filter(SensorData.sensor_guid == Sensor.guid)
        )

