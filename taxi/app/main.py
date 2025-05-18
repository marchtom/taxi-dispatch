import logging
import os
import socket
from contextlib import asynccontextmanager

import httpx
from fastapi import FastAPI, Request

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

DISPATCH_URL = os.getenv("DISPATCH_URL", "http://dispatch:8080")


@asynccontextmanager
async def lifespan(_: FastAPI):
    logger.info("Sending register signal to Dispatch")
    taxi_id = socket.gethostname()
    callback_url = f"http://{taxi_id}:8081"
    data = {"id": taxi_id, "callback_url": callback_url}
    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(f"{DISPATCH_URL}/taxi", json=data)
            logger.info("TAXI Register OK:", response.json())
        except Exception as e:
            logger.error("Taxi Register Error:", e)
    yield


app = FastAPI(lifespan=lifespan)


@app.get("/")
def root():
    return {"Taxi": "OK"}


@app.post("/message")
async def dispatch_confirm(request: Request):
    body = await request.body()
    logger.info("Message from Dispatch!")
    logger.info(f"{body}")
    return "ok"
