import uuid
from typing import Optional

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import selectinload

from fastapi import Depends, Request, HTTPException, Response
from fastapi_users import BaseUserManager, IntegerIDMixin
from fastapi_users import FastAPIUsers
from fastapi_users.authentication import (
    AuthenticationBackend,
    BearerTransport,
    JWTStrategy,
)
from fastapi_users.password import PasswordHelper
from fastapi_users.db import SQLAlchemyUserDatabase

from admin.db.tables import User
from admin.db.base import get_session
from admin.repositories.user import UserRepository
from admin.repositories.auth import AuthRepository
from admin.services.email import send_forgot_password_mail
from admin.schemas.auth import AuthPasswordRestoreSchema

SECRET = "SECRET"

bearer_transport = BearerTransport(tokenUrl="/api/auth/login")


class AuthService:
    def __init__(
            self,
            user_repository: UserRepository = Depends(),
            auth_repository: AuthRepository = Depends()
    ):
        self.user_repository = user_repository
        self.auth_repository = auth_repository
        self.password_helper = PasswordHelper()

    def _hash_password(self, password: str) -> str:
        return self.password_helper.hash(password)

    async def _request_password_restore(self, user_email: str):
        if (await self.user_repository.get_one(user_email=user_email, mute_not_found_exception=True)) is None:
            return
        code = await self.auth_repository.create_restore_code(user_email)
        await send_forgot_password_mail(user_email, code)

    async def _restore_password(self, restore_code: str, user_email: str, new_password: str):
        if not (await self.auth_repository.validate_restore_code(user_email, restore_code)):
            raise HTTPException(400)
        user = await self.user_repository.get_one(user_email=user_email)
        hashed_password = self._hash_password(new_password)
        await self.user_repository.update(user.id, hashed_password=hashed_password)
        await self.auth_repository.delete_restore_code(restore_code)

    async def _validate_restore_code(self, user_email, restore_code):
        if not (await self.auth_repository.validate_restore_code(user_email, restore_code)):
            raise HTTPException(400)

    async def process_restore_request(self, schema: AuthPasswordRestoreSchema, response: Response):
        if schema.restore_code is None:
            await self._request_password_restore(schema.email)
            response.status_code = 202
        elif schema.new_password is None:
            await self._validate_restore_code(schema.email, schema.restore_code)
            response.status_code = 200
        elif schema.new_password is not None:
            await self._restore_password(schema.restore_code, schema.email, schema.new_password)
            response.status_code = 204


class UserManager(IntegerIDMixin, BaseUserManager[User, int]):
    reset_password_token_secret = SECRET
    verification_token_secret = SECRET


class _AuthUserModel(SQLAlchemyUserDatabase):
    pass


def get_jwt_strategy() -> JWTStrategy:
    return JWTStrategy(secret=SECRET, lifetime_seconds=3600)


async def _get_user_db(session: AsyncSession = Depends(get_session)):
    yield _AuthUserModel(session, User)


async def get_user_manager(user_db: SQLAlchemyUserDatabase = Depends(_get_user_db)):
    yield UserManager(user_db)


auth_backend = AuthenticationBackend(
    name="jwt",
    transport=bearer_transport,
    get_strategy=get_jwt_strategy,
)

fastapi_users = FastAPIUsers[User, int](get_user_manager, [auth_backend])
