import logging

import psycopg2
from models import Filmwork, Genre, GenreFilmwork, Person, PersonFilmwork
from psycopg2.extensions import connection as _connection
from psycopg2.extras import execute_batch as _execute_batch


def create_db(conn: _connection) -> None:
    curr = conn.cursor()
    sql_query = """CREATE SCHEMA IF NOT EXISTS content;"""
    curr.execute(sql_query)
    curr.execute(open("movies_database.sql", "r").read())
    conn.commit()
    curr.close()


def save_film_works(conn: _connection, filmworks: list[Filmwork]) -> None:
    curr = conn.cursor()
    values = []
    sql_insert_query = """ INSERT INTO content.film_work
                            (id, title, description, creation_date, rating, type, created, modified, file_path)
                            VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s) """
    for film in filmworks:
        values.append((
            film.id,
            film.title,
            film.description,
            film.creation_date,
            film.rating,
            film.type,
            film.created,
            film.modified,
            film.file_path
        ))
    try:
        _execute_batch(curr, sql_insert_query, values)
        conn.commit()
    except (psycopg2.Error) as error:
        logging.exception(error)
    curr.close()


def save_genres(conn: _connection, genres: list[Genre]) -> None:
    curr = conn.cursor()
    values = []
    sql_insert_query = """ INSERT INTO content.genre
                            (id, name, description, created, modified)
                            VALUES (%s,%s,%s,%s,%s) """
    for genre in genres:
        values.append((
            genre.id,
            genre.name,
            genre.description,
            genre.created,
            genre.modified,
        ))
    try:
        _execute_batch(curr, sql_insert_query, values)
        conn.commit()
    except (psycopg2.Error) as error:
        logging.exception(error)
    curr.close()


def save_people(conn: _connection, people: list[Person]) -> None:
    curr = conn.cursor()
    values = []
    sql_insert_query = """ INSERT INTO content.person
                            (id, full_name, created, modified)
                            VALUES (%s,%s,%s,%s) """
    for person in people:
        values.append((
            person.id,
            person.full_name,
            person.created,
            person.modified,
        ))
    try:
        _execute_batch(curr, sql_insert_query, values)
        conn.commit()
    except (psycopg2.Error) as error:
        logging.exception(error)
    curr.close()


def save_genre_film_work(conn: _connection, genre_filmworks: list[GenreFilmwork]) -> None:
    curr = conn.cursor()
    values = []
    sql_insert_query = """ INSERT INTO content.genre_film_work
                            (id, genre_id, film_work_id, created)
                            VALUES (%s,%s,%s,%s) """
    for genre in genre_filmworks:
        values.append((
            genre.id,
            genre.genre_id,
            genre.film_work_id,
            genre.created,
        ))
    try:
        _execute_batch(curr, sql_insert_query, values)
        conn.commit()
    except (psycopg2.Error) as error:
        logging.exception(error)
    curr.close()


def save_person_film_work(conn: _connection, people: list[PersonFilmwork]) -> None:
    curr = conn.cursor()
    values = []
    sql_insert_query = """ INSERT INTO content.person_film_work
                            (id, film_work_id, person_id, role, created)
                            VALUES (%s,%s,%s,%s,%s) """
    for person in people:
        values.append((
            person.id,
            person.film_work_id,
            person.person_id,
            person.role,
            person.created
        ))
    try:
        _execute_batch(curr, sql_insert_query, values)
        conn.commit()
    except (psycopg2.Error) as error:
        logging.exception(error)
    curr.close()
