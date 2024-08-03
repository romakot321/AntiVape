from pydantic import BaseModel, ConfigDict

from admin.schemas.room import RoomShortSchema
from .base import BaseFiltersSchema


class ZoneGetSchema(BaseModel):
    id: int
    name: str
    rooms: list[RoomShortSchema]

    model_config = ConfigDict(from_attributes=True)


class ZoneCreateSchema(BaseModel):
    name: str


class ZoneShortSchema(BaseModel):
    id: int
    name: str

    model_config = ConfigDict(from_attributes=True)


class ZoneFiltersSchema(BaseFiltersSchema):
    name: str | None = None


class ZoneUpdateSchema(BaseModel):
    name: str | None = None

