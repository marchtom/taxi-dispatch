import logging

from fastapi import APIRouter

from app.dependencies import TaxiCrudDep, TripCrudDep
from app.schemas.event import EventPostRequest, EventPostResponse


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


router = APIRouter(
    prefix="/event",
    tags=["event"],
)


@router.post(
    "/picked",
    response_model=EventPostResponse,
    description="Notifies Dispatch about client pick up",
)
async def trip_event(
    request_body: EventPostRequest,
) -> EventPostResponse:
    logger.info(f"Client picked up by: {request_body.taxi_id}")
    return EventPostResponse(message="ok")


@router.post(
    "/dropped",
    response_model=EventPostResponse,
    description="Notifies Dispatch about client drop off",
)
async def trip_event(
    request_body: EventPostRequest,
    crud_taxi: TaxiCrudDep,
    crud_trip: TripCrudDep,
) -> EventPostResponse:
    logger.info(f"Client dropped off by: {request_body.taxi_id}")
    trip = await crud_trip.get_ongoing_by_taxi_id(request_body.taxi_id)
    await crud_taxi.update_status(
        id_=request_body.taxi_id,
        new_x=trip.x_stop,
        new_y=trip.y_stop,
    )
    await crud_trip.finalize_trip(trip.id)
    return EventPostResponse(message="ok")
