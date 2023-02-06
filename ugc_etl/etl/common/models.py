from dataclasses import dataclass


@dataclass(frozen=True)
class MovieWatch:
    user_id: str
    film_id: str
    timestamp: int


@dataclass(frozen=True)
class MovieWatchLater:
    user_id: str
    film_id: str
