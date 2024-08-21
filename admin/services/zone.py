from fastapi import Depends
import functools

from admin.schemas.zone import ZoneGetSchema, ZoneCreateSchema
from admin.schemas.zone import ZoneShortSchema, ZoneFiltersSchema
from admin.schemas.zone import ZoneUpdateSchema, ZoneStatisticsFiltersSchema
from admin.schemas.zone import ZoneStatisticsGetSchema, ZoneListStatisticsGetSchema
from admin.repositories.zone import ZoneRepository
from admin.repositories.sensor import SensorRepository
from admin.repositories.sensor_data import SensorDataRepository
from admin.services.access import ZoneAccessService
from admin.services.caching import cacheable
from admin.db.tables import Zone
from admin.dependencies import get_current_user_websocket


class ZoneService:
    def __init__(
            self,
            repository: ZoneRepository = Depends(),
            sensor_repository: SensorRepository = Depends(),
            sensor_data_repository: SensorDataRepository = Depends(),
            access_service: ZoneAccessService = Depends()
    ):
        self.repository = repository
        self.sensor_repository = sensor_repository
        self.access_service = access_service
        self.sensor_data_repository = sensor_data_repository

        self._statistics_cache = {}

    async def create(self, schema: ZoneCreateSchema, creator_id: int) -> ZoneShortSchema:
        model = Zone(creator_id=creator_id, **schema.model_dump())
        model = await self.repository.create(model)
        return ZoneShortSchema.model_validate(model)

    async def get_one(self, zone_id: int) -> ZoneGetSchema:
        model = await self.repository.get_one(zone_id=zone_id)
        active_sensors_count = await self.sensor_repository.count_sensors(zone_id=zone_id, active=True)
        model = model.__dict__ | {'active_sensors_count': active_sensors_count}
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

    async def get_sensors_statistics(self, zone_id: int, filters: ZoneStatisticsFiltersSchema) -> list[ZoneStatisticsGetSchema]:
        filters = filters.model_dump(exclude_none=True)
        models = await self.sensor_data_repository.get_zone_statistic(zone_id=zone_id, **filters)
        return ZoneStatisticsGetSchema.model_validate({'data': models, 'zone_id': zone_id})

    async def stream_zones_sensors_statistics(self):
        zones = await self.get_many(ZoneFiltersSchema())
        while True:
            statistics = []
            for zone in zones:
                statistics.append(await self.get_sensors_statistics(zone.id, ZoneStatisticsFiltersSchema()))
            yield ZoneListStatisticsGetSchema(statistics=statistics)


class WebsocketZoneService(ZoneService):
    def __init__(
            self,
            repository: ZoneRepository = Depends(),
            sensor_repository: SensorRepository = Depends(),
            sensor_data_repository: SensorDataRepository = Depends(),
            current_user=Depends(get_current_user_websocket)
    ):
        self.repository = repository
        self.sensor_repository = sensor_repository
        self.sensor_data_repository = sensor_data_repository
        self.access_service = ZoneAccessService(zone_repository=repository, current_user=current_user)

