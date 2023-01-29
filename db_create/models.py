import uuid
from dataclasses import dataclass, field
from datetime import datetime


@dataclass
class Filmwork:
    id: uuid.UUID
    title: str
    description: str
    creation_date: datetime
    type: str
    file_path: str
    created_at: str
    updated_at: str
    created: datetime = field(default_factory=datetime.now)
    modified: datetime = field(default_factory=datetime.now)
    rating: float = field(default=0.0)

    def __eq__(self, other):
        is_equal = False
        if (
            self.id == other.id
            and self.title == other.title
            and self.description == other.description
            and self.creation_date == other.creation_date
            and self.type == other.type
            and self.file_path == other.file_path
            and self.rating == other.rating
        ):
            is_equal = True
        return is_equal

    def __hash__(self):
        return hash(
            (
                self.id,
                self.title,
                self.description,
                self.creation_date,
                self.type,
                self.file_path,
                self.rating,
            )
        )


@dataclass
class Genre:
    id: uuid.UUID
    name: str
    description: str
    created_at: str
    updated_at: str
    created: datetime = field(default_factory=datetime.now)
    modified: datetime = field(default_factory=datetime.now)

    def __eq__(self, other):
        is_equal = False
        if (
            self.id == other.id
            and self.name == other.name
            and self.description == other.description
        ):
            is_equal = True
        return is_equal

    def __hash__(self):
        return hash((self.id, self.name, self.description))


@dataclass
class Person:
    id: uuid.UUID
    full_name: str
    created_at: str
    updated_at: str
    created: datetime = field(default_factory=datetime.now)
    modified: datetime = field(default_factory=datetime.now)

    def __eq__(self, other):
        is_equal = False
        if self.id == other.id and self.full_name == other.full_name:
            is_equal = True
        return is_equal

    def __hash__(self):
        return hash((self.id, self.full_name))


@dataclass
class GenreFilmwork:
    id: uuid.UUID
    genre_id: uuid.UUID
    film_work_id: uuid.UUID
    created_at: str
    created: datetime = field(default_factory=datetime.now)

    def __eq__(self, other):
        is_equal = False
        if (
            self.id == other.id
            and self.genre_id == other.genre_id
            and self.film_work_id == other.film_work_id
        ):
            is_equal = True
        return is_equal

    def __hash__(self):
        return hash((self.id, self.genre_id, self.film_work_id))


@dataclass
class PersonFilmwork:
    id: uuid.UUID
    film_work_id: uuid.UUID
    person_id: uuid.UUID
    role: str
    created_at: str
    created: datetime = field(default_factory=datetime.now)

    def __eq__(self, other):
        is_equal = False
        if (
            self.id == other.id
            and self.person_id == other.person_id
            and self.film_work_id == other.film_work_id
            and self.role == other.role
        ):
            is_equal = True
        return is_equal

    def __hash__(self):
        return hash((self.id, self.person_id, self.film_work_id, self.role))
