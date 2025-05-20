import asyncio
import logging
import socket
import uuid
from contextlib import asynccontextmanager
from urllib.parse import urljoin

import httpx
from fastapi import FastAPI

from app.config import settings
from app.state import get_taxi_state


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(_: FastAPI):
    await asyncio.sleep(5)
    await initialize_taxi()
    yield
    # TODO: Add teardown call to dispatch here


async def initialize_taxi() -> None:
    logger.info("Sending register signal to Dispatch")
    taxi_state = get_taxi_state()

    taxi_url = socket.gethostname()
    callback_url = f"http://{taxi_url}:8081"
    taxi_state.taxi_id = str(uuid.uuid4())
    taxi_state.randomize_state()

    data = {
        "id": taxi_state.taxi_id,
        "callback_url": callback_url,
        "available": taxi_state.available,
        "x": taxi_state.x,
        "y": taxi_state.y,
    }
    async with httpx.AsyncClient() as client:
        try:
            taxi_register_url = urljoin(str(settings.dispatch_url), "taxi")
            response = await client.post(
                taxi_register_url,
                json=data,
            )
            logger.info(f"TAXI Register OK {response.json()}")
        except Exception as e:
            logger.error("Taxi Register Error:", e)
