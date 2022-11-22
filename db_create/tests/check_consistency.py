import postgres.load_data as pg_load_data
import postgres.pg_context as pg_context
from models import Filmwork, Genre, GenreFilmwork, Person, PersonFilmwork
from sqlite.load_data import load_from_sqlite


def check():
    filmworks = []
    genres = []
    people = []
    genre_filmworks = []
    person_filmworks = []
    do_work = True
    gen = load_from_sqlite()
    while do_work:
        data = next(gen)
        if len(data) > 0:
            if type(data[0]) is Filmwork:
                filmworks.extend(data)
            elif type(data[0]) is Genre:
                genres.extend(data)
            elif type(data[0]) is Person:
                people.extend(data)
            elif type(data[0]) is GenreFilmwork:
                genre_filmworks.extend(data)
            elif type(data[0]) is PersonFilmwork:
                person_filmworks.extend(data)
        else:
            do_work = False
    with pg_context.conn_context() as conn:
        test_two_tables(filmworks, pg_load_data.load_film_works(conn))
        test_two_tables(genres, pg_load_data.load_genres(conn))
        test_two_tables(people, pg_load_data.load_people(conn))
        test_two_tables(person_filmworks, pg_load_data.load_person_film_work(conn))
        test_two_tables(genre_filmworks, pg_load_data.load_genre_film_work(conn))


def test_two_tables(pg_data: list, sqlite_data: list):
    assert pg_data == sqlite_data


if __name__ == '__main__':
    check()
