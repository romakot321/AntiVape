from sqlalchemy import select

from .base import BaseRepository
from admin.db.tables import Zone


class ZoneRepository(BaseRepository):
    base_table = Zone

    async def create(self, model: Zone) -> Zone:
        return await self._create(model)

    async def get_one(self, zone_id: int) -> Zone:
        filters = {k: v for k, v in (('id', zone_id),) if v is not None}
        return await self._get_one(**filters, select_in_load=Zone.rooms)

    async def get_many(self, **filters) -> list[Zone]:
        return list(await self._get_many(**filters))

    async def update(self, zone_id: int, **fields) -> Zone:
        return await self._update(zone_id, **fields)

    async def delete(self, zone_id: int) -> None:
        await self._delete(zone_id)

    async def get_creator_id(self, zone_id: int) -> int | None:
        query = select(Zone.creator_id).filter_by(id=zone_id)
        return await self.session.scalar(query)


