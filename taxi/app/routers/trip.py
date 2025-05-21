import asyncio

from fastapi import APIRouter, Depends, HTTPException, status

from app.schemas.trip import TripPostRequest, TripPostResponse
from app.state import get_taxi_state, TaxiState

router = APIRouter(
    prefix="/trip",
    tags=["trip"],
)


@router.post(
    "",
    response_model=TripPostResponse,
    description="Order a new taxi trip",
)
async def create_trip(
    request_body: TripPostRequest,
    taxi_state: TaxiState = Depends(get_taxi_state),
) -> TripPostResponse:
    if taxi_state.is_busy:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Taxi is busy, try again later.",
        )

    taxi_state.mark_busy()
    asyncio.create_task(taxi_state.handle_trip(request_body))

    return TripPostResponse(message="ok")
