from fastapi import Depends
import random
import string
from loguru import logger

from admin.db.redis import get_redis_session


class AuthRepository:
    RESTORE_CODE_LETTERS = string.ascii_uppercase + string.digits
    RESTORE_CODE_LENGTH = 6
    RESTORE_CODE_LIFETIME = 30 * 60  # In seconds

    def __init__(self, redis_session=Depends(get_redis_session)):
        self.redis_session = redis_session

    async def _save_redis(self, key: str, value: str, expire: int | None = None):
        await self.redis_session.set(key, value, ex=expire)

    async def _get_redis(self, key: str) -> str | None:
        resp = await self.redis_session.get(key)
        if isinstance(resp, bytes):
            resp = resp.decode()
        return resp

    async def _delete_redis(self, key: str):
        await self.redis_session.delete(key)

    async def _generate_restore_code(self):
        while await self._get_redis(
                code := ''.join(random.choices(self.RESTORE_CODE_LETTERS, k=self.RESTORE_CODE_LENGTH))
                ) is not None:
            pass
        return code

    async def generate_restore_code(self, user_email: str) -> str:
        code = await self._generate_restore_code()
        await self._save_redis(code, user_email, self.RESTORE_CODE_LIFETIME)

    async def validate_restore_code(self, user_email: str, code: str) -> bool:
        valid_email = await self._get_redis(code)
        return valid_email is not None and valid_email == user_email

    async def delete_restore_code(self, code: str):
        await self._delete_redis(code)

