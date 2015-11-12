import django
from django import template

# Django 1.5 adds support of context variables for the url template tag
if django.VERSION >= (1, 5):
    from django.template.defaulttags import url as url_defaulttag
else:
    from django.templatetags.future import url as url_defaulttag

register = template.Library()


@register.tag
def url(parser, token):
    return url_defaulttag(parser, token)
