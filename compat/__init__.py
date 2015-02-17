# flake8: noqa
from __future__ import unicode_literals

import sys
import inspect
import django

from django.conf import settings 

from django.core.exceptions import ImproperlyConfigured

try:
    from importlib import import_module
except ImportError:  # Fallback for Python 2.6 & Django < 1.7
    from django.utils.importlib import import_module

try:
    # django 1.4.2+ , https://docs.djangoproject.com/en/1.5/topics/python3/#philosophy
    from django.utils import six
except ImportError:
    import six
    
# get_indent
if six.PY3:
    from threading import get_ident
else:
    from thread import get_ident  # noqa

try:
    from django.conf.urls import url, patterns, include, handler404, handler500
except ImportError:
    from django.conf.urls.defaults import url, patterns, include, handler404, handler500 # pyflakes:ignore



# Handle django.utils.encoding rename in 1.5 onwards.
# smart_unicode -> smart_text
# force_unicode -> force_text
try:
    from django.utils.encoding import smart_text
except ImportError:
    from django.utils.encoding import smart_unicode as smart_text
try:
    from django.utils.encoding import force_text
except ImportError:
    from django.utils.encoding import force_unicode as force_text
    
    

if django.VERSION >= (1, 6):
    def clean_manytomany_helptext(text):
        return text
else:
    # Up to version 1.5 many to many fields automatically suffix
    # the `help_text` attribute with hardcoded text.
    def clean_manytomany_helptext(text):
        if text.endswith(' Hold down "Control", or "Command" on a Mac, to select more than one.'):
            text = text[:-69]
        return text
        
        

# cStringIO only if it's available, otherwise StringIO
try:
    import cStringIO.StringIO as StringIO
except ImportError:
    StringIO = six.StringIO

BytesIO = six.BytesIO


def get_model_name(model_cls):
    try:
        return model_cls._meta.model_name
    except AttributeError:
        # < 1.6 used module_name instead of model_name
        return model_cls._meta.module_name
        

# View._allowed_methods only present from 1.5 onwards
if django.VERSION >= (1, 5):
    from django.views.generic import View
else:
    from django.views.generic import View as DjangoView

    class View(DjangoView):
        def _allowed_methods(self):
            return [m.upper() for m in self.http_method_names if hasattr(self, m)]



# URLValidator only accepts `message` in 1.6+
if django.VERSION >= (1, 6):
    from django.core.validators import URLValidator
else:
    from django.core.validators import URLValidator as DjangoURLValidator

    class URLValidator(DjangoURLValidator):
        def __init__(self, *args, **kwargs):
            self.message = kwargs.pop('message', self.message)
            super(URLValidator, self).__init__(*args, **kwargs)

# EmailValidator requires explicit regex prior to 1.6+
if django.VERSION >= (1, 6):
    from django.core.validators import EmailValidator
else:
    from django.core.validators import EmailValidator as DjangoEmailValidator
    from django.core.validators import email_re

    class EmailValidator(DjangoEmailValidator):
        def __init__(self, *args, **kwargs):
            super(EmailValidator, self).__init__(email_re, *args, **kwargs)


try:
    from django.utils.encoding import python_2_unicode_compatible
except ImportError:
    def python_2_unicode_compatible(klass):
        """
        A decorator that defines __unicode__ and __str__ methods under Python 2.
        Under Python 3 it does nothing.
        To support Python 2 and 3 with a single code base, define a __str__ method
        returning text and apply this decorator to the class.
        """
        if '__str__' not in klass.__dict__:
            raise ValueError("@python_2_unicode_compatible cannot be applied "
                             "to %s because it doesn't define __str__()." %
                             klass.__name__)
        klass.__unicode__ = klass.__str__
        klass.__str__ = lambda self: self.__unicode__().encode('utf-8')
        return klass
        
try:
    import unittest2 as unittest
except ImportError:
    import unittest  # pyflakes:ignore
try:
    from unittest import mock  # Since Python 3.3 mock is is in stdlib
except ImportError:
    try:
        import mock # pyflakes:ignore
    except ImportError:
        # mock is used for tests only however it is hard to check if user is
        # running tests or production code so we fail silently here; mock is
        # still required for tests at setup.py (See PR #193)
        pass

# Django 1.5 compatibility utilities, providing support for custom User models.
# Since get_user_model() causes a circular import if called when app models are
# being loaded, the user_model_label should be used when possible, with calls
# to get_user_model deferred to execution time

user_model_label = getattr(settings, 'AUTH_USER_MODEL', 'auth.User')

"""
try:
    from django.contrib.auth import get_user_model
except ImportError:
    from django.contrib.auth.models import User
    get_user_model = lambda: User
"""
try:
    get_user_model = lambda: settings.AUTH_USER_MODEL
except:
    try:
        from django.contrib.auth import get_user_model
    except ImportError:
        from django.contrib.auth.models import User
        get_user_model = lambda: User


# get_username_field
if django.VERSION >= (1, 5):
    def get_username_field():
        return get_user_model().USERNAME_FIELD
else:
    def get_username_field():
            return 'username'
            
            
def get_user_model_path():
    """
    Returns 'app_label.ModelName' for User model. Basically if
    ``AUTH_USER_MODEL`` is set at settings it would be returned, otherwise
    ``auth.User`` is returned.
    """
    return getattr(settings, 'AUTH_USER_MODEL', 'auth.User')

def get_user_permission_full_codename(perm):
    """
    Returns 'app_label.<perm>_<usermodulename>'. If standard ``auth.User`` is
    used, for 'change' perm this would return ``auth.change_user`` and if
    ``myapp.CustomUser`` is used it would return ``myapp.change_customuser``.
    """
    User = get_user_model()
    return '%s.%s_%s' % (User._meta.app_label, perm, User._meta.module_name)

def get_user_permission_codename(perm):
    """
    Returns '<perm>_<usermodulename>'. If standard ``auth.User`` is
    used, for 'change' perm this would return ``change_user`` and if
    ``myapp.CustomUser`` is used it would return ``change_customuser``.
    """
    return get_user_permission_full_codename(perm).split('.')[1]


def import_string(dotted_path):
    """
    Import a dotted module path and return the attribute/class designated by the
    last name in the path. Raise ImportError if the import failed.
    Backported from Django 1.7
    """
    try:
        module_path, class_name = dotted_path.rsplit('.', 1)
    except ValueError:
        msg = "%s doesn't look like a module path" % dotted_path
        six.reraise(ImportError, ImportError(msg), sys.exc_info()[2])

    module = import_module(module_path)

    try:
        return getattr(module, class_name)
    except AttributeError:
        msg = 'Module "%s" does not define a "%s" attribute/class' % (
            dotted_path, class_name)
        six.reraise(ImportError, ImportError(msg), sys.exc_info()[2])


# HttpResponseBase only exists from 1.5 onwards
try:
    from django.http.response import HttpResponseBase
except ImportError:
    from django.http import HttpResponse as HttpResponseBase
    
    
# Python 3
try:
    unicode = unicode # pyflakes:ignore
    basestring = basestring # pyflakes:ignore
    str = str # pyflakes:ignore
except NameError:
    basestring = unicode = str = str


# urlparse in python3 has been renamed to urllib.parse 
try:
    from urlparse import urlparse, parse_qs, urlunparse
except ImportError:
    from urllib.parse import urlparse, parse_qs, urlunparse

try:
    from urllib import urlencode, unquote_plus
except ImportError:
    from urllib.parse import urlencode, unquote_plus
    
    
    
# Django 1.7 compatibility
try:
    from django.http import JsonResponse
except:
    from .json_response import JsonResponse
    
# create_permission API changed: skip the create_models (second
# positional argument) if we have django 1.7+ and 2+ positional
# arguments with the second one being a list/tuple 
def create_permissions(*args, **kwargs):
    from django.contrib.auth.management import create_permissions as original_create_permissions
    if django.get_version().split('.')[:2] >= ['1','7'] and \
        len(args) > 1 and isinstance(args[1], (list, tuple)):
        args = args[:1] + args[2:]
    return original_create_permissions(*args, **kwargs)

# Requires django < 1.5 or python >= 2.6
if django.VERSION < (1,5):
    from django.utils import simplejson
else:
    import json as simplejson


### Undocumented ###

try:
    from django.template import VariableNode
except:
    from django.template.base import VariableNode
    
#the tests will try to import these
__all__ = [ 
    'get_model_name',
    'get_user_model',
    'get_username_field',
    'import_string',
    'user_model_label',
    'url',
    'patterns',
    'include',
    'handler404',
    'handler500',
    'get_ident',
   # 'mock',
   # 'unittest',
    'urlparse', 
    'parse_qs', 
    'urlunparse',
    'urlencode', 
    'unquote_plus',
    'JsonResponse',
    'HttpResponseBase',
    'python_2_unicode_compatible',
    'URLValidator',
    'EmailValidator',
    'View', 
    'StringIO',
    'BytesIO',
    'clean_manytomany_helptext', 
    'smart_text',
    'force_text',
    'simplejson',
    'import_module',
    'VariableNode',
]
