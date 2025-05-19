from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud import TaxiCrud, TripCrud
from app.db import get_db


async def get_taxi_crud(
    session: Annotated[AsyncSession, Depends(get_db)]
) -> TaxiCrud:
    return TaxiCrud(session)


async def get_trip_crud(
    session: Annotated[AsyncSession, Depends(get_db)]
) -> TripCrud:
    return TripCrud(session)


TaxiCrudDep = Annotated[TaxiCrud, Depends(get_taxi_crud)]
TripCrudDep = Annotated[TripCrud, Depends(get_trip_crud)]
