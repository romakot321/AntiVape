from fastapi import Depends

from admin.db.base import AsyncSession, get_session
from admin.db.tables import User
from admin.services.auth import fastapi_users

get_current_user = fastapi_users.current_user(active=True)


