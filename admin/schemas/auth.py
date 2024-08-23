import uuid
from fastapi_users import schemas
from pydantic import BaseModel


class AuthUserReadSchema(schemas.BaseUser[int]):
    name: str | None = None

class AuthUserCreateSchema(schemas.BaseUserCreate):
    name: str | None = None


class AuthUserUpdateSchema(schemas.BaseUserUpdate):
    name: str | None = None


class AuthPasswordRestoreSchema(BaseModel):
    email: str
    restore_code: str | None = None
    new_password: str | None = None

