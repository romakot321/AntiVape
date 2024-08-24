from fastapi import Depends

from admin.schemas.user import UserShortSchema, UserFiltersSchema
from admin.repositories.user import UserRepository
from admin.db.tables import User


class UserService:
    def __init__(
            self,
            repository: UserRepository = Depends(),
    ):
        self.repository = repository

    async def get_many(self, filters: UserFiltersSchema) -> list[UserShortSchema]:
        filters = filters.model_dump(exclude_none=True)
        models = await self.repository.get_many(**filters)
        return [
            UserShortSchema.model_validate(model)
            for model in models
        ]

