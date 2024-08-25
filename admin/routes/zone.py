from fastapi import APIRouter, Depends, WebSocket
from fastapi import WebSocketDisconnect
import asyncio

from admin.schemas.zone import ZoneShortSchema
from admin.schemas.zone import ZoneGetSchema
from admin.schemas.zone import ZoneCreateSchema
from admin.schemas.zone import ZoneUpdateSchema
from admin.schemas.zone import ZoneFiltersSchema
from admin.schemas.zone import ZoneStatisticsFiltersSchema
from admin.schemas.zone import ZoneStatisticsGetSchema
from admin.services.zone import ZoneService, WebsocketZoneService
from admin.services.access import ZoneAccessService
from admin.db.tables import User
from admin.dependencies import get_current_user, get_current_user_websocket

router = APIRouter(prefix="/api/zone", tags=["Zone"])


@router.get(
    '',
    response_model=list[ZoneShortSchema],
    dependencies=[ZoneAccessService.validate_get_many()]
)
async def get_zones(filters: ZoneFiltersSchema = Depends(), service: ZoneService = Depends()):
    return await service.get_many(filters)


@router.get(
    '/{zone_id}',
    response_model=ZoneGetSchema,
    dependencies=[ZoneAccessService.validate_get_one()]
)
async def get_zone(zone_id: int, service: ZoneService = Depends()):
    return await service.get_one(zone_id=zone_id)


@router.post(
    '',
    response_model=ZoneShortSchema,
    status_code=201,
    dependencies=[ZoneAccessService.validate_create()]
)
async def create_zone(
        schema: ZoneCreateSchema,
        service: ZoneService = Depends(),
):
    return await service.create(schema)


@router.patch(
    '/{zone_id}',
    response_model=ZoneShortSchema,
    dependencies=[ZoneAccessService.validate_update()]
)
async def update_zone(
        zone_id: int,
        schema: ZoneUpdateSchema,
        service: ZoneService = Depends()
):
    return await service.update(zone_id, schema)


@router.delete(
    '/{zone_id}',
    status_code=204,
    dependencies=[ZoneAccessService.validate_delete()]
)
async def delete_zone(zone_id: int, service: ZoneService = Depends()):
    await service.delete(zone_id)


@router.get(
    '/{zone_id}/statistics',
    response_model=ZoneStatisticsGetSchema,
    dependencies=[ZoneAccessService.validate_get_one()]
)
async def get_zone_statistics(zone_id: int, filters: ZoneStatisticsFiltersSchema = Depends(), service: ZoneService = Depends()):
    return await service.get_sensors_statistics(zone_id, filters)


@router.websocket('/stream')
async def stream_zone_statistics(websocket: WebSocket, service: WebsocketZoneService = Depends()):
    await websocket.accept()
    async for statistics in service.stream_zones_sensors_statistics():
        try:
            await websocket.send_json(statistics.model_dump_json())
        except WebSocketDisconnect:
            break
        await asyncio.sleep(30)

