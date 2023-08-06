from django.core.exceptions import ObjectDoesNotExist
from django.db import models

from bublik.tabl import tabl


class BublikQuerySetMixin:

    def tabl(self, *args, **kwargs):
        return tabl(self, *args, **kwargs)

    def ids(self):
        return self.order_by().values_list('id', flat=True)


class BublikQuerySet(BublikQuerySetMixin, models.QuerySet):
    pass


class BublikManagerMixin:
    def get_queryset(self):
        return BublikQuerySet(self.model, using=self._db)

    def tabl(self, *args, **kwargs):
        return tabl(self.get_queryset(), *args, **kwargs)

    def ids(self):
        return self.get_queryset().order_by().values_list('id', flat=True)


class BublikManager(BublikManagerMixin, models.Manager):
    pass


class BublikModelMixin(models.Model):
    bublik = BublikManager()

    class Meta:
        abstract = True

    @classmethod
    def tabl(cls, *args, **kwargs):
        return tabl(cls, *args, **kwargs)

    @classmethod
    def get(cls, pk_or_unique, /):
        try:
            obj = cls.objects.get(pk=pk_or_unique)
            print(f'match by primary key')
            return obj
        except (ObjectDoesNotExist, ValueError):
            for field in cls._meta.get_fields():
                if getattr(field, 'unique', False):
                    try:
                        query_lookup = field.name
                        if issubclass(type(field), models.CharField):
                            query_lookup += '__iexact'
                        obj = cls.objects.get(**{query_lookup: str(pk_or_unique)})
                        print(f'match by {field.name}')
                        return obj
                    except (ObjectDoesNotExist, ValueError):
                        pass
        raise cls.DoesNotExist(
            f'{cls._meta.model_name.capitalize()} matching query does not exist.')
