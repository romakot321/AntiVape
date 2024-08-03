from sqlalchemy import select

from .base import BaseRepository
from admin.db.tables import Sensor


class SensorRepository(BaseRepository):
    base_table = Sensor

    async def create(self, model: Sensor) -> Sensor:
        return await self._create(model)

    async def get_one(self, sensor_id: int | None = None, sensor_guid: str | None = None) -> Sensor:
        filters = {k: v for k, v in (('id', sensor_id), ('guid', sensor_guid)) if v is not None}
        return await self._get_one(**filters, select_in_load=Sensor.room)

    async def get_many(self, room_id: int | None = None) -> list[Sensor]:
        return list(await self._get_many(room_id=room_id))

    async def update(self, sensor_id: int, **fields) -> Sensor:
        return await self._update(sensor_id, **fields)

    async def delete(self, sensor_id: int) -> None:
        await self._delete(sensor_id)

    async def get_creator_id(self, sensor_id: int | None = None, sensor_guid: str | None = None) -> int | None:
        filters = {k: v for k, v in (('id', sensor_id), ('guid', sensor_guid)) if v is not None}
        query = select(Sensor.creator_id).filter_by(**filters)
        return await self.session.scalar(query)

