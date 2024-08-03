from pydantic import BaseModel, AliasChoices, Field


class SensorDataSchema(BaseModel):
    guid: str
    co2: int
    tvoc: int
    battery_charge: int = Field(validation_alias=AliasChoices('battery_charge', 'batteryCharge'))

