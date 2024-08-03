import datetime as dt

from .base import BaseRepository


class SensorRepository(BaseRepository):
    @staticmethod
    def _generate_key(received_at: dt.datetime, sensor_info: str):
        return sensor_info + ':' + str(received_at.timestamp())

    async def store(self, sensor_info: str, received_at: dt.datetime, data: str):
        key = self._generate_key(received_at, sensor_info)
        await self._store(key, data)

