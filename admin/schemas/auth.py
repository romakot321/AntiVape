import uuid

from fastapi_users import schemas


class AuthUserReadSchema(schemas.BaseUser[int]):
    pass


class AuthUserCreateSchema(schemas.BaseUserCreate):
    pass


class AuthUserUpdateSchema(schemas.BaseUserUpdate):
    pass

