from fastapi import FastAPI

from app.lifespan import lifespan
from app.routers import event, taxi, trip

app = FastAPI(lifespan=lifespan)
app.include_router(taxi.router)
app.include_router(trip.router)
app.include_router(event.router)


@app.get("/")
def root() -> dict:
    return {"Dispatch": "OK"}
