from pydantic import BaseModel
from src.schemas import Film


class Item(BaseModel):
    user_id: str
    film_id: str
    timestamp: int


class FilmViews(Film):
    user_id: str
    timestamp: int


class ResponseModel(BaseModel):
    msg: str
