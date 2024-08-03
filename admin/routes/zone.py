from fastapi import APIRouter, Depends

from admin.schemas.zone import ZoneShortSchema
from admin.schemas.zone import ZoneGetSchema
from admin.schemas.zone import ZoneCreateSchema
from admin.schemas.zone import ZoneUpdateSchema
from admin.schemas.zone import ZoneFiltersSchema
from admin.services.zone import ZoneService
from admin.services.access import ZoneAccessService
from admin.db.tables import User
from admin.dependencies import get_current_user

router = APIRouter(prefix="/api/zone", tags=["Zone"])


@router.get('', response_model=list[ZoneShortSchema])
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
    status_code=201
)
async def create_zone(
        schema: ZoneCreateSchema,
        service: ZoneService = Depends(),
        user: User = Depends(get_current_user)
):
    return await service.create(schema, creator_id=user.id)


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

