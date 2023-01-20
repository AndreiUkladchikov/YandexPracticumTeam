from rest_framework import generics

from config.pagination import MoviesPagination
from movies.models import FilmWork
from movies.api.v1.serializers import MovieSerializer


class MoviesListApi(generics.ListAPIView):
    serializer_class = MovieSerializer
    queryset = FilmWork.objects.prefetch_related('genres', 'persons')
    pagination_class = MoviesPagination


class MovieDetailApi(generics.RetrieveAPIView):
    serializer_class = MovieSerializer
    queryset = FilmWork.objects.prefetch_related('genres', 'persons')
    lookup_field = 'pk'
