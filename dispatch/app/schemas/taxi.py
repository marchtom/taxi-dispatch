from typing import Annotated

from pydantic import BaseModel, Field


class TaxiGetRequest(BaseModel):
    id: str
    callback_url: str
    available: bool
    x: int
    y: int


class TaxiPostRequest(BaseModel):
    id: str
    callback_url: str
    available: bool
    x: Annotated[int, Field(ge=1, le=100)]
    y: Annotated[int, Field(ge=1, le=100)]


class TaxiPostResponse(BaseModel):
    id: str


class TaxiNotifyMessage(BaseModel):
    message: str
