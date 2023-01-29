import logging

import psycopg2
from models import Filmwork, Genre, GenreFilmwork, Person, PersonFilmwork
from psycopg2.extensions import connection as _connection
from psycopg2.extras import NamedTupleCursor


def load_film_works(conn: _connection) -> list[Filmwork]:
    try:
        curs = conn.cursor(cursor_factory=NamedTupleCursor)
        curs.execute("SELECT * FROM content.film_work;")
        result = curs.fetchall()
        filmworks = []
        for film in result:
            filmworks.extend(
                [
                    Filmwork(
                        id=film.id,
                        title=film.title,
                        description=film.description,
                        creation_date=film.creation_date,
                        file_path=film.file_path,
                        rating=film.rating,
                        type=film.type,
                        created=film.created,
                        modified=film.modified,
                    )
                ]
            )
        return filmworks
    except (psycopg2.Error) as error:
        logging.error(error)


def load_genres(conn: _connection) -> list[Genre]:
    try:
        curs = conn.cursor(cursor_factory=NamedTupleCursor)
        curs.execute("SELECT * FROM content.genre;")
        result = curs.fetchall()
        genres = []
        for genre in result:
            genres.extend(
                [
                    Genre(
                        id=genre.id,
                        name=genre.name,
                        description=genre.description,
                        created=genre.created,
                        modified=genre.modified,
                    )
                ]
            )
        return genres
    except (psycopg2.Error) as error:
        logging.error(error)


def load_people(conn: _connection) -> list[Person]:
    try:
        curs = conn.cursor(cursor_factory=NamedTupleCursor)
        curs.execute("SELECT * FROM content.person;")
        result = curs.fetchall()
        people = []
        for person in result:
            people.extend(
                [
                    Person(
                        id=person.id,
                        full_name=person.full_name,
                        created=person.created,
                        modified=person.modified,
                    )
                ]
            )
        return people
    except (psycopg2.Error) as error:
        logging.error(error)


def load_genre_film_work(conn: _connection) -> list[GenreFilmwork]:
    try:
        curs = conn.cursor(cursor_factory=NamedTupleCursor)
        curs.execute("SELECT * FROM content.genre_film_work;")
        result = curs.fetchall()
        genre_film_works = []
        for genre in result:
            genre_film_works.extend(
                [
                    GenreFilmwork(
                        id=genre.id,
                        genre_id=genre.genre_id,
                        film_work_id=genre.film_work_id,
                        created=genre.created,
                    )
                ]
            )
        return genre_film_works
    except (psycopg2.Error) as error:
        logging.error(error)


def load_person_film_work(conn: _connection) -> list[PersonFilmwork]:
    try:
        curs = conn.cursor(cursor_factory=NamedTupleCursor)
        curs.execute("SELECT * FROM content.person_film_work;")
        result = curs.fetchall()
        person_film_works = []
        for person in result:
            person_film_works.extend(
                [
                    PersonFilmwork(
                        id=person.id,
                        person_id=person.person_id,
                        film_work_id=person.film_work_id,
                        role=person.role,
                        created=person.created,
                    )
                ]
            )
        return person_film_works
    except (psycopg2.Error) as error:
        logging.error(error)
