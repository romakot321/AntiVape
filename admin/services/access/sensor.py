from fastapi import Depends

from admin.db.base import get_session, AsyncSession
from admin.db.tables import User, Sensor

from admin.dependencies import get_current_user
from admin.exceptions import AuthException
from admin.repositories.room import RoomRepository
from admin.repositories.sensor import SensorRepository

from admin.schemas.sensor import SensorCreateSchema
from admin.schemas.sensor import SensorFiltersSchema


class SensorAccessService:
    def __init__(
            self,
            room_repository: RoomRepository = Depends(),
            sensor_repository: SensorRepository = Depends(),
            current_user: User = Depends(get_current_user)
    ):
        self.room_repository = room_repository
        self.sensor_repository = sensor_repository
        self.current_user = current_user

    async def filter_get_many_response(
            self, sensors: list[Sensor]
    ) -> list[Sensor]:
        if self.current_user.is_superuser:
            return sensors
        for i in range(len(sensors)):
            if sensors[i].owner_id != self.current_user.id:
                sensors[i] = None
        return list(filter(lambda i: i is not None, sensors))

    @classmethod
    def validate_get_one(cls):
        async def validator(
                id_or_guid: str,
                self: SensorAccessService = Depends(cls)
        ):
            if self.current_user.is_superuser:
                return

            sensor_guid, sensor_id = None, None
            if id_or_guid.isnumeric():
                sensor_id = int(id_or_guid)
            else:
                sensor_guid = id_or_guid

            sensor_owner_id = await self.sensor_repository.get_owner_id(sensor_id=sensor_id, sensor_guid=sensor_guid)
            if sensor_owner_id != self.current_user.id:
                raise AuthException()

        return Depends(validator)

    @classmethod
    def validate_get_many(cls):
        async def validator(
                filters: SensorFiltersSchema = Depends(),
                self: SensorAccessService = Depends(cls)
        ):
            if filters.owner_id is not None and not self.current_user.is_superuser:
                raise AuthException()

        return Depends(validator)

    @classmethod
    def _get_base_validator(cls):
        async def validator(
                self: SensorAccessService = Depends(cls)
        ):
            if not self.current_user.is_superuser:
                raise AuthException()

        return Depends(validator)

    @classmethod
    def validate_update(cls):
        return cls._get_base_validator()

    @classmethod
    def validate_delete(cls):
        return cls._get_base_validator()

    @classmethod
    def validate_create(cls):
        return cls._get_base_validator()

