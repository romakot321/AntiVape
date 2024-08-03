from sqlalchemy import exc

from admin.db.base import AsyncSession, async_session
from admin.db.tables import SensorData
from admin.repositories.sensor_data import SensorDataRepository
from admin.schemas.sensor_data import SensorDataSchema


class AdminController:
    def __init__(self, session: AsyncSession):
        self.sensor_data_repository = SensorDataRepository(session=session)
        self.session = session

    async def _store_sensors_data(self, sensors_data: list[SensorData]):
        for data in sensors_data:
            try:
                await self.sensor_data_repository.create(data, do_commit=False)
            except exc.IntegrityError:
                await self.session.rollback()
        await self.session.commit()

    @classmethod
    async def store_sensors_data(cls, *sensors_data_schemas: list[SensorDataSchema]) -> None:
        sensors_data = [SensorData(**schema.model_dump()) for schema in sensors_data_schemas]
        async with async_session() as session:
            self = cls(session=session)
            await self._store_sensors_data(sensors_data)

