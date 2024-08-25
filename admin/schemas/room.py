from pydantic import BaseModel, ConfigDict
import datetime as dt

from admin.schemas.sensor import SensorShortSchema
from admin.schemas.sensor_data import SensorDataSchema
from .base import BaseFiltersSchema


class RoomGetSchema(BaseModel):
    id: int
    name: str
    zone_id: int
    owner_id: int
    sensors: list[SensorShortSchema]

    model_config = ConfigDict(from_attributes=True)


class RoomCreateSchema(BaseModel):
    name: str
    zone_id: int
    owner_id: int


class RoomShortSchema(BaseModel):
    id: int
    name: str
    zone_id: int
    owner_id: int

    model_config = ConfigDict(from_attributes=True)


class RoomFiltersSchema(BaseFiltersSchema):
    zone_id: int | None = None
    name: str | None = None
    owner_id: int | None = None


class RoomUpdateSchema(BaseModel):
    name: str | None = None


class RoomStatisticFiltersSchema(BaseModel):
    from_datetime: dt.datetime | None = None
    to_datetime: dt.datetime | None = None


class RoomStatisticGetSchema(BaseModel):
    data: list[SensorDataSchema]

