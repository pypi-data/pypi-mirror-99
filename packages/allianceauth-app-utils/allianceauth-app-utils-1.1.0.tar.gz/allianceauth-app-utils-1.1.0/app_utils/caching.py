import functools
import hashlib
from typing import Union

from django.core.cache import cache
from django.db import models


class ObjectCacheMixin:
    """Adds a simple object cache to a Django manager"""

    def get_cached(
        self,
        pk,
        timeout: Union[int, float] = None,
        select_related: str = None,
    ) -> models.Model:
        """Will return the requested object either from DB or from cache

        Args:
            pk: Primary key for object to fetch
            timeout: Timeout in seconds for cache
            select_related: select_related query to be applied (if any)

        Returns:
            model instance if found

        Exceptions:
            ``Model.DoesNotExist`` if object can not be found

        Example:

        .. code-block:: python

            # adding the Mixin to the model manager
            class MyModelManager(ObjectCacheMixin, models.Manager):
                pass

            # using the cache method
            obj = MyModel.objects.get_cached(pk=42, timeout=3600)

        """
        func = functools.partial(
            self._fetch_object_for_cache, pk=pk, select_related=select_related
        )
        return cache.get_or_set(
            self._create_object_cache_key(pk, select_related), func, timeout
        )

    def _create_object_cache_key(self, pk, select_related: str = None) -> str:
        suffix = (
            hashlib.md5(select_related.encode("utf-8")).hexdigest()
            if select_related
            else ""
        )
        return "{}_{}_{}{}".format(
            self.model._meta.app_label,
            self.model._meta.model_name,
            pk,
            f"_{suffix}" if suffix else "",
        )

    def _fetch_object_for_cache(self, pk, select_related: str = None):
        qs = self.select_related(select_related) if select_related else self
        return qs.get(pk=pk)


def cached_queryset(
    queryset: models.QuerySet, key: str, timeout: Union[int, float]
) -> models.QuerySet:
    """caches the given queryset

    Args:
        queryset: the query set to cache
        key: key to be used to reference this cache
        timeout: Timeout in seconds for cache

    Returns:
        query set

    Example:

        .. code-block:: python

            queryset = cached_queryset(
                MyModel.objects.filter(name__contains="dummy"),
                key="my_cache_key",
                timeout=3600
            )

    """
    return cache.get_or_set(key, lambda: queryset, timeout)
