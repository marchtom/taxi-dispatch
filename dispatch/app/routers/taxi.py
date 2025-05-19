from fastapi import APIRouter

from app.dependencies import TaxiCrudDep
from app.schemas.taxi import TaxiPostRequest, TaxiPostResponse, TaxiGetRequest


router = APIRouter(
    prefix="/taxi",
    tags=["taxi"],
)


@router.get(
    "",
    response_model=list[TaxiGetRequest],
    description="Get list of all taxies"
)
async def list_taxi(crud: TaxiCrudDep) -> list[TaxiGetRequest]:
    return await crud.get_all()


@router.get(
    r"/{id_}",
    response_model=TaxiGetRequest,
    description="Get info about a single taxi"
)
async def get_taxi(id_: str, crud: TaxiCrudDep) -> TaxiGetRequest:
    return await crud.get_by_id(id_)


@router.post(
    "",
    response_model=TaxiPostResponse,
    description="Register (create) new taxi"
)
async def create_taxi(
    request_body: TaxiPostRequest,
    crud: TaxiCrudDep,
) -> TaxiPostResponse:
    return await crud.create_taxi(request_body)
