from django import template

register = template.Library()

@register.filter
def divide(value, divisor, decimal_places=2):
    try:
        result = value / divisor
        return round(result, decimal_places)  # Round the result to the specified number of decimal places
    except (TypeError, ZeroDivisionError):
        return None  # Return None if division is not possible