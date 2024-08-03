from pydantic import BaseModel, ConfigDict

from admin.schemas.sensor import SensorShortSchema
from .base import BaseFiltersSchema


class RoomGetSchema(BaseModel):
    id: int
    name: str
    zone_id: int
    sensors: list[SensorShortSchema]

    model_config = ConfigDict(from_attributes=True)


class RoomCreateSchema(BaseModel):
    name: str
    zone_id: int


class RoomShortSchema(BaseModel):
    id: int
    name: str
    zone_id: int

    model_config = ConfigDict(from_attributes=True)


class RoomFiltersSchema(BaseFiltersSchema):
    zone_id: int | None = None
    name: str | None = None


class RoomUpdateSchema(BaseModel):
    name: str | None = None

