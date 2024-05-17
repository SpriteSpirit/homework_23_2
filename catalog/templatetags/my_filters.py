from django import template
from transliterate import slugify
import locale

register = template.Library()


@register.filter(name='currency')
def currency(value):
    locale.setlocale(locale.LC_ALL, 'ru_RU.UTF-8')
    rounded_value = round(value)
    return locale.format_string('%d ₽', rounded_value, grouping=True)


@register.filter(name='translate')
def translate(value):
    return slugify(value)


@register.filter()
def my_media(value):
    if value:
        return f'/media/{value}'
    return '#'
