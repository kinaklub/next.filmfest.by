from django.db import models

from modeladminutils.queryset import SearchableQuerySet


__all__ = ['SearchableManager']


class BaseSearchableManager(models.Manager):
    def get_queryset(self):
        return SearchableQuerySet(self.model)


SearchableManager = BaseSearchableManager.from_queryset(SearchableQuerySet)
