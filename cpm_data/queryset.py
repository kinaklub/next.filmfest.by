from django.db import models

from wagtail.wagtailsearch.queryset import SearchableQuerySetMixin


class SearchableQuerySet(SearchableQuerySetMixin, models.query.QuerySet):
    pass
