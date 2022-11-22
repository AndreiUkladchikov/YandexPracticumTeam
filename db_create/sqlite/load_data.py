import logging
import sqlite3
from contextlib import contextmanager
from datetime import datetime

import db_config
from models import Filmwork, Genre, GenreFilmwork, Person, PersonFilmwork

load_limit = 100


def load_from_sqlite() -> list:
    with conn_context() as conn:
        curs = conn.cursor()
        try:
            generators = []
            generators.append(load_film_works(curs))
            generators.append(load_genres(curs))
            generators.append(load_people(curs))
            generators.append(load_genre_film_work(curs))
            generators.append(load_person_film_work(curs))
            gen_id = 0
            current_gen = generators[gen_id]
            load = True
            while load:
                data = next(current_gen)
                if len(data) == 0:
                    if gen_id == len(generators) - 1:
                        load = False
                    else:
                        gen_id = gen_id + 1
                        current_gen = generators[gen_id]
                        data = next(current_gen)
                yield data
        except (sqlite3.Error) as error:
            logging.exception(error)


def load_film_works(curs: sqlite3.Cursor) -> list[Filmwork]:
    curs.execute("SELECT * FROM film_work;")
    while True:
        try:
            result = curs.fetchmany(load_limit)
            filmworks = []
            for row in result:
                film = Filmwork(**row)
                film.created = parse_sqlite_datetime(film.created_at)
                film.modified = parse_sqlite_datetime(film.updated_at)
                filmworks.extend([film])
            yield filmworks
        except StopIteration:
            return


def load_genres(curs: sqlite3.Cursor) -> list[Genre]:
    curs.execute("SELECT * FROM genre;")
    while True:
        try:
            result = curs.fetchmany(load_limit)
            genres = []
            for row in result:
                genre = Genre(**row)
                genre.created = parse_sqlite_datetime(genre.created_at)
                genre.modified = parse_sqlite_datetime(genre.updated_at)
                genres.extend([genre])
            yield genres
        except StopIteration:
            return


def load_people(curs: sqlite3.Cursor) -> list[Person]:
    curs.execute("SELECT * FROM person;")
    while True:
        try:
            result = curs.fetchmany(load_limit)
            people = []
            for row in result:
                person = Person(**row)
                person.created = parse_sqlite_datetime(person.created_at)
                person.modified = parse_sqlite_datetime(person.updated_at)
                people.extend([person])
            yield people
        except StopIteration:
            return


def load_genre_film_work(curs: sqlite3.Cursor) -> list[GenreFilmwork]:
    curs.execute("SELECT * FROM genre_film_work;")
    while True:
        try:
            result = curs.fetchmany(load_limit)
            genre_filmworks = []
            for row in result:
                genre_filmwork = GenreFilmwork(**row)
                genre_filmwork.created = parse_sqlite_datetime(genre_filmwork.created_at)
                genre_filmworks.extend([genre_filmwork])
            yield genre_filmworks
        except StopIteration:
            return


def load_person_film_work(curs: sqlite3.Cursor) -> list[PersonFilmwork]:
    curs.execute("SELECT * FROM person_film_work;")
    while True:
        try:
            result = curs.fetchmany(load_limit)
            person_filmworks = []
            for row in result:
                person_filmwork = PersonFilmwork(**row)
                person_filmwork.created = parse_sqlite_datetime(person_filmwork.created_at)
                person_filmworks.extend([person_filmwork])
            yield person_filmworks
        except StopIteration:
            return


def parse_sqlite_datetime(string: str) -> datetime:
    return datetime.strptime(string[0:19], '%Y-%m-%d %H:%M:%S') if string != 'None' else None


def dict_factory(curs: sqlite3.Cursor, row: tuple) -> dict:
    d = {}
    for idx, col in enumerate(curs.description):
        d[col[0]] = row[idx]
    return d


@contextmanager
def conn_context():
    print(db_config.SQLITE_CON)
    conn = sqlite3.connect(db_config.SQLITE_CON)
    conn.row_factory = dict_factory
    yield conn
    conn.close()
