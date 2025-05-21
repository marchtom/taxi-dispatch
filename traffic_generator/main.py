import asyncio
import logging
import os
import random

import httpx
from dotenv import load_dotenv

load_dotenv()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


DISPATCH_URL = os.environ["DISPATCH_URL"]
INTERVAL_SECONDS = float(os.environ["INTERVAL_SECONDS"])
REQUEST_BATCH_SIZE = int(os.getenv("INTERVAL_SECONDS", 1))


def generate_random_trip() -> dict:
    return {
        "x_start": random.randint(1, 100),
        "y_start": random.randint(1, 100),
        "x_stop": random.randint(1, 100),
        "y_stop": random.randint(1, 100),
    }


async def send_trip():
    trip = generate_random_trip()
    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(f"{DISPATCH_URL}/trip", json=trip)
            logger.info(f"Sent trip: {trip}, response status: {response.status_code}")
        except httpx.HTTPError as e:
            logger.error(
                f"Failed to send trip: {e}",
                exc_info=True,
            )


async def main():
    # let other services start
    await asyncio.sleep(10)

    while True:
        await asyncio.gather(*[send_trip() for _ in range(REQUEST_BATCH_SIZE)])
        await asyncio.sleep(INTERVAL_SECONDS)


if __name__ == "__main__":
    asyncio.run(main())
