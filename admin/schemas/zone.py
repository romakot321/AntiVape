from pydantic import BaseModel, ConfigDict, model_validator
import datetime as dt
from itertools import groupby
import operator

from admin.schemas.room import RoomShortSchema
from admin.schemas.sensor_data import SensorDataSchema
from .base import BaseFiltersSchema


class ZoneGetSchema(BaseModel):
    id: int
    name: str
    rooms: list[RoomShortSchema]
    active_sensors_count: int

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


class ZoneStatisticsFiltersSchema(BaseModel):
    from_datetime: dt.datetime | None = None
    to_datetime: dt.datetime | None = None

    def __hash__(self):
        return hash(str(self.from_datetime) + str(self.to_datetime))


class ZoneRoomSensorDataSchema(BaseModel):
    room_id: int
    co2: int
    tvoc: int


class ZoneStatisticsGetSchema(BaseModel):
    zone_id: int
    data: list[ZoneRoomSensorDataSchema]

    @model_validator(mode='before')
    @classmethod
    def from_list(cls, data):
        if not isinstance(data, dict):
            return data
        if data.get('data', []) and isinstance(data['data'][0], ZoneRoomSensorDataSchema):
            return data
        schemas = []
        for room_id, sensor_datas in groupby(data['data'], key=operator.attrgetter('sensor.room_id')):
            sensor_datas = list(sensor_datas)
            co2 = sum(map(lambda i: i.co2, sensor_datas)) / len(sensor_datas)
            tvoc = sum(map(lambda i: i.tvoc, sensor_datas)) / len(sensor_datas)
            schemas.append(ZoneRoomSensorDataSchema(co2=co2, tvoc=tvoc, room_id=room_id))
        data['data'] = schemas
        return data


class ZoneListStatisticsGetSchema(BaseModel):
    statistics: list[ZoneStatisticsGetSchema]

