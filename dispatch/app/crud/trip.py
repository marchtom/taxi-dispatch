from datetime import datetime, timezone

from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.schemas.trip import TripPatchRequest, TripPostRequest
from app.models import TripModel


class TripCrud:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def get_by_id(self, id_: str) -> TripModel:
        query = select(TripModel).where(TripModel.id == id_)
        result = await self.session.execute(query)
        item: TripModel | None = result.scalars().first()
        if not item:
            raise HTTPException(
                status_code=404,
                detail=f"Trip.ID: `{id_}` not found.",
            )
        return item
    
    async def create_trip(self, request_body: TripPostRequest) -> TripModel:
        item = TripModel.create(
            id=request_body.id,
            start_time=request_body.start_time,
            x_start=request_body.x_start,
            y_start=request_body.y_start,
            x_stop=request_body.x_stop,
            y_stop=request_body.y_stop,
        )
        await self.save(item)
        return item
    
    async def update_trip(
        self, id_: str, request_body: TripPatchRequest
    ) -> TripModel:
        item = await self.get_by_id(id_)
        item.end_time = request_body.end_time or datetime.now(tz=timezone.utc)
        await self.save(item)
        return item

    async def save(self, entity: TripModel) -> None:
        self.session.add(entity)
        await self.session.flush()
