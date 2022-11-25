import uuid
import logging
from datetime import datetime

import psycopg2
from psycopg2.extensions import connection as _connection
from psycopg2.extras import NamedTupleCursor

from models import Movie, PersonTypes, Person, Genre


def load_film_works(conn: _connection, date: datetime, offset: int, limit: int) -> list[Movie]:
    try:
        curs = conn.cursor(cursor_factory=NamedTupleCursor)
        curs.execute(
            """
                DROP TABLE IF EXISTS temp_table;

                SELECT DISTINCT movies.id, movies.title, movies.description, movies.type, movies.rating
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
            (date, date, date, date, date, limit, offset)
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
                        director='',
                        actors_names=[],
                        writers_names=[],
                        actors=[],
                        writers=[],
                        genres=[],
                        genre=[]
                    )
                if film.role == PersonTypes.DIRECTOR:
                    movies[film.id].director = film.full_name
                elif film.role == PersonTypes.ACTOR and film.full_name not in movies[film.id].actors_names:
                    movies[film.id].actors_names.extend([film.full_name])
                    movies[film.id].actors.extend([Person(id=film.person_id, name=film.full_name)])
                elif film.role == PersonTypes.WRITER and film.full_name not in movies[film.id].writers_names:
                    movies[film.id].writers_names.extend([film.full_name])
                    movies[film.id].writers.extend([Person(id=film.person_id, name=film.full_name)])
                if film.genre_name not in movies[film.id].genre:
                    movies[film.id].genre.extend([film.genre_name])
                    movies[film.id].genres.extend([Genre(id=film.genre_id, name=film.genre_name)])
            movies_list = list(movies.values())[1:]
        return movies_list
    except (psycopg2.Error) as error:
        logging.error(error)


def load_genres(conn: _connection, date: datetime, offset: int, limit: int) -> list[Genre]:
    try:
        curs = conn.cursor(cursor_factory=NamedTupleCursor)
        curs.execute(
            """
                SELECT genres.id, genres.name
                FROM content.genre as genres
                WHERE genres.modified > %s

                LIMIT %s OFFSET %s;""",
            (date, limit, offset)
            )
        result = curs.fetchall()
        genres = []
        if len(result) > 0:
            for genre in result:
                genres.extend([
                    Genre(
                        id=genre.id,
                        name=genre.name
                    )
                ])
        return genres
    except (psycopg2.Error) as error:
        logging.error(error)
