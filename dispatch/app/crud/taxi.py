import typing as t

from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.schemas.taxi import TaxiPostRequest
from app.models import TaxiModel


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
            raise HTTPException(
                status_code=404,
                detail=f"Taxi.ID: `{id_}` not found.",
            )
        return item
    
    async def create_taxi(self, request_body: TaxiPostRequest):
        item = TaxiModel.create(
            id=request_body.id,
            callback_url=request_body.callback_url,
            available=request_body.available,
            x=request_body.x,
            y=request_body.y,
        )
        await self.save(item)
        return item

    async def save(self, entity: TaxiModel) -> None:
        self.session.add(entity)
        await self.session.flush()
