from fastapi import FastAPI

from app.routers import taxi, trip


app = FastAPI()
app.include_router(taxi.router)
app.include_router(trip.router)


@app.get("/")
def root() -> dict:
    return {"Dispatch": "OK"}
