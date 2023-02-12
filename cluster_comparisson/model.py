class MovieWatch:
    user_id: str
    film_id: str
    timestamp: int

    def __init__(self, user, film, time) -> None:
        self.user_id = user
        self.film_id = film
        self.timestamp = time
