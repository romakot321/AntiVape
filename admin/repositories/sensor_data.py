from .base import BaseRepository

from admin.db.tables import SensorData


class SensorDataRepository(BaseRepository):
    base_table = SensorData

    async def create(self, model: SensorData) -> SensorData:
        return await self._create(model)

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

    async def get_creator_id(self, sensor_data_id: int) -> int | None:
        query = select(SensorData.creator_id).filter_by(id=room_id)
        return await self.session.scalar(query)

