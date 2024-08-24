from fastapi import Depends, Header
from fastapi_users.jwt import SecretType, decode_jwt, generate_jwt
from loguru import logger

from admin.db.base import AsyncSession, get_session
from admin.db.tables import User
from admin.services.auth import fastapi_users, get_user_manager
from admin.services.auth import auth_backend, get_jwt_strategy

_strategy = get_jwt_strategy()
get_current_user = fastapi_users.current_user(active=True)
get_current_superuser = fastapi_users.current_user(active=True, superuser=True)


async def get_current_user_websocket(
        token: str,
        user_manager=Depends(get_user_manager)
):
    logger.debug(token)
    return await _strategy.read_token(token, user_manager)

