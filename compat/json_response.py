"""
A subclass of HttpResponse useful as a shortcut in views; it chooses the correct JSON serializer based on whether or not it is passed a QuerySet.
Source: https://djangosnippets.org/snippets/154/
"""
from django.core.serializers import json, serialize
from django.db.models.query import QuerySet
from django.http import HttpResponse

class JsonResponse(HttpResponse):
    def __init__(self, object):
        if isinstance(object, QuerySet):
            content = serialize('json', object)
        else:
            content = simplejson.dumps(
                object, indent=2, cls=json.DjangoJSONEncoder,
                ensure_ascii=False)
        super(JsonResponse, self).__init__(
            content, content_type='application/json')
