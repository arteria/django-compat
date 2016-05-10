import django
from django import template

register = template.Library()


@register.tag
def url(parser, token):
    # Django 1.5 adds support of context variables for the url template tag
    if django.VERSION >= (1, 5):
        from django.template.defaulttags import url as url_defaulttag
    else:
        from django.templatetags.future import url as url_defaulttag

    return url_defaulttag(parser, token)


@register.tag
def verbatim(parser, token):
    if django.VERSION >= (1, 5):
        from django.template.defaulttags import verbatim as verbatim_defaulttag
        return verbatim_defaulttag(parser, token)

    # 1.4; not available from django
    # Source: https://github.com/aljosa/django-verbatim
    class VerbatimNode(template.Node):
        def __init__(self, content):
            self.content = content

        def render(self, context):
            return self.content

    text = []
    while 1:
        token = parser.tokens.pop(0)
        if token.contents == 'endverbatim':
            break
        if token.token_type == template.TOKEN_VAR:
            text.append('{{ ')
        elif token.token_type == template.TOKEN_BLOCK:
            text.append('{% ')
        text.append(token.contents)
        if token.token_type == template.TOKEN_VAR:
            text.append(' }}')
        elif token.token_type == template.TOKEN_BLOCK:
            text.append(' %}')
    return VerbatimNode(''.join(text))
