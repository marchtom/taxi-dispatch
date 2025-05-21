from fastapi import APIRouter

from app.dependencies import TaxiCrudDep
from app.schemas.taxi import (
    TaxiGetRequest,
    TaxiPatchRequest,
    TaxiPatchResponse,
    TaxiPostRequest,
    TaxiPostResponse,
)


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


@router.patch(
    r"/{id_}",
    response_model=TaxiPatchResponse,
    description="Taxi status update"
)
async def update_taxi(
    id_: str,
    request_body: TaxiPatchRequest,
    crud: TaxiCrudDep,
) -> TaxiPatchResponse:
    await crud.update_taxi(id_, request_body)
    return TaxiPatchResponse(message="ok")
