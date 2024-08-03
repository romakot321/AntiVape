from fastapi import Depends

from admin.schemas.zone import ZoneGetSchema, ZoneCreateSchema
from admin.schemas.zone import ZoneShortSchema, ZoneFiltersSchema
from admin.schemas.zone import ZoneUpdateSchema
from admin.repositories.zone import ZoneRepository
from admin.services.access import ZoneAccessService
from admin.db.tables import Zone


class ZoneService:
    def __init__(
            self,
            repository: ZoneRepository = Depends(),
            access_service: ZoneAccessService = Depends()
    ):
        self.repository = repository
        self.access_service = access_service

    async def create(self, schema: ZoneCreateSchema, creator_id: int) -> ZoneShortSchema:
        model = Zone(creator_id=creator_id, **schema.model_dump())
        model = await self.repository.create(model)
        return ZoneShortSchema.model_validate(model)

    async def get_one(self, zone_id: int) -> ZoneGetSchema:
        model = await self.repository.get_one(zone_id=zone_id)
        return ZoneGetSchema.model_validate(model)

    async def get_many(self, filters: ZoneFiltersSchema) -> list[ZoneShortSchema]:
        filters = filters.model_dump(exclude_none=True)
        models = await self.repository.get_many(**filters)
        models = await self.access_service.filter_get_many_response(models)
        return [
            ZoneShortSchema.model_validate(model)
            for model in models
        ]

    async def update(self, zone_id: int, schema: ZoneUpdateSchema) -> ZoneShortSchema:
        fields = schema.model_dump(exclude_none=True)
        model = await self.repository.update(zone_id, **fields)
        return ZoneShortSchema.model_validate(model)

    async def delete(self, zone_id: int) -> None:
        await self.repository.delete(zone_id)

