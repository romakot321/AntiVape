from fastapi import Depends, Header
from fastapi_users.jwt import SecretType, decode_jwt, generate_jwt

from admin.db.base import AsyncSession, get_session
from admin.db.tables import User
from admin.services.auth import fastapi_users, get_user_manager
from admin.services.auth import auth_backend, get_jwt_strategy

_strategy = get_jwt_strategy()
get_current_user = fastapi_users.current_user(active=True)


async def get_current_user_websocket(
        authorization: str = Header(),
        user_manager=Depends(get_user_manager)
):
    authorization = authorization[7:]
    return await _strategy.read_token(authorization, user_manager)

