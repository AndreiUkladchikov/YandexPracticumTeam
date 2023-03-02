class ReviewMsg:
    __slots__ = ()
    not_found_by_id = "Review not found"


class FilmMsg:
    __slots__ = ()
    not_found_by_id = "Film not found by id"


class DuplicateFilmMsg:
    __slots__ = ()
    film_duplicate = "You have already added this film"


class NoUserBookmarksMsg:
    _slots__ = ()
    no_bookmarks = "The user has no bookmarks"
