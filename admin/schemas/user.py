from pydantic import BaseModel, ConfigDict, model_validator

from .base import BaseFiltersSchema


class UserShortSchema(BaseModel):
    id: int
    name: str | None = None
    sensors_count: int

    model_config = ConfigDict(from_attributes=True)


class UserFiltersSchema(BaseFiltersSchema):
    pass

