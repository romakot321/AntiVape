from contextlib import asynccontextmanager

from fastapi import Depends, APIRouter, Response

from admin.db.tables import User
from admin.schemas.auth import AuthUserCreateSchema, AuthUserReadSchema, AuthUserUpdateSchema
from admin.schemas.auth import AuthPasswordRestoreSchema
from admin.services.auth import (
    SECRET,
    auth_backend,
    fastapi_users,
)
from admin.services.auth import AuthService
from admin.dependencies import get_current_user


router = APIRouter(prefix="/api/auth", tags=["Auth"])

router.include_router(
    fastapi_users.get_auth_router(auth_backend)
)
router.include_router(
    fastapi_users.get_register_router(AuthUserReadSchema, AuthUserCreateSchema),
)
router.include_router(
    fastapi_users.get_users_router(AuthUserReadSchema, AuthUserUpdateSchema),
    prefix="/user"
)


@router.get("/me", response_model=AuthUserReadSchema)
async def get_user_by_token(user: User = Depends(get_current_user)):
    return user


@router.put(
    '/restore',
    description="""
    email only = send restore code to email.
    email + restore_code = validate restore code.
    email + restore_code + new_password = set new password.
    """
)
async def request_password_restore(
        schema: AuthPasswordRestoreSchema,
        response: Response,
        service: AuthService = Depends()
):
    await service.process_restore_request(schema, response)

