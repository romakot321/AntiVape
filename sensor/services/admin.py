from admin.controller import AdminController
from admin.schemas.sensor_data import SensorDataSchema
from sensor.db.base import get_session, Redis
from sensor.repositories.sensor import SensorRepository


class AdminAPIService:
    def __init__(self, session: Redis):
        self.sensor_repository = SensorRepository(session=session)

    async def _pop_sensors_data(self) -> list[SensorDataSchema]:
        rows = await self.sensor_repository.pop_all()
        schemas = [
            SensorDataSchema.from_redis(key=row[0].decode(), value=row[1].decode())
            for row in rows
        ]
        return list(filter(lambda i: i is not None, schemas))  # Delete invalid data

    async def _store_in_admin(self, *sensors_data_schemas: list[SensorDataSchema]):
        await AdminController.store_sensors_data(*sensors_data_schemas)

    @classmethod
    async def transfer_sensors_data(cls):
        session_getter = get_session()
        session = next(session_getter)
        self = cls(session=session)
        data = await self._pop_sensors_data()
        await self._store_in_admin(*data)

