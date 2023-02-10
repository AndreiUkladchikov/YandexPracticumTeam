from pydantic import BaseModel


class Item(BaseModel):
    user_id: str
    film_id: str
    timestamp: int


class ResponseModel(BaseModel):
    msg: str
