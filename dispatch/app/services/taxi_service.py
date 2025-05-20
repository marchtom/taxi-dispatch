from urllib.parse import urljoin

import httpx

from app.models import TaxiModel, TripModel


class TaxiService:
    """Class for communication with taxies."""

    async def order_trip(
        self,
        taxi: TaxiModel,
        trip: TripModel,
    ) -> None:
        async with httpx.AsyncClient() as client:
            await client.post(
                urljoin(taxi.callback_url, "trip"),
                json={
                    "x_start": trip.x_start,
                    "y_start": trip.y_start,
                    "x_stop": trip.x_stop,
                    "y_stop": trip.y_stop,
                },
            )
