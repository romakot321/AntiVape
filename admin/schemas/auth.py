import uuid
from fastapi_users import schemas
from pydantic import BaseModel


class AuthUserReadSchema(schemas.BaseUser[int]):
    pass


class AuthUserCreateSchema(schemas.BaseUserCreate):
    pass


class AuthUserUpdateSchema(schemas.BaseUserUpdate):
    pass


class AuthPasswordRestoreSchema(BaseModel):
    email: str
    restore_code: str | None = None
    new_password: str | None = None

