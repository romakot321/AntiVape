from pydantic import BaseModel, computed_field
import json
import datetime as dt


class SensorDataSchema(BaseModel):
    sensor_guid: str
    co2: int
    tvoc: int
    battery_charge: int
    created_at: dt.datetime

    @classmethod
    def from_redis(cls, key, value):
        sensor_guid, timestamp = key.split(':')
        data = json.loads(value)
        return cls(
            sensor_guid=sensor_guid,
            created_at=dt.datetime.fromtimestamp(float(timestamp)),
            co2=data['co2'],
            tvoc=data['tvoc'],
            battery_charge=data['battery_charge']
        )
