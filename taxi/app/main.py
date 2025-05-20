from fastapi import FastAPI

from app.lifespan import lifespan
from app.routers import trip


app = FastAPI(lifespan=lifespan)
app.include_router(trip.router)


@app.get("/")
def root() -> dict:
    return {"Taxi": "OK"}
