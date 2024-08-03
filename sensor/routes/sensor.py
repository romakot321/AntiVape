from fastapi import APIRouter, Depends, Header
from sensor.services.sensor import SensorService
from sensor.dependencies import validate_token

router = APIRouter(prefix="/sensor/sensor", tags=["Sensor"])


@router.post('')
async def store_data(data: str, service: SensorService = Depends()):
    return await service.store(data)

