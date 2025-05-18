import logging

from fastapi import FastAPI

from app.routers import taxi


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

TAXI_DB = {}

app = FastAPI()
app.include_router(taxi.router)


@app.get("/")
def root() -> dict:
    return {"Dispatch": "OK"}
