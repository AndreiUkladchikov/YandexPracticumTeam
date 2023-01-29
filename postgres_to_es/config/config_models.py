from datetime import datetime
from enum import Enum

from pydantic import BaseModel


class State(BaseModel):
    last_update: datetime
    last_row: int
    is_finished: bool
    index: str


class Indexes(Enum):
    MOVIE = "movies"
    GENRE = "genres"
    PERSONS = "persons"
