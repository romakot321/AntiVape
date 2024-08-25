import datetime as dt
from sqlalchemy import select

from .base import BaseRepository
from admin.db.tables import SensorData, Sensor


class SensorDataRepository(BaseRepository):
    base_table = SensorData

    async def create(self, model: SensorData, do_commit: bool = True) -> SensorData:
        return await self._create(model, do_commit=do_commit)

    async def get_one(self, sensor_data_id: int) -> SensorData:
        filters = {k: v for k, v in (('id', sensor_data_id),) if v is not None}
        return await self._get_one(**filters, select_in_load=[SensorData.sensor])

    async def get_many(self, sensor_id: int | None = None, **filters) -> list[SensorData]:
        filters |= {k: v for k, v in (('sensor_id', sensor_id),) if v is not None}
        return list(await self._get_many(**filters))

    async def update(self, sensor_data_id: int, **fields) -> SensorData:
        return await self._update(sensor_data_id, **fields)

    async def delete(self, sensor_data_id: int) -> None:
        await self._delete(sensor_data_id)

    async def get_owner_id(self, sensor_data_id: int) -> int | None:
        query = select(SensorData.owner_id).filter_by(id=room_id)
        return await self.session.scalar(query)

    async def get_room_statistic(
            self,
            room_id: int,
            from_datetime: dt.datetime | None = None,
            to_datetime: dt.datetime | None = None
    ) -> list[SensorData]:
        query = self._room_statistic_query(room_id, from_datetime, to_datetime)
        return list(await self.session.scalars(query))

    async def get_zone_statistic(
            self,
            zone_id: int,
            from_datetime: dt.datetime | None = None,
            to_datetime: dt.datetime | None = None
    ) -> list[SensorData]:
        query = self._zone_statistic_query(zone_id, from_datetime, to_datetime)
        return list(await self.session.scalars(query))

    @staticmethod
    def _room_statistic_query(room_id, from_datetime, to_datetime):
        query = select(SensorData).filter(SensorData.sensor.has(Sensor.room_id == room_id))
        query = query.order_by(SensorData.created_at)
        if from_datetime is not None:
            from_datetime = from_datetime.replace(tzinfo=None)
            query = query.filter(SensorData.created_at >= from_datetime)
        if to_datetime is not None:
            to_datetime = to_datetime.replace(tzinfo=None)
            query = query.filter(SensorData.created_at <= to_datetime)
        return query

    @classmethod
    def _zone_statistic_query(cls, zone_id, from_datetime, to_datetime):
        query = select(SensorData).filter(SensorData.sensor.has(Sensor.zone_id == zone_id))
        query = query.order_by(SensorData.created_at)
        if from_datetime is not None:
            query = query.filter(SensorData.created_at >= from_datetime)
        if to_datetime is not None:
            query = query.filter(SensorData.created_at <= to_datetime)
        query = cls._query_select_in_load(query, [SensorData.sensor])
        return query

