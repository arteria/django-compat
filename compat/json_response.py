from __future__ import unicode_literals

import datetime
import decimal
import uuid

from django.http import HttpResponse
from django.utils.timezone import is_aware

from compat import simplejson


class DjangoJSONEncoder(simplejson.JSONEncoder):
    """
    JSONEncoder subclass that knows how to encode date/time, decimal types and UUIDs.
    """
    def default(self, o):
        # See "Date Time String Format" in the ECMA-262 specification.
        if isinstance(o, datetime.datetime):
            r = o.isoformat()
            if o.microsecond:
                r = r[:23] + r[26:]
            if r.endswith('+00:00'):
                r = r[:-6] + 'Z'
            return r
        elif isinstance(o, datetime.date):
            return o.isoformat()
        elif isinstance(o, datetime.time):
            if is_aware(o):
                raise ValueError("JSON can't represent timezone-aware times.")
            r = o.isoformat()
            if o.microsecond:
                r = r[:12]
            return r
        elif isinstance(o, decimal.Decimal):
            return str(o)
        elif isinstance(o, uuid.UUID):
            return str(o)
        else:
            return super(DjangoJSONEncoder, self).default(o)


class JsonResponse(HttpResponse):
    """
    An HTTP response class that consumes data to be serialized to JSON.
    :param data: Data to be dumped into json. By default only ``dict`` objects
      are allowed to be passed due to a security flaw before EcmaScript 5. See
      the ``safe`` parameter for more information.
    :param encoder: Should be an json encoder class. Defaults to
      ``django.core.serializers.json.DjangoJSONEncoder``.
    :param safe: Controls if only ``dict`` objects may be serialized. Defaults
      to ``True``.
    """

    def __init__(self, data, encoder=DjangoJSONEncoder, safe=True, **kwargs):
        if safe and not isinstance(data, dict):
            raise TypeError('In order to allow non-dict objects to be '
                'serialized set the safe parameter to False')
        kwargs.setdefault('content_type', 'application/json')
        data = simplejson.dumps(data, cls=encoder)
        super(JsonResponse, self).__init__(content=data, **kwargs)

