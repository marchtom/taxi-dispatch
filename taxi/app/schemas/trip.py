from typing import Annotated

from pydantic import BaseModel, Field


class TripPostRequest(BaseModel):
    x_start: Annotated[int, Field(ge=1, le=100)]
    y_start: Annotated[int, Field(ge=1, le=100)]
    x_stop: Annotated[int, Field(ge=1, le=100)]
    y_stop: Annotated[int, Field(ge=1, le=100)]


class TripPostResponse(BaseModel):
    message: str
