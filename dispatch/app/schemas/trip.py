from datetime import datetime

from pydantic import BaseModel


class TripGetRequest(BaseModel):
    id: str
    start_time: datetime
    end_time: datetime | None = None
    x_start: int
    y_start: int
    x_stop: int
    y_stop: int


class TripPostRequest(BaseModel):
    id: str
    start_time: datetime | None = None
    x_start: int
    y_start: int
    x_stop: int
    y_stop: int


class TripPostResponse(BaseModel):
    id: str
