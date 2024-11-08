from pydantic import BaseModel, ConfigDict, Field

from .base import BaseFiltersSchema


class SensorCreateSchema(BaseModel):
    guid: str
    room_id: int | None = None
    owner_id: int


class SensorUpdateSchema(BaseModel):
    room_id: int | None = None


class SensorRoomZoneSchema(BaseModel):
    id: int
    name: str


class SensorRoomSchema(BaseModel):
    id: int
    name: str
    zone: SensorRoomZoneSchema


class SensorGetSchema(BaseModel):
    room: SensorRoomSchema | None = None
    guid: str
    id: int
    owner_id: int

    model_config = ConfigDict(from_attributes=True)


class SensorShortSchema(BaseModel):
    id: int
    room_id: int | None
    guid: str
    owner_id: int

    model_config = ConfigDict(from_attributes=True)


class SensorFiltersSchema(BaseFiltersSchema):
    room_id: int | None = None
    guid: str | None = None
    owner_id: int | None = None

