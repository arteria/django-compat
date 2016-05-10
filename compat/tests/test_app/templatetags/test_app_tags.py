from django import template

register = template.Library()


@register.simple_tag
def my_tag():
    return "Return value of my_tag"
