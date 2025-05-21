import typing as t

from fastapi import HTTPException, status
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.schemas.taxi import TaxiPostRequest, TaxiPatchRequest
from app.models import TaxiModel, TripModel


class TaxiCrud:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def get_all(self) -> t.Sequence[TaxiModel] | None:
        results = await self.session.execute(select(TaxiModel))
        items: t.Sequence[TaxiModel] | None = results.scalars().all()
        return items

    async def get_by_id(self, id_: str) -> TaxiModel:
        query = select(TaxiModel).where(TaxiModel.id == id_)
        result = await self.session.execute(query)
        item: TaxiModel | None = result.scalars().first()
        if not item:
            # TODO: Create custom Error for missing items
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Taxi.ID: `{id_}` not found.",
            )
        return item

    async def create_taxi(self, request_body: TaxiPostRequest) -> TaxiModel:
        item = TaxiModel.create(
            id=request_body.id,
            callback_url=request_body.callback_url,
            available=request_body.available,
            x=request_body.x,
            y=request_body.y,
        )
        await self.save(item)
        return item

    async def update_taxi(self, id_: str, request_body: TaxiPatchRequest) -> None:
        item = await self.get_by_id(id_)
        item.available = request_body.available
        await self.save(item)

    # TODO: create BaseCrud and move self.save() there
    async def save(self, entity: TaxiModel | TripModel) -> None:
        self.session.add(entity)
        await self.session.commit()

    async def find_available(self, trip: TripModel) -> TaxiModel:
        """Finds the most suitable taxi for the trip."""
        manhattan_dist = func.abs(TaxiModel.x - trip.x_start) + func.abs(TaxiModel.y - trip.y_start)

        query = (
            select(TaxiModel).where(TaxiModel.available.is_(True)).order_by(manhattan_dist).limit(1)
        )
        result = await self.session.execute(query)
        item: TaxiModel | None = result.scalars().first()
        if not item:
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail="We are sorry, all the taxies are busy at the moment.",
            )

        # Book taxi for the trip
        # TODO: find a way to revert it if trip fails to start
        item.available = False
        await self.save(item)

        return item

    async def update_status(self, id_: str, new_x: int, new_y: int) -> None:
        item = await self.get_by_id(id_)
        item.available = True
        item.x = new_x
        item.y = new_y
        await self.save(item)
