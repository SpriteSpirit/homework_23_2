from django.core.cache import cache

from catalog.models import Product, Category
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


def get_categories():
    # кеширование на 60 минут
    cache_timeout = 60 * 60

    cache_key = 'categories'
    categories = cache.get(cache_key)

    if not categories:
        categories = Category.objects.all()
        cache.set(cache_key, categories, cache_timeout)
    return categories


def get_cached_blog(slug):
    # кеширование на 15 минут
    cache_timeout = 60 * 15
    cache_key = slug

    if settings.CACHE_ENABLED:
        blog = cache.get_or_set(cache_key, cache_timeout)

        if not blog:
            blog = BlogPost.objects.get(slug=slug),
            cache.add(cache_key, blog, cache_timeout)
    else:
        blog = BlogPost.objects.get(slug=slug)

    print(f'Кэширование блога {slug}')
    return blog


def get_cached_blogs():
    # кеширование на 30 минут
    cache_timeout = 60 * 30
    cache_key = 'blogs'

    if settings.CACHE_ENABLED:
        blogs = cache.get_or_set(cache_key, BlogPost.objects.all, cache_timeout)

        if not blogs:
            blogs = BlogPost.objects.all()
            cache.add(cache_key, blogs, cache_timeout)
    else:
        blogs = BlogPost.objects.all()

    print(f'Кэширование продуктов {cache.get(cache_key)}')

    return blogs
