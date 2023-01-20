from rest_framework import serializers
from movies.models import FilmWork, PersonRole


class MovieSerializer(serializers.ModelSerializer):
    creation_date = serializers.DateTimeField(format='%d-%m-%Y')
    genres = serializers.SerializerMethodField()
    actors = serializers.SerializerMethodField()
    directors = serializers.SerializerMethodField()
    writers = serializers.SerializerMethodField()

    def get_genres(self, instance):
        return [genre.name for genre in instance.genres.all()]

    def get_actors(self, instance):
        return [person.full_name for person in instance.persons.filter(personfilmwork__role=PersonRole.ACTOR)]

    def get_writers(self, instance):
        return [person.full_name for person in instance.persons.filter(personfilmwork__role=PersonRole.SCREENWRITER)]

    def get_directors(self, instance):
        return [person.full_name for person in instance.persons.filter(personfilmwork__role=PersonRole.PRODUCER)]

    class Meta:
        model = FilmWork
        fields = ('id', 'title', 'description', 'rating', 'type', 'creation_date',
                  'genres', 'actors', 'directors', 'writers')
