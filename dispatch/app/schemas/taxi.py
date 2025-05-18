from pydantic import BaseModel


class TaxiGetRequest(BaseModel):
    id: str
    callback_url: str
    active: bool
    x: int
    y: int


class TaxiPostRequest(BaseModel):
    id: str
    callback_url: str
    active: bool
    x: int
    y: int


class TaxiPostResponse(BaseModel):
    id: str


class TaxiNotifyMessage(BaseModel):
    message: str
