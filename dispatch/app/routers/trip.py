from fastapi import APIRouter

from app.dependencies import TripCrudDep
from app.schemas.trip import (
    TripGetResponse,
    TripPatchRequest,
    TripPatchResponse,
    TripPostRequest,
    TripPostResponse,
)


router = APIRouter(
    prefix="/trip",
    tags=["trip"],
)


@router.get(
    r"/{id_}",
    response_model=TripGetResponse,
    description="Get info about a single trip",
)
async def get_trip(id_: str, crud: TripCrudDep) -> TripGetResponse:
    return await crud.get_by_id(id_)


@router.post(
    "",
    response_model=TripPostResponse,
    description="Order a new taxi trip",
)
async def create_trip(
    request_body: TripPostRequest,
    crud: TripCrudDep,
) -> TripPostResponse:
    return await crud.create_trip(request_body)


@router.patch(
    r"/{id_}",
    response_model=TripPatchResponse,
    description="Update existing trip",
)
async def update_trip(
    id_: str,
    request_body: TripPatchRequest,
    crud: TripCrudDep,
) -> TripPatchResponse:
    return await crud.update_trip(id_, request_body)
