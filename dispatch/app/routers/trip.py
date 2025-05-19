import logging

from fastapi import APIRouter
from fastapi.responses import Response

from app.dependencies import TripCrudDep
from app.schemas.trip import TripGetRequest, TripPostRequest


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


router = APIRouter(
    prefix="/trip",
    tags=["trip"],
)


@router.get(
    r"/{id_}",
    response_model=TripGetRequest,
)
async def get_trip(id_: str, crud: TripCrudDep) -> TripGetRequest:
    item = await crud.get_by_id(id_)
    return item


@router.post(
    "",
    description="Order a new taxi trip",
    status_code=204,
)
async def create_trip(
    request_body: TripPostRequest,
    crud: TripCrudDep,
) -> Response:
    await crud.create_trip(request_body)
    return Response(status_code=204)
