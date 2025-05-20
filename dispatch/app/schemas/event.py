from pydantic import BaseModel


class EventPostRequest(BaseModel):
    taxi_id: str


class EventPostResponse(BaseModel):
    message: str
