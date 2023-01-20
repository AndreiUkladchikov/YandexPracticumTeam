from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.utils.translation import gettext_lazy as _
from movies.core import TimeStampedMixin, UUIDMixin


class FilmType(models.TextChoices):
    MOVIE = 'movie', 'Кино',
    TV_SHOW = 'tv_show', 'ТВ шоу'


class PersonRole(models.TextChoices):
    ACTOR = 'actor', 'Актер',
    SCREENWRITER = 'screenwriter', 'Сценарист'
    PRODUCER = 'producer', 'Режиссер'


class Genre(UUIDMixin, TimeStampedMixin):
    name = models.CharField(_('name'), max_length=255)
    description = models.TextField(_('description'), blank=True, null=True)

    class Meta:
        db_table = 'content"."genre'
        verbose_name = _('Genre')
        verbose_name_plural = _('Genres')

    def __str__(self):
        return self.name


class Person(UUIDMixin, TimeStampedMixin):
    full_name = models.CharField(_('full_name'), max_length=300)

    class Meta:
        db_table = 'content"."person'
        verbose_name = _('Person')
        verbose_name_plural = _('Persons')

    def __str__(self):
        return self.full_name


class FilmWork(UUIDMixin, TimeStampedMixin):
    title = models.CharField(_('name'), max_length=255)
    description = models.TextField(_('description'), blank=True, null=True)
    creation_date = models.DateTimeField(_('creation_date'), auto_now_add=True, null=True)
    rating = models.FloatField(_('rating'), blank=True, null=True,
                               validators=[MinValueValidator(0),
                                           MaxValueValidator(100)])
    type = models.CharField(_('type'), max_length=100, blank=False, choices=FilmType.choices)
    genres = models.ManyToManyField(Genre, through='GenreFilmWork', related_name='film_works')
    persons = models.ManyToManyField(Person, through='PersonFilmWork', related_name='film_works')

    class Meta:
        db_table = 'content"."film_work'
        verbose_name = _('FilmWork')
        verbose_name_plural = _('FilmWorks')
        index_together = (
            ('rating', 'type')
        )

    def __str__(self):
        return self.title


class GenreFilmWork(UUIDMixin):
    film_work = models.ForeignKey(FilmWork, on_delete=models.CASCADE)
    genre = models.ForeignKey(Genre, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'content"."genre_film_work'
        unique_together = ('film_work', 'genre',)
        verbose_name = _('GenreFilmWork')
        verbose_name_plural = _('GenreFilmWorks')


class PersonFilmWork(UUIDMixin):
    person = models.ForeignKey(Person, on_delete=models.CASCADE)
    film_work = models.ForeignKey(FilmWork, on_delete=models.CASCADE)
    role = models.TextField(_('role'), blank=False, choices=PersonRole.choices)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'content"."person_film_work'
        unique_together = ('person', 'film_work', 'role')
        verbose_name = _('PersonFilmWork')
        verbose_name_plural = _('PersonFilmWorks')
