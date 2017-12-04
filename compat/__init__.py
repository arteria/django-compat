# flake8: noqa
from __future__ import unicode_literals

import sys
import django

from django.conf import settings

# removed get_queryset <> get_query_set see, #29
#from django.db.models import Manager
## Monkey patch:
#
#try:
#    Manager.get_query_set = Manager.get_queryset
#except AttributeError:
#    Manager.get_queryset = Manager.get_query_set
from django.core.exceptions import ImproperlyConfigured

if django.VERSION < (1, 8):
    from django.template import add_to_builtins
elif django.VERSION < (1, 9):
    from django.template.base import add_to_builtins
else:
    pass  # Removed in 1.9. Use template settings instead


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
try:
    from threading import get_ident
except ImportError:
    from six.moves._thread import get_ident  # noqa

try:
    from django.conf.urls import url, include, handler404, handler500
except ImportError:
    from django.conf.urls.defaults import url, include, handler404, handler500  # pyflakes:ignore

try:
    from django.conf.urls import patterns
except ImportError:
    try:
        from django.conf.urls.defaults import patterns # pyflakes:ignore
    except ImportError:
        pass


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

try:
    # Django 1.7 or over use the new application loading system
    from django.apps import apps
    get_model = apps.get_model
except ImportError:
    from django.db.models.loading import get_model


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
        import mock  # pyflakes:ignore
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


# get_username_field
if django.VERSION >= (1, 5):
    def get_username_field():
        return get_user_model().USERNAME_FIELD
else:
    def get_username_field():
        return 'username'

try:
    from django.contrib.auth import get_user_model
except ImportError:
    from django.contrib.auth.models import User
    get_user_model = lambda: User


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


def commit(using=None):
    """
    Possibility of calling transaction.commit() in new Django versions (in atomic block).
    """
    try:
        django.db.transaction.commit(using)
    except django.db.transaction.TransactionManagementError:
        pass


def rollback(using=None, sid=None):
    """
    Possibility of calling transaction.rollback() in new Django versions (in atomic block).
    Important: transaction savepoint (sid) is required for Django < 1.8
    """
    if sid:
        django.db.transaction.savepoint_rollback(sid)
    else:
        try:
             django.db.transaction.rollback(using)
        except django.db.transaction.TransactionManagementError:
             django.db.transaction.set_rollback(True, using)


# HttpResponseBase only exists from 1.5 onwards
try:
    from django.http.response import HttpResponseBase
except ImportError:
    from django.http import HttpResponse as HttpResponseBase


# Python 3
try:
    unicode = unicode  # pyflakes:ignore
    basestring = basestring  # pyflakes:ignore
    str = str  # pyflakes:ignore
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


def create_permissions(*args, **kwargs):
    # create_permission API changed: skip the create_models (second
    # positional argument) if we have django 1.7+ and 2+ positional
    # arguments with the second one being a list/tuple
    from django.contrib.auth.management import create_permissions as original_create_permissions
    if django.VERSION < (1, 7) and len(args) > 1 and isinstance(args[1], (list, tuple)):
        args = args[:1] + args[2:]
    return original_create_permissions(*args, **kwargs)


# Requires django < 1.5 or python >= 2.6
if django.VERSION < (1, 5):
    from django.utils import simplejson
else:
    import json as simplejson

try:
    from collections import OrderedDict as SortedDict
except ImportError:
    from django.utils.datastructures import SortedDict


# Backporting from 1.8
if django.VERSION < (1, 8):
    from compat.json_response import DjangoJSONEncoder
else:
    from django.core.serializers.json import DjangoJSONEncoder


if django.VERSION < (1, 8):
    from compat.json_response import JsonResponse
else:
    from django.http import JsonResponse


# format_html (django 1.6)

try:
    from django.utils.html import format_html, conditional_escape
except ImportError:
    # support django < 1.5. Taken from django.utils.html
    from django.utils import html

    def format_html(format_string, *args, **kwargs):
        """
        Similar to str.format, but passes all arguments through conditional_escape,
        and calls 'mark_safe' on the result. This function should be used instead
        of str.format or % interpolation to build up small HTML fragments.
        """
        args_safe = map(html.conditional_escape, args)
        kwargs_safe = dict([(k, html.conditional_escape(v)) for (k, v) in
                            six.iteritems(kwargs)])
        return html.mark_safe(format_string.format(*args_safe, **kwargs_safe))

try:
    from django.db import close_old_connections as close_connection
except ImportError:  # django < 1.8
    from django.db import close_connection


def get_template_loaders():
    """
    Compatibility method to fetch the template loaders.
    Source: https://github.com/django-debug-toolbar/django-debug-toolbar/blob/ece1c2775af108a92a0ef59636266b49e286e916/debug_toolbar/compat.py
    """
    try:
        from django.template.engine import Engine
    except ImportError:  # Django < 1.8
        Engine = None

    if Engine:
        try:
            engine = Engine.get_default()
        except ImproperlyConfigured:
            loaders = []
        else:
            loaders = engine.template_loaders
    else:  # Django < 1.8
        from django.template.loader import find_template_loader
        loaders = [
            find_template_loader(loader_name)
            for loader_name in settings.TEMPLATE_LOADERS]
    return loaders


if django.VERSION >= (2, 0):
    from django.urls import (
        clear_url_caches, get_script_prefix, get_urlconf,
        is_valid_path, resolve, reverse, reverse_lazy, set_script_prefix,
        set_urlconf, NoReverseMatch, URLPattern,
        URLResolver, Resolver404, ResolverMatch, get_ns_resolver, get_resolver, get_callable, get_mod_func
    )
    RegexURLPattern = URLPattern
    RegexURLResolver = URLResolver
elif django.VERSION >= (1, 10):
    import django.urls as urlresolvers
    from django.urls import (
        clear_url_caches, get_script_prefix, get_urlconf,
        is_valid_path, resolve, reverse, reverse_lazy, set_script_prefix,
        set_urlconf, LocaleRegexProvider, LocaleRegexURLResolver, NoReverseMatch, RegexURLPattern,
        RegexURLResolver, Resolver404, ResolverMatch, get_ns_resolver, get_resolver, get_callable, get_mod_func
    )
    URLPattern = RegexURLPattern
    URLResolver = RegexURLResolver
else:
    import django.core.urlresolvers as urlresolvers
    from django.core.urlresolvers import (
        clear_url_caches, get_script_prefix, get_urlconf,
        is_valid_path, resolve, reverse, reverse_lazy, set_script_prefix,
        set_urlconf, LocaleRegexProvider, LocaleRegexURLResolver, NoReverseMatch, RegexURLPattern,
        RegexURLResolver, Resolver404, ResolverMatch, get_ns_resolver, get_resolver, get_callable, get_mod_func
    )
    URLPattern = RegexURLPattern
    URLResolver = RegexURLResolver

try:
    from django.shortcuts import resolve_url
except ImportError:  # django < 1.5
    from .shortcuts import resolve_url



from django.template.loader import render_to_string as render_to_string_django

_context_instance_undefined = object()
_dictionary_undefined = object()
_dirs_undefined = object()

def render_to_string(template_name, context=None,
                     context_instance=_context_instance_undefined,
                     dirs=_dirs_undefined,
                     dictionary=_dictionary_undefined,
                     request=None, using=None):
    if (context_instance is _context_instance_undefined and dirs is _dirs_undefined and
            dictionary is _dictionary_undefined):
        if django.VERSION >= (1, 8):
            # Call new render_to_string with new arguments
            return render_to_string_django(template_name, context, request, using)
        else:
            # Call legacy render_to_string with new arguments
            from django.template import RequestContext
            context_instance = RequestContext(request) if request else None
            return render_to_string_django(template_name, context, context_instance)
    else:
        if django.VERSION >= (1, 10):
            # Call new render_to_string with legacy arguments
            raise NotImplementedError('Django compat does not support calling post-1.8 render_to_string with pre-1.8 '
                                      'keyword arguments')
        else:
            # Call legacy render_to_string with legacy arguments
            if dictionary is _dictionary_undefined:
                dictionary = {}
            if context_instance is _context_instance_undefined:
                context_instance = None
            return render_to_string_django(template_name, dictionary, context_instance)


### Undocumented ###

try:
    from django.template import VariableNode
except:
    from django.template.base import VariableNode

# slugify template filter is available as a standard python function at django.utils.text since django 1.5
try:
    from django.utils.text import slugify
except:
    from django.template.defaultfilters import slugify

if django.VERSION < (1, 7):
    from django.contrib.contenttypes.generic import GenericForeignKey
elif django.VERSION < (1, 9):
    from django.contrib.contenttypes.fields import GenericForeignKey
else:
    pass  # Loading models from __init__ is deprecated from 1.9. Import from compat.models instead

# commit_on_success replaced by atomic in Django >=1.8
atomic = commit_on_success = getattr(django.db.transaction, 'atomic', None) or getattr(django.db.transaction, 'commit_on_success')

# Removed from django.contrib.sites.models in Django 1.9
try:
    from django.contrib.sites.shortcuts import get_current_site
except ImportError:
    from django.contrib.sites.models import get_current_site

# Renamed utils and removed in Django 1.9
try:
    from django.contrib.admin import utils as admin_utils
except ImportError:
    from django.contrib.admin import util as admin_utils

# the tests will try to import these
__all__ = [
    'add_to_builtins',
    'get_model',
    'get_model_name',
    'get_user_model',
    'get_username_field',
    'import_string',
    'commit',
    'rollback',
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
    'DjangoJSONEncoder',
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
    'slugify',
    'GenericForeignKey',
    'SortedDict',
    'atomic',
    'commit_on_success', # alias
    'format_html',
    'resolve_url',
    'close_connection',
    'get_template_loaders',
    'LocaleRegexProvider', 'LocaleRegexURLResolver', 'NoReverseMatch',
    'RegexURLPattern', 'RegexURLResolver', # Old names before 2.0, alias after
    'URLPattern', 'URLResolver', # New names in 2.0, alias before
    'Resolver404', 'ResolverMatch', 'clear_url_caches', 'get_callable', 'get_mod_func', 'get_ns_resolver',
    'get_resolver', 'get_script_prefix', 'get_urlconf', 'is_valid_path', 'resolve', 'reverse', 'reverse_lazy',
    'set_script_prefix', 'set_urlconf',
    'render_to_string',
    'get_current_site',
    'admin_utils'
]
