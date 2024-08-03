from fastapi import Depends
import json
import datetime as dt

from sensor.repositories.sensor import SensorRepository
from sensor.schemas.sensor import SensorDataSchema


class SensorService:
    def __init__(self, repository: SensorRepository = Depends()):
        self.repository = repository

    async def store(self, raw_data: str):
        data = SensorDataSchema(data=raw_data)
        await self.repository.store(received_at=dt.datetime.now(), **data.model_dump())


