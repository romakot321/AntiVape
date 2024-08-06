from fastapi import APIRouter, Depends

from admin.schemas.room import RoomShortSchema
from admin.schemas.room import RoomGetSchema
from admin.schemas.room import RoomCreateSchema
from admin.schemas.room import RoomUpdateSchema
from admin.schemas.room import RoomFiltersSchema
from admin.schemas.room import RoomStatisticFiltersSchema
from admin.schemas.room import RoomStatisticGetSchema
from admin.services.room import RoomService
from admin.services.access import RoomAccessService
from admin.db.tables import User
from admin.dependencies import get_current_user

router = APIRouter(prefix="/api/room", tags=["Room"])


@router.get('', response_model=list[RoomShortSchema])
async def get_rooms(filters: RoomFiltersSchema = Depends(), service: RoomService = Depends()):
    return await service.get_many(filters)


@router.get(
    '/{room_id}',
    response_model=RoomGetSchema,
    dependencies=[RoomAccessService.validate_get_one()]
)
async def get_room(room_id: int, service: RoomService = Depends()):
    return await service.get_one(room_id=room_id)


@router.get(
    '/{room_id}/statistic',
    response_model=RoomStatisticGetSchema,
    dependencies=[RoomAccessService.validate_get_one()]
)
async def get_room_statistic(
        room_id: int,
        schema: RoomStatisticFiltersSchema = Depends(),
        service: RoomService = Depends()
):
    return await service.get_sensors_statistic(room_id, schema)


@router.post(
    '',
    response_model=RoomShortSchema,
    status_code=201,
    dependencies=[RoomAccessService.validate_create()]
)
async def create_room(
        schema: RoomCreateSchema,
        service: RoomService = Depends(),
        user: User = Depends(get_current_user)
):
    return await service.create(schema, creator_id=user.id)


@router.patch(
    '/{room_id}',
    response_model=RoomShortSchema,
    dependencies=[RoomAccessService.validate_update()]
)
async def update_room(
        room_id: int,
        schema: RoomUpdateSchema,
        service: RoomService = Depends()
):
    return await service.update(room_id, schema)


@router.delete(
    '/{room_id}',
    status_code=204,
    dependencies=[RoomAccessService.validate_delete()]
)
async def delete_room(room_id: int, service: RoomService = Depends()):
    await service.delete(room_id)

