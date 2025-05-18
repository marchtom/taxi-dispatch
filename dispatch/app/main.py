import logging
from urllib.parse import urljoin

import httpx
from fastapi import FastAPI

from .schemas.taxi import TaxiPostRequest, TaxiPostResponse, TaxiNotifyMessage

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

TAXI_DB = {}

app = FastAPI()


@app.get("/")
def root():
    return {"Dispatch": "OK"}


@app.get("/taxi")
def taxi_list():
    return TAXI_DB


@app.post("/taxi")
def register_taxi(taxi: TaxiPostRequest):
    TAXI_DB[taxi.id] = taxi.callback_url
    logger.info(f"Taxi registered, {taxi.id}: {taxi.callback_url}")
    return TaxiPostResponse(id=taxi.id)


@app.post("/taxi/{id_}")
def ping_taxi(id_:str, data: TaxiNotifyMessage):
    url = urljoin(TAXI_DB[id_], "message")
    logger.info(f"Sending request to taxi, url: {url}")
    httpx.post(url, json={"message": data.message})
    return "ok"
