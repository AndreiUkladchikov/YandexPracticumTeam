import uuid
from datetime import datetime

import psycopg2
from loguru import logger
from models import Movie, NestedModel, NestedModelPerson, Person, PersonTypes
from psycopg2.extensions import connection as _connection
from psycopg2.extras import NamedTupleCursor


def load_film_works(
    conn: _connection, date: datetime, offset: int, limit: int
) -> list[Movie]:
    try:
        curs = conn.cursor(cursor_factory=NamedTupleCursor)
        curs.execute(
            """
                DROP TABLE IF EXISTS temp_table;

                SELECT DISTINCT movies.id, movies.title, movies.description, movies.type, movies.rating, movies.access_level
                INTO TEMP TABLE temp_table
                FROM content.film_work as movies
                LEFT JOIN content.person_film_work as person_filmworks on movies.id = person_filmworks.film_work_id
                LEFT JOIN content.person as person on person.id = person_filmworks.person_id
                LEFT JOIN content.genre_film_work as genre_filmworks on movies.id = genre_filmworks.film_work_id
                LEFT JOIN content.genre as genre on person.id = genre_filmworks.genre_id
                WHERE movies.modified > %s OR
                    person_filmworks.created > %s OR
                    person.modified > %s OR
                    genre_filmworks.created > %s OR
                    genre.modified > %s

                LIMIT %s OFFSET %s;

                SELECT temp_table.id as id,
                    temp_table.title,
                    temp_table.description,
                    temp_table.rating,
                    temp_table.type,
                    temp_table.access_level,
                    person_filmworks.person_id,
                    person_filmworks.role,
                    person.full_name,
                    genre.name as genre_name,
                    genre.id as genre_id
                FROM temp_table as temp_table
                LEFT JOIN content.person_film_work as person_filmworks on temp_table.id = person_filmworks.film_work_id
                LEFT JOIN content.person as person on person.id = person_filmworks.person_id
                LEFT JOIN content.genre_film_work as genre_filmworks on temp_table.id = genre_filmworks.film_work_id
                LEFT JOIN content.genre as genre on genre.id = genre_filmworks.genre_id
                ORDER BY temp_table.id;""",
            (date, date, date, date, date, limit, offset),
        )
        result = curs.fetchall()
        movies = {uuid.UUID: Movie}
        movies_list = []
        if len(result) > 0:
            for film in result:
                if film.id not in movies.keys():
                    movies[film.id] = Movie(
                        id=film.id,
                        imdb_rating=film.rating,
                        type=film.type,
                        title=film.title,
                        description=film.description,
                        director="",
                        actors_names=[],
                        writers_names=[],
                        actors=[],
                        writers=[],
                        genres=[],
                        genre=[],
                        directors=[],
                        access_level=film.access_level,
                    )
                if film.role == PersonTypes.DIRECTOR:
                    movies[film.id].director = film.full_name
                    movies[film.id].directors = [
                        NestedModelPerson(id=film.person_id, full_name=film.full_name)
                    ]
                elif (
                    film.role == PersonTypes.ACTOR
                    and film.full_name not in movies[film.id].actors_names
                ):
                    movies[film.id].actors_names.extend([film.full_name])
                    movies[film.id].actors.extend(
                        [NestedModelPerson(id=film.person_id, full_name=film.full_name)]
                    )
                elif (
                    film.role == PersonTypes.WRITER
                    and film.full_name not in movies[film.id].writers_names
                ):
                    movies[film.id].writers_names.extend([film.full_name])
                    movies[film.id].writers.extend(
                        [NestedModelPerson(id=film.person_id, full_name=film.full_name)]
                    )
                if film.genre_name not in movies[film.id].genre:
                    movies[film.id].genre.extend([film.genre_name])
                    movies[film.id].genres.extend(
                        [NestedModel(id=film.genre_id, name=film.genre_name)]
                    )
            movies_list = list(movies.values())[1:]
        return movies_list
    except (psycopg2.Error) as error:
        logger.error(error)


def load_genres(
    conn: _connection, date: datetime, offset: int, limit: int
) -> list[NestedModel]:
    try:
        curs = conn.cursor(cursor_factory=NamedTupleCursor)
        curs.execute(
            """
                SELECT genres.id, genres.name
                FROM content.genre as genres
                WHERE genres.modified > %s

                LIMIT %s OFFSET %s;""",
            (date, limit, offset),
        )
        result = curs.fetchall()
        genres = []
        if len(result) > 0:
            for genre in result:
                genres.extend([NestedModel(id=genre.id, name=genre.name)])
        return genres
    except (psycopg2.Error) as error:
        logger.error(error)


def load_persons(
    conn: _connection, date: datetime, offset: int, limit: int
) -> list[Person]:
    try:
        curs = conn.cursor(cursor_factory=NamedTupleCursor)
        curs.execute(
            """
                DROP TABLE IF EXISTS temp_table;

                SELECT DISTINCT person.id, person.full_name
                INTO TEMP TABLE temp_table
                FROM content.person as person
                LEFT JOIN content.person_film_work as person_filmworks on person.id = person_filmworks.person_id
                WHERE person_filmworks.created > %s OR
                    person.modified > %s

                LIMIT %s OFFSET %s;

                SELECT temp_table.id as id,
                    temp_table.full_name,
                    person_filmworks.film_work_id,
                    person_filmworks.role
                FROM temp_table as temp_table
                LEFT JOIN content.person_film_work as person_filmworks on temp_table.id = person_filmworks.person_id
                ORDER BY temp_table.id;""",
            (date, date, limit, offset),
        )
        result = curs.fetchall()
        persons = {uuid.UUID: Person}
        persons_list = []
        if len(result) > 0:
            for person in result:
                if person.id not in persons.keys():
                    persons[person.id] = Person(
                        id=person.id,
                        full_name=person.full_name,
                        actor_in=[],
                        writer_in=[],
                        director_in=[],
                    )
                if person.role == PersonTypes.DIRECTOR:
                    persons[person.id].director_in.extend([person.film_work_id])
                elif person.role == PersonTypes.ACTOR:
                    persons[person.id].actor_in.extend([person.film_work_id])
                elif person.role == PersonTypes.WRITER:
                    persons[person.id].writer_in.extend([person.film_work_id])
            persons_list = list(persons.values())[1:]
        return persons_list
    except (psycopg2.Error) as error:
        logger.error(error)
