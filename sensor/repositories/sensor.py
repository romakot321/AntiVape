import datetime as dt
from loguru import logger

from .base import BaseRepository


class SensorRepository(BaseRepository):
    @staticmethod
    def _generate_key(received_at: dt.datetime, guid: str):
        return guid + '---' + str(received_at.timestamp())

    async def store(self, guid: str, received_at: dt.datetime, data: str):
        key = self._generate_key(received_at, guid)
        await self._store(key, data)
        logger.debug(f'Stored {key} {data}')

    async def pop_all(self) -> list[tuple[str, str]]:
        rows = []
        async for key in self.session.scan_iter():
            value = await self.session.getdel(key)
            rows.append((key, value))
        logger.debug(rows)
        return rows

