from fastapi import APIRouter, Depends

from admin.schemas.user import UserShortSchema
from admin.schemas.user import UserFiltersSchema
from admin.services.user import UserService
from admin.db.tables import User
from admin.dependencies import get_current_superuser

router = APIRouter(prefix="/api/user", tags=["User"])


@router.get('', response_model=list[UserShortSchema])
async def get_users(
        filters: UserFiltersSchema = Depends(),
        service: UserService = Depends(),
        _: User = Depends(get_current_superuser)
):
    """Get users list, access only for admin/superuser"""
    return await service.get_many(filters)

