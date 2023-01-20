from django.contrib import admin
from movies.models import FilmWork, Genre, Person


@admin.register(Person)
class PersonAdmin(admin.ModelAdmin):
    list_display = ('full_name',)
    search_fields = ('full_name',)


class GenreFilmWorkInline(admin.TabularInline):
    model = FilmWork.genres.through
    extra = 0


class PersonFilmWorkInline(admin.TabularInline):
    model = FilmWork.persons.through
    extra = 0


@admin.register(FilmWork)
class FilmWorkAdmin(admin.ModelAdmin):
    search_fields = ('title', 'description')
    list_display = ('title', 'type', 'creation_date', 'rating', 'get_genres')
    list_filter = ('type',)
    list_prefetch_related = ('genres',)
    inlines = (GenreFilmWorkInline, PersonFilmWorkInline)

    def get_queryset(self, request):
        queryset = (
            super()
            .get_queryset(request)
            .prefetch_related(*self.list_prefetch_related)
        )
        return queryset

    def get_genres(self, obj):
        return ','.join([genre.name for genre in obj.genres.all()])

    get_genres.short_description = 'Жанры фильма'


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)
