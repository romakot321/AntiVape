from fastapi import FastAPI
from fastapi import status
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic_settings import BaseSettings
from loguru import logger


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


def init_web_application():
    project_settings = ProjectSettings()
    application = FastAPI(
        openapi_url='/api/openapi.json',
        docs_url='/api/docs',
        redoc_url='/api/redoc'
    )

    if project_settings.LOCAL_MODE:
        register_exception(application)
        register_cors(application)

    from admin.routes.sensor import router as sensor_router
    from admin.routes.room import router as room_router
    from admin.routes.zone import router as zone_router
    from admin.routes.auth import router as auth_router
    from admin.routes.user import router as user_router

    application.include_router(auth_router)
    application.include_router(zone_router)
    application.include_router(room_router)
    application.include_router(sensor_router)
    application.include_router(user_router)

    from sensor.main import init_web_application as init_sensor_app

    application.mount('/api/external', init_sensor_app(application))

    return application


def run() -> FastAPI:
    application = init_web_application()
    return application


fastapi_app = run()
