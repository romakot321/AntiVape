from sqlalchemy import exc

from admin.db.base import AsyncSession, async_session
from admin.db.tables import SensorData
from admin.repositories.sensor_data import SensorDataRepository
from admin.repositories.sensor import SensorRepository
from admin.schemas.sensor_data import SensorDataSchema


class AdminController:
    def __init__(self, session: AsyncSession):
        self.sensor_data_repository = SensorDataRepository(session=session)
        self.sensor_repository = SensorRepository(session=session)
        self.session = session

    async def _store_sensors_data(self, sensors_data: list[SensorData]):
        for data in sensors_data:
            try:
                await self.sensor_data_repository.create(data, do_commit=False)
            except exc.IntegrityError:
                await self.session.rollback()
        await self.session.commit()

    async def _filter_unexisting_sensors(self, sensor_datas: list[SensorData]):
        cache = {}
        filtered = []
        for sensor_data in sensor_datas:
            guid = sensor_data.sensor_guid
            if cache.get(guid, None) is None:
                cache[guid] = await self.sensor_repository.is_exists(sensor_guid=guid)
            if cache[guid]:
                filtered.append(sensor_data)
        return filtered

    @classmethod
    async def store_sensors_data(cls, *sensors_data_schemas: list[SensorDataSchema]) -> None:
        sensors_data = [SensorData(**schema.model_dump()) for schema in sensors_data_schemas]
        async with async_session() as session:
            self = cls(session=session)
            sensors_data = await self._filter_unexisting_sensors(sensors_data)
            await self._store_sensors_data(sensors_data)

