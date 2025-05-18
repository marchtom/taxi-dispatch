from pydantic import BaseModel


class TaxiPostRequest(BaseModel):
    id: str
    callback_url: str


class TaxiPostResponse(BaseModel):
    id: str


class TaxiNotifyMessage(BaseModel):
    message: str
