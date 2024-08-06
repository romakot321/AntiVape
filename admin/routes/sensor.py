from fastapi import APIRouter, Depends

from admin.schemas.sensor import SensorShortSchema
from admin.schemas.sensor import SensorGetSchema
from admin.schemas.sensor import SensorCreateSchema
from admin.schemas.sensor import SensorUpdateSchema
from admin.schemas.sensor import SensorFiltersSchema
from admin.services.sensor import SensorService
from admin.services.access import SensorAccessService
from admin.db.tables import User
from admin.dependencies import get_current_user

router = APIRouter(prefix="/api/sensor", tags=["Sensor"])


@router.get('', response_model=list[SensorShortSchema])
async def get_sensors(filters: SensorFiltersSchema = Depends(), service: SensorService = Depends()):
    """Get list on sensors for room_id, or search sensor by guid"""
    return await service.get_many(filters)


@router.get(
    '/{id_or_guid}',
    response_model=SensorGetSchema,
    dependencies=[SensorAccessService.validate_get_one()]
)
async def get_sensor(id_or_guid: str, service: SensorService = Depends()):
    sensor_guid, sensor_id = None, None
    if id_or_guid.isnumeric():
        sensor_id = int(id_or_guid)
    else:
        sensor_guid = id_or_guid
    return await service.get_one(sensor_id=sensor_id, sensor_guid=sensor_guid)


@router.post(
    '',
    response_model=SensorShortSchema,
    status_code=201,
    dependencies=[SensorAccessService.validate_create()]
)
async def create_sensor(
        schema: SensorCreateSchema,
        service: SensorService = Depends(),
        user: User = Depends(get_current_user)
):
    return await service.create(schema, creator_id=user.id)


@router.patch(
    '/{sensor_id}',
    response_model=SensorShortSchema,
    dependencies=[SensorAccessService.validate_update()]
)
async def update_sensor(
        sensor_id: int,
        schema: SensorUpdateSchema,
        service: SensorService = Depends()
):
    return await service.update(sensor_id, schema)


@router.delete(
    '/{sensor_id}',
    status_code=204,
    dependencies=[SensorAccessService.validate_delete()]
)
async def delete_sensor(sensor_id: int, service: SensorService = Depends()):
    await service.delete(sensor_id)

