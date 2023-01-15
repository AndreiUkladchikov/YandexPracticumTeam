from django.http import JsonResponse
from django.views.generic.list import BaseListView
from django.views.generic.detail import BaseDetailView
from django.contrib.postgres.aggregates import ArrayAgg
from django.db.models import Q

from movies.models import Filmwork, RoleTypes


class MoviesApiMixin:
    model = Filmwork
    http_method_names = ['get']

    def get_queryset(self):
        base_set = Filmwork.objects.prefetch_related('people', 'genres_list').annotate(
            writers=ArrayAgg('people__full_name', filter=Q(personfilmwork__role=RoleTypes.WRITER), distinct=True),
            actors=ArrayAgg('people__full_name', filter=Q(personfilmwork__role=RoleTypes.ACTOR), distinct=True),
            directors=ArrayAgg('people__full_name', filter=Q(personfilmwork__role=RoleTypes.DIRECTOR), distinct=True),
            genres=ArrayAgg('genres_list__name', distinct=True)
        ).values("id", "title", "description", "creation_date", "rating", "type", "genres", "actors", "directors", "writers")
        return base_set

    def render_to_response(self, context, **response_kwargs):
        return JsonResponse(context)


class MoviesListApi(MoviesApiMixin, BaseListView):
    paginate_by = 50

    def get_context_data(self, *, object_list=None, **kwargs):
        queryset = self.get_queryset()
        paginator, page, queryset, is_paginated = self.paginate_queryset(
            queryset,
            self.paginate_by
        )
        return {
            "count": paginator.count,
            "total_pages": paginator.num_pages,
            "prev": page.previous_page_number() if page.has_previous() else None,
            "next": page.next_page_number() if page.has_next() else None,
            "results": [film for film in queryset.all()]
        }

    def render_to_response(self, context, **response_kwargs):
        return JsonResponse(context)


class MoviesDetailApi(MoviesApiMixin, BaseDetailView):

    def get_context_data(self, **kwargs):
        context = self.get_object()
        return context
