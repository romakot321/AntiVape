from pydantic import BaseModel, ConfigDict

from .base import BaseFiltersSchema


class SensorCreateSchema(BaseModel):
    guid: str
    room_id: int | None = None


class SensorUpdateSchema(BaseModel):
    room_id: int | None = None


class SensorGetSchema(BaseModel):
    room_id: int | None
    guid: str
    id: int

    model_config = ConfigDict(from_attributes=True)


class SensorShortSchema(BaseModel):
    id: int
    room_id: int | None
    guid: str

    model_config = ConfigDict(from_attributes=True)


class SensorFiltersSchema(BaseFiltersSchema):
    room_id: int | None = None

