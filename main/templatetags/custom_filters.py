from django import template

register = template.Library()

@register.filter
def dict_item(dictionary, key):
    """
    Fetches a value from a dictionary by key.
    """
    if isinstance(dictionary, dict):  # Ensure it's a dictionary
        return dictionary.get(key, '')
    return ''


@register.filter
def range_filter(value):
    """Returns a range object from 0 to the specified value."""
    return range(value)

@register.filter
def subtract(value, arg):
    """Subtracts arg from value."""
    return value - arg