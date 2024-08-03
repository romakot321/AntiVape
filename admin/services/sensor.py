from fastapi import Depends

from admin.schemas.sensor import SensorGetSchema, SensorCreateSchema
from admin.schemas.sensor import SensorShortSchema, SensorFiltersSchema
from admin.schemas.sensor import SensorUpdateSchema
from admin.repositories.sensor import SensorRepository
from admin.repositories.sensor_data import SensorDataRepository
from admin.services.access import SensorAccessService
from admin.db.tables import Sensor


class SensorService:
    def __init__(
            self,
            repository: SensorRepository = Depends(),
            access_service: SensorAccessService = Depends()
    ):
        self.repository = repository
        self.access_service = access_service

    async def create(self, schema: SensorCreateSchema, creator_id: int) -> SensorShortSchema:
        model = Sensor(creator_id=creator_id, **schema.model_dump())
        model = await self.repository.create(model)
        return SensorShortSchema.model_validate(model)

    async def get_one(self, sensor_id: int | None = None, sensor_guid: str | None = None) -> SensorGetSchema:
        model = await self.repository.get_one(sensor_id=sensor_id, sensor_guid=sensor_guid)
        return SensorGetSchema.model_validate(model)

    async def get_many(self, filters: SensorFiltersSchema) -> list[SensorShortSchema]:
        filters = filters.model_dump(exclude_none=True)
        models = await self.repository.get_many(**filters)
        models = await self.access_service.filter_get_many_response(models)
        return [
            SensorShortSchema.model_validate(model)
            for model in models
        ]

    async def update(self, sensor_id: int, schema: SensorUpdateSchema) -> SensorShortSchema:
        fields = schema.model_dump(exclude_none=True)
        model = await self.repository.update(sensor_id, **fields)
        return SensorShortSchema.model_validate(model)

    async def delete(self, sensor_id: int) -> None:
        await self.repository.delete(sensor_id)

