import operator
from functools import reduce
from itertools import chain

from django.db import models
from django.utils import six

from rest_framework import filters
from rest_framework.compat import distinct

from .layout import DefaultLayout


class LayoutSearchFilter(filters.SearchFilter):
    """Keyboard layout-insensitive search filter.

    Filter allows to search for entries, even if search term is typed on
    wrong layout.

    Example:

        class ExampleListView(BaseAPIView):
            queryset = Example.objects.all()
            serializer_class = ExampleSerializer
            filter_backends = (LayoutSearchFilter,)
            search_fields = ('name',)
            search_layouts = (EnglishRussianLayout,)

    """

    def get_search_layouts(self, view):
        """Method to get search layouts from view class."""
        default_layouts = (DefaultLayout,)
        search_layouts = getattr(view, 'search_layouts', [])
        return chain(default_layouts, search_layouts)

    def get_term(self, term, layout):
        """Method to convert search term to different layout."""
        return layout.convert_term(term)

    def filter_queryset(self, request, queryset, view):
        """Custom `filter_queryset` method.

        This is the original `filter_queryset` method with adding extra
        search conditions for ``SearchFilter`` filtering.

        """
        search_fields = getattr(view, 'search_fields', None)
        search_terms = self.get_search_terms(request)

        if not search_fields or not search_terms:
            return queryset

        orm_lookups = [
            self.construct_search(six.text_type(search_field))
            for search_field in search_fields
        ]

        base = queryset
        conditions = []

        # Here is custom code - each search term in transformed to each of
        # specified keyboard layouts

        for search_term in search_terms:
            queries = [
                models.Q(**{orm_lookup: self.get_term(search_term, layout)})
                for orm_lookup in orm_lookups
                for layout in self.get_search_layouts(view)
            ]
            conditions.append(reduce(operator.or_, queries))

        queryset = queryset.filter(reduce(operator.and_, conditions))

        if self.must_call_distinct(queryset, search_fields):
            queryset = distinct(queryset, base)

        return queryset
