from django import template
import locale

register = template.Library()


@register.filter(name='currency')
def currency(value):
    locale.setlocale(locale.LC_ALL, 'ru_RU.UTF-8')
    rounded_value = round(value)
    return locale.format_string('%d ₽', rounded_value, grouping=True)


@register.filter()
def my_media(value):
    if value:
        return f'/media/{value}'
    return '#'
