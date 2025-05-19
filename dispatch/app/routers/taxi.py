import logging

from fastapi import APIRouter

from app.dependencies import TaxiCrudDep
from app.schemas.taxi import TaxiPostRequest, TaxiPostResponse, TaxiGetRequest


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


router = APIRouter(
    prefix="/taxi",
    tags=["taxi"],
)


@router.get(
    "",
    response_model=list[TaxiGetRequest],
)
async def list_taxi(crud: TaxiCrudDep) -> list[TaxiGetRequest]:
    items = await crud.get_all()
    return items


@router.get(
    r"/{id_}",
    response_model=TaxiGetRequest,
)
async def get_taxi(id_: str, crud: TaxiCrudDep) -> TaxiGetRequest:
    item = await crud.get_by_id(id_)
    return item


@router.post(
    "",
    response_model=TaxiPostResponse,
)
async def create_taxi(
    request_body: TaxiPostRequest,
    crud: TaxiCrudDep,
) -> TaxiPostResponse:
    item = await crud.create_taxi(request_body)
    return TaxiPostResponse(id=item.id)
