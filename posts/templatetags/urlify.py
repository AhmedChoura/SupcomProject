from urllib import quote_plus
from django import template
#get the template library
register = template.Library()
# register urlify function as a filter in this library to use directly in templates
@register.filter
def urlify(value):
    return quote_plus(value)