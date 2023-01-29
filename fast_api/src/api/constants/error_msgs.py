# This classes in future can be extended with localization, etc.


class PersonMsg:
    __slots__ = ()
    not_found_by_id = "Person not found"
    no_search_result = "Persons with your criteria not found"
    no_films_by_person = "Films with this person not found"


class FilmMsg:
    __slots__ = ()
    not_found_by_id = "Film not found"
    no_search_result = "Films with your criteria not found"


class GenreMsg:
    __slots__ = ()
    not_found_by_id = "Genre not found"
    no_search_result = "Genres with your criteria not found"


class ElasticMsg:
    __slots__ = ()
    elasticsearch_is_not_available = (
        "Something went wrong :( Everything will be working soon! We apologize for the "
        "inconvenience"
    )
