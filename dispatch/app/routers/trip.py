from fastapi import APIRouter

from app.dependencies import TripCrudDep
from app.schemas.trip import TripGetRequest, TripPostRequest, TripPostResponse


router = APIRouter(
    prefix="/trip",
    tags=["trip"],
)


@router.get(
    r"/{id_}",
    response_model=TripGetRequest,
    description="Get info about a single trip",
)
async def get_trip(id_: str, crud: TripCrudDep) -> TripGetRequest:
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
