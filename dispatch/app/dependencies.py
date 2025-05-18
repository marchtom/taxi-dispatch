from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.taxi import TaxiCrud
from app.db import get_db


def get_taxi_crud(session: AsyncSession = Depends(get_db)) -> TaxiCrud:
    return TaxiCrud(session=session)


TaxiCrudDep = Annotated[TaxiCrud, Depends(get_taxi_crud)]
