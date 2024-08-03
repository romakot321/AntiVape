from contextlib import asynccontextmanager

from fastapi import Depends, APIRouter

from admin.db.tables import User
from admin.schemas.auth import AuthUserCreateSchema, AuthUserReadSchema, AuthUserUpdateSchema
from admin.services.auth import (
    SECRET,
    auth_backend,
    fastapi_users,
)
from admin.dependencies import get_current_user


router = APIRouter(prefix="/api/auth", tags=["Auth"])

router.include_router(
    fastapi_users.get_auth_router(auth_backend)
)
router.include_router(
    fastapi_users.get_register_router(AuthUserReadSchema, AuthUserCreateSchema),
)


@router.get("/me", response_model=AuthUserReadSchema)
async def get_user_by_token(user: User = Depends(get_current_user)):
    return user

