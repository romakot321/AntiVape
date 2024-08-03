from pydantic import BaseModel


class SensorDataSchema(BaseModel):
    data: str
    sensor_info: str = ''

