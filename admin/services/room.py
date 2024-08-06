from fastapi import Depends

from admin.schemas.room import RoomGetSchema, RoomCreateSchema
from admin.schemas.room import RoomShortSchema, RoomFiltersSchema
from admin.schemas.room import RoomUpdateSchema, RoomStatisticFiltersSchema
from admin.schemas.room import RoomStatisticGetSchema
from admin.repositories.room import RoomRepository
from admin.repositories.sensor_data import SensorDataRepository
from admin.services.access import RoomAccessService
from admin.db.tables import Room


class RoomService:
    def __init__(
            self,
            repository: RoomRepository = Depends(),
            access_service: RoomAccessService = Depends(),
            sensor_data_repository: SensorDataRepository = Depends()
    ):
        self.repository = repository
        self.access_service = access_service
        self.sensor_data_repository = sensor_data_repository

    async def create(self, schema: RoomCreateSchema, creator_id: int) -> RoomShortSchema:
        model = Room(creator_id=creator_id, **schema.model_dump())
        model = await self.repository.create(model)
        return RoomShortSchema.model_validate(model)

    async def get_one(self, room_id: int) -> RoomGetSchema:
        model = await self.repository.get_one(room_id=room_id)
        return RoomGetSchema.model_validate(model)

    async def get_many(self, filters: RoomFiltersSchema) -> list[RoomShortSchema]:
        filters = filters.model_dump(exclude_none=True)
        models = await self.repository.get_many(**filters)
        models = await self.access_service.filter_get_many_response(models)
        return [
            RoomShortSchema.model_validate(model)
            for model in models
        ]

    async def update(self, room_id: int, schema: RoomUpdateSchema) -> RoomShortSchema:
        fields = schema.model_dump(exclude_none=True)
        model = await self.repository.update(room_id, **fields)
        return RoomShortSchema.model_validate(model)

    async def delete(self, room_id: int) -> None:
        await self.repository.delete(room_id)

    async def get_sensors_statistic(self, room_id: int, filters: RoomStatisticFiltersSchema) -> RoomStatisticGetSchema:
        filters = filters.model_dump(exclude_none=True)
        models = await self.sensor_data_repository.get_room_statistic(room_id=room_id, **filters)
        return RoomStatisticGetSchema.model_validate({'data': models})

