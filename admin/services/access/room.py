from fastapi import Depends

from admin.db.base import get_session, AsyncSession
from admin.db.tables import User, Room

from admin.dependencies import get_current_user
from admin.exceptions import AuthException
from admin.repositories.zone import ZoneRepository
from admin.repositories.room import RoomRepository

from admin.schemas.room import RoomCreateSchema
from admin.schemas.room import RoomFiltersSchema


class RoomAccessService:
    def __init__(
            self,
            zone_repository: ZoneRepository = Depends(),
            room_repository: RoomRepository = Depends(),
            current_user: User = Depends(get_current_user)
    ):
        self.zone_repository = zone_repository
        self.room_repository = room_repository
        self.current_user = current_user

    async def filter_get_many_response(
            self, rooms: list[Room]
    ) -> list[Room]:
        if self.current_user.is_superuser:
            return rooms
        for i in range(len(rooms)):
            if rooms[i].owner_id != self.current_user.id:
                rooms[i] = None
        return list(filter(lambda i: i is not None, rooms))

    @classmethod
    def validate_get_one(cls):
        async def validator(
                room_id: int,
                self: RoomAccessService = Depends(cls)
        ):
            if self.current_user.is_superuser:
                return
            room_owner_id = await self.room_repository.get_owner_id(room_id)
            if room_owner_id != self.current_user.id:
                raise AuthException()

        return Depends(validator)

    @classmethod
    def validate_get_many(cls):
        async def validator(
                filters: RoomFiltersSchema = Depends(),
                self: RoomAccessService = Depends(cls)
        ):
            if filters.owner_id is not None and not self.current_user.is_superuser:
                raise AuthException()

        return Depends(validator)

    @classmethod
    def _get_base_validator(cls):
        async def validator(
                self: RoomAccessService = Depends(cls)
        ):
            if not self.current_user.is_superuser:
                raise AuthException()

        return Depends(validator)

    @classmethod
    def validate_create(cls):
        return cls._get_base_validator()

    @classmethod
    def validate_update(cls):
        return cls._get_base_validator()

    @classmethod
    def validate_delete(cls):
        return cls._get_base_validator()

