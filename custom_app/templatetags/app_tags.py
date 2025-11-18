from django import template
from datetime import datetime

register = template.Library()


# Кастомний тег
@register.simple_tag
def current_time(format_string):
    """ Повертає поточний час у заданому форматі. """
    return datetime.now().strftime(format_string)


# Кастомний фільтр
@register.filter
def lower_first(value):
    """ Робить літеру рядка малою. """
    if isinstance(value, str) and len(value) > 0:
        return value[0].lower() + value[1:]
    return value
