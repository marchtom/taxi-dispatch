import asyncio
import logging
import os
import socket
from contextlib import asynccontextmanager

import httpx
from fastapi import FastAPI

from app.state import get_taxi_state


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

DISPATCH_URL = os.environ["DISPATCH_URL"]


@asynccontextmanager
async def lifespan(_: FastAPI):
    await asyncio.sleep(5)
    logger.info("Sending register signal to Dispatch")
    taxi_state = get_taxi_state()

    taxi_id = socket.gethostname()
    callback_url = f"http://{taxi_id}:8081"
    taxi_state.taxi_id = taxi_id

    data = {
        "id": taxi_id,
        "callback_url": callback_url,
        "available": True,
        "x": taxi_state.x,
        "y": taxi_state.y,
    }
    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(f"{DISPATCH_URL}/taxi", json=data)
            logger.info(f"TAXI Register OK {response.json()}")
        except Exception as e:
            logger.error("Taxi Register Error:", e)
    yield
    # TODO: Add teardown call to dispatch here
