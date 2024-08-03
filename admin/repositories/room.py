from sqlalchemy import select

from .base import BaseRepository
from admin.db.tables import Room


class RoomRepository(BaseRepository):
    base_table = Room

    async def create(self, model: Room) -> Room:
        return await self._create(model)

    async def get_one(self, room_id: int) -> Room:
        filters = {k: v for k, v in (('id', room_id),) if v is not None}
        return await self._get_one(**filters, select_in_load=[Room.zone, Room.sensors])

    async def get_many(self, zone_id: int | None = None, **filters) -> list[Room]:
        filters |= {k: v for k, v in (('zone_id', zone_id),) if v is not None}
        return list(await self._get_many(**filters))

    async def update(self, room_id: int, **fields) -> Room:
        return await self._update(room_id, **fields)

    async def delete(self, room_id: int) -> None:
        await self._delete(room_id)

    async def get_creator_id(self, room_id: int) -> int | None:
        query = select(Room.creator_id).filter_by(id=room_id)
        return await self.session.scalar(query)

