from django.core.cache import cache

from catalog.models import Product
from config import settings


def get_cached_products():
    """
    Чтобы избежать избыточного запроса к базе данных, можно использовать метод get_or_set(),
    который получает значение из кэша и, если его нет, помещает значение в кэш.

    Чтобы избежать гонки при чтении/записи можно использовать метод add(),
    который помещает значение в кэш только в случае, если значение не существует
    """
    # кеширование на 15 минут
    cache_timeout = 60 * 15

    if settings.CACHE_ENABLED:
        cache_key = 'products'

        products = cache.get_or_set(cache_key, Product.objects.all, cache_timeout)

        if not products:
            products = Product.objects.all()
            cache.add(cache_key, products, cache_timeout)

        return products

