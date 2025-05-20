from datetime import datetime
from typing import Annotated

from pydantic import BaseModel, Field


class TripGetResponse(BaseModel):
    id: str
    start_time: datetime
    pickup_time: datetime | None = None
    end_time: datetime | None = None
    x_start: int
    y_start: int
    x_stop: int
    y_stop: int


class TripPostRequest(BaseModel):
    id: str | None = None
    start_time: datetime | None = None
    x_start: Annotated[int, Field(ge=1, le=100)]
    y_start: Annotated[int, Field(ge=1, le=100)]
    x_stop: Annotated[int, Field(ge=1, le=100)]
    y_stop: Annotated[int, Field(ge=1, le=100)]


class TripPostResponse(BaseModel):
    id: str


class TripPatchRequest(BaseModel):
    end_time: datetime | None = None


class TripPatchResponse(TripPostResponse):
    ...
