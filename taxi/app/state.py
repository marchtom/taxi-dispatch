import asyncio
import logging
import os
import random

import httpx

from app.config import settings
from app.schemas.trip import TripPostRequest


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

DISPATCH_URL = os.environ["DISPATCH_URL"]


class TaxiState:
    def __init__(
        self,
        available: bool = True,
        x: int = 0,
        y: int = 0,
    ) -> None:
        self._available = available
        self.x = x
        self.y = y

        self._speed_lower_boundary = settings.speed_min
        self._speed_upper_boundary = settings.speed_max

        self._taxi_id = None

    @property
    def taxi_id(self) -> str:
        if self._taxi_id is None:
            raise AttributeError("`taxi_id` not initialized")
        return self._taxi_id

    @taxi_id.setter
    def taxi_id(self, value) -> None:
        self._taxi_id = value

    @property
    def is_available(self) -> bool:
        return self._available

    @property
    def is_busy(self) -> bool:
        return not self._available

    @property
    def current_position(self) -> dict[str, int]:
        return {
            "x": self.x,
            "y": self.y,
        }

    def randomize_state(self, seed: int | None = None) -> None:
        random.seed(seed)

        self.x = random.randint(1, 100)
        self.y = random.randint(1, 100)

        self.available = random.choice([True, False])

        if not self.available:
            delay = random.uniform(5, 30)
            logger.info(
                f"Taxi will be available in: {delay:.1f} s"
            )
            asyncio.create_task(self._delayed_mark_available(delay))

        random.seed(None)

    async def _delayed_mark_available(self, delay: float) -> None:
        await asyncio.sleep(delay)
        self.mark_available()
        await self.notify_dispatch_availability_change(available=True)

    def mark_busy(self) -> None:
        self._available = False

    def mark_available(self) -> None:
        self._available = True

    async def move_to(self, target_x: int, target_y: int) -> None:
        while (self.x, self.y) != (target_x, target_y):
            # Simulate travel time with sleep
            travel_time = random.uniform(
                self._speed_lower_boundary,
                self._speed_upper_boundary,
            )
            await asyncio.sleep(travel_time)

            # Get distance differences
            dx = target_x - self.x
            dy = target_y - self.y

            # For simplicity: let's start with traveling along x-axis
            if dx != 0:
                # Determine step direction from difference sign
                sign = 1 if dx > 0 else -1
                self.x += 1 * sign
            else:
                sign = 1 if dy > 0 else -1
                self.y += 1 * sign

            logger.info(f"Moved to ({self.x}, {self.y})")

    async def handle_trip(self, trip: TripPostRequest) -> None:
        await self.move_to(trip.x_start, trip.y_start)
        await self.notify_dispatch_picked()

        await self.move_to(trip.x_stop, trip.y_stop)
        await self.notify_dispatch_dropped()

        self.mark_available()

    async def notify_dispatch_picked(self) -> None:
        async with httpx.AsyncClient() as client:
            try:
                await client.post(
                    f"{DISPATCH_URL}/event/picked",
                    json={"taxi_id": self.taxi_id},
                )
            except httpx.HTTPError as e:
                logger.error(
                    f"Failed to notify Dispatch about pick up: {e}",
                    exc_info=True,
                )

    async def notify_dispatch_dropped(self) -> None:
        async with httpx.AsyncClient() as client:
            try:
                await client.post(
                    f"{DISPATCH_URL}/event/dropped",
                    json={"taxi_id": self.taxi_id},
                )
            except httpx.HTTPError as e:
                logger.error(
                    f"Failed to notify Dispatch about drop off: {e}",
                    exc_info=True,
                )

    async def notify_dispatch_availability_change(self, available: bool) -> None:
        async with httpx.AsyncClient() as client:
            try:
                await client.patch(
                    f"{DISPATCH_URL}/taxi/{self.taxi_id}",
                    json={"available": available},
                )
            except httpx.HTTPError as e:
                logger.error(
                    f"Failed to notify Dispatch about change: {e}",
                    exc_info=True,
                )


_TAXI_STATE = TaxiState()


def get_taxi_state() -> TaxiState:
    return _TAXI_STATE
