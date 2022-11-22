import postgres.pg_context as pg_context
import postgres.save_data as save_data
from models import Filmwork, Genre, GenreFilmwork, Person, PersonFilmwork
from sqlite.load_data import load_from_sqlite


def main():
    do_work = True
    gen = load_from_sqlite()
    with pg_context.conn_context() as conn:
        while do_work:
            data = next(gen)
            if len(data) > 0:
                if type(data[0]) is Filmwork:
                    save_data.save_film_works(conn, data)
                elif type(data[0]) is Genre:
                    save_data.save_genres(conn, data)
                elif type(data[0]) is Person:
                    save_data.save_people(conn, data)
                elif type(data[0]) is GenreFilmwork:
                    save_data.save_genre_film_work(conn, data)
                elif type(data[0]) is PersonFilmwork:
                    save_data.save_person_film_work(conn, data)
            else:
                do_work = False


if __name__ == '__main__':
    main()
