from fastapi import FastAPI
from fastapi import status
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi_utils.tasks import repeat_every
from pydantic_settings import BaseSettings
from loguru import logger
from sensor.services.admin import AdminAPIService


class ProjectSettings(BaseSettings):
    LOCAL_MODE: bool = False


def register_exception(application):
    @application.exception_handler(RequestValidationError)
    async def validation_exception_handler(request, exc):
        exc_str = f'{exc}'.replace('\n', ' ').replace('   ', ' ')
        # or logger.error(f'{exc}')
        logger.debug(f'{exc}')
        content = {'status_code': 422, 'message': exc_str, 'data': None}
        return JSONResponse(
            content=content, status_code=status.HTTP_422_UNPROCESSABLE_ENTITY
        )


def register_cors(application):
    application.add_middleware(
        CORSMiddleware,
        allow_origins=['*'],
        allow_credentials=True,
        allow_methods=['*'],
        allow_headers=['*'],
    )


def init_web_application(admin_app: FastAPI):
    project_settings = ProjectSettings()
    application = FastAPI(
        openapi_url='/openapi.json',
        docs_url='/docs',
        redoc_url='/redoc'
    )

    if project_settings.LOCAL_MODE:
        register_exception(application)
        register_cors(application)

    from sensor.routes.sensor import router as sensor_router

    application.include_router(sensor_router)

    @repeat_every(seconds=15)
    async def transfer_task():
        try:
            await AdminAPIService.transfer_sensors_data()
        except Exception as e:
            logger.exception(e)

    admin_app.add_event_handler("startup", transfer_task)

    return application

