from fastapi import APIRouter, Depends, Header
from sensor.services.sensor import SensorService
from sensor.dependencies import validate_token
from sensor.schemas.sensor import SensorDataSchema
from sensor.services.admin import AdminAPIService

router = APIRouter(prefix="/sensors_data", tags=["Sensor"])


@router.post('')
async def store_data(data: SensorDataSchema, service: SensorService = Depends()):
    return await service.store(data)

