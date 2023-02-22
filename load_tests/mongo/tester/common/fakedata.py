from uuid import uuid4


class FakeData:

    def __init__(self) -> None:
        self.users_id = [str(uuid4()) for _ in range(100)]
        self.films_id = [str(uuid4()) for _ in range(100)]


fakeids = FakeData()
