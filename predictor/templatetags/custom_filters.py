from django import template

register = template.Library()

@register.filter
def divide(value, divisor):
    try:
        return value / divisor
    except (TypeError, ZeroDivisionError):
        return None  # Return None if division is not possible