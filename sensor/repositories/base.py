from fastapi import Depends
from sensor.db.base import Redis, get_session


class BaseRepository:
    def __init__(self, session: Redis = Depends(get_session)):
        self.session = session

    async def _store(self, key: str, value: str | dict):
        if isinstance(value, str):
            return await self.session.set(key, value)
        elif isinstance(value, dict):
            return await self.session.hmset(key, value)
        raise ValueError(f"Unknown value type {type(value)}")

