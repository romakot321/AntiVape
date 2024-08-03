from fastapi import Depends
import json
import datetime as dt

from sensor.repositories.sensor import SensorRepository
from sensor.schemas.sensor import SensorDataSchema


class SensorService:
    def __init__(self, repository: SensorRepository = Depends()):
        self.repository = repository

    async def store(self, data: SensorDataSchema):
        dumped_data = json.dumps(data.model_dump())
        await self.repository.store(received_at=dt.datetime.now(), data=dumped_data, guid=data.guid)


