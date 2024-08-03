from fastapi import Depends

from admin.db.base import get_session, AsyncSession
from admin.db.tables import User, Zone

from admin.dependencies import get_current_user
from admin.exceptions import AuthException
from admin.repositories.zone import ZoneRepository
from admin.repositories.zone import ZoneRepository

from admin.schemas.zone import ZoneCreateSchema
from admin.schemas.zone import ZoneFiltersSchema


class ZoneAccessService:
    def __init__(
            self,
            zone_repository: ZoneRepository = Depends(),
            current_user: User = Depends(get_current_user)
    ):
        self.zone_repository = zone_repository
        self.current_user = current_user

    async def filter_get_many_response(
            self, zones: list[Zone]
    ) -> list[Zone]:
        for i in range(len(zones)):
            if zones[i].creator_id != self.current_user.id:
                zones[i] = None
        return list(filter(lambda i: i is not None, zones))

    @classmethod
    def validate_get_one(cls):
        async def validator(
                zone_id: int,
                self: ZoneAccessService = Depends(cls)
        ):
            zone_creator_id = await self.zone_repository.get_creator_id(zone_id=zone_id)
            if zone_creator_id != self.current_user.id:
                raise AuthException()

        return Depends(validator)

    @classmethod
    def validate_update(cls):
        async def validator(
                zone_id: int,
                self: ZoneAccessService = Depends(cls)
        ):
            zone_creator_id = await self.zone_repository.get_creator_id(zone_id)
            if zone_creator_id != self.current_user.id:
                raise AuthException()

        return Depends(validator)

    @classmethod
    def validate_delete(cls):
        async def validator(
                zone_id: int,
                self: ZoneAccessService = Depends(cls)
        ):
            zone_creator_id = await self.zone_repository.get_creator_id(zone_id)
            if zone_creator_id != self.current_user.id:
                raise AuthException()

        return Depends(validator)


