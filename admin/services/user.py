from fastapi import Depends
from loguru import logger

from admin.schemas.user import UserShortSchema, UserFiltersSchema
from admin.repositories.user import UserRepository
from admin.repositories.sensor import SensorRepository
from admin.db.tables import User


class UserService:
    def __init__(
            self,
            repository: UserRepository = Depends(),
            sensor_repository: SensorRepository = Depends(),
    ):
        self.repository = repository
        self.sensor_repository = sensor_repository

    async def get_many(self, filters: UserFiltersSchema) -> list[UserShortSchema]:
        filters = filters.model_dump(exclude_none=True)
        models = await self.repository.get_many(select_in_load=User.sensors, **filters)
        return [
            UserShortSchema.model_validate(model)
            for model in models
        ]

