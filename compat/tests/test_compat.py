# -*- encoding: utf-8 -*-
from __future__ import unicode_literals

import json
import uuid

import django
from django.contrib.admin.models import LogEntry
from django.core.serializers.json import DjangoJSONEncoder
from django.test import TestCase, SimpleTestCase
from django.test.client import RequestFactory
from django.contrib.auth.views import logout
try:
    from django.urls import NoReverseMatch
except ImportError:
    from django.core.urlresolvers import NoReverseMatch
from django.template import Template, Context, TemplateSyntaxError, RequestContext

import compat
from compat import (import_module, resolve_url, JsonResponse, get_model, render_to_string,
                    get_template_loaders, get_current_site)
from compat.docs.compatibility import is_compatible
from compat.tests.test_app.models import UnimportantThing


class CompatTests(TestCase):

    def test_is_compatible(self):
        self.assertTrue(is_compatible('get_model', (1, 4)))
        self.assertFalse(is_compatible('get_model', (1, 3)))
        self.assertFalse(is_compatible('Eyjafjallajoekull', (1, 4)))
        self.assertTrue(is_compatible('GenericForeignKey', (1, 4), module='models'))
        self.assertFalse(is_compatible('Eyjafjallajoekull', (1, 4), module='models'))

    def test_compat(self):
        compat = import_module('compat')
        for attribute in compat.__all__:
            if is_compatible(attribute, django.VERSION[:2]):
                self.assertTrue(hasattr(compat, attribute))

    def test_compat_models(self):
        compat_models = import_module('compat.models')
        for attribute in compat_models.__all__:
            if is_compatible(attribute, django.VERSION[:2], 'models'):
                self.assertTrue(hasattr(compat_models, attribute))

    def test_format_html(self):
        """
        Test: format_html
        url: https://github.com/django/django/blob/stable/1.8.x/tests/utils_tests/test_html.py#L44-L53

        """

        from django.utils import html

        from compat import format_html

        self.assertEqual(
            format_html("{0} {1} {third} {fourth}",
                             "< Dangerous >",
                             html.mark_safe("<b>safe</b>"),
                             third="< dangerous again",
                             fourth=html.mark_safe("<i>safe again</i>")
                             ),
            "&lt; Dangerous &gt; <b>safe</b> &lt; dangerous again <i>safe again</i>"
        )

    def test_resolve_url__url_path(self):
        """
        Tests that passing a URL path to ``resolve_url`` will result in the
        same url.
        """
        self.assertEqual('/something/', resolve_url('/something/'))

    def test_resolve_url__relative_path(self):
        """
        Tests that passing a relative URL path to ``resolve_url`` will result
        in the same url.
        """
        self.assertEqual('../', resolve_url('../'))
        self.assertEqual('../relative/', resolve_url('../relative/'))
        self.assertEqual('./', resolve_url('./'))
        self.assertEqual('./relative/', resolve_url('./relative/'))

    def test_resolve_url__full_url(self):
        """
        Tests that passing a full URL to ``resolve_url`` will result in the
        same url.
        """
        url = 'http://example.com/'
        self.assertEqual(url, resolve_url(url))

    def test_resolve_url__model(self):
        """
        Tests that passing a model to ``resolve_url`` will result in
        ``get_absolute_url`` being called on that model instance.
        """
        m = UnimportantThing(importance=1)
        self.assertEqual(m.get_absolute_url(), resolve_url(m))

    def test_resolve_url__view_function(self):
        """
        Tests that passing a view name to ``resolve_url`` will result in the
        URL path mapping to that view name.
        """
        resolved_url = resolve_url(logout)
        self.assertEqual('/accounts/logout/', resolved_url)

    '''
    incompatible with lower django versions
    def test_resolve_url__lazy_reverse(self):
        """
        Tests that passing the result of reverse_lazy is resolved to a real URL
        string.
        """
        from django.utils import six
        resolved_url = resolve_url(reverse_lazy('logout'))
        self.assertIsInstance(resolved_url, six.text_type)
        self.assertEqual('/accounts/logout/', resolved_url)
    '''

    if django.VERSION < (1, 10):
        def test_resolve_url__valid_view_name(self):
            """
            Tests that passing a view function to ``resolve_url`` will result in
            the URL path mapping to that view.
            """
            resolved_url = resolve_url('django.contrib.auth.views.logout')
            self.assertEqual('/accounts/logout/', resolved_url)

    def test_resolve_url__domain(self):
        """
        Tests that passing a domain to ``resolve_url`` returns the same domain.
        """
        self.assertEqual(resolve_url('example.com'), 'example.com')

    def test_resolve_url__non_view_callable_raises_no_reverse_match(self):
        """
        Tests that passing a non-view callable into ``resolve_url`` raises a
        ``NoReverseMatch`` exception.
        """
        with self.assertRaises(NoReverseMatch):
            resolve_url(lambda: 'asdf')

    def test_commit_on_success(self):
        """
        Test of commit_on_success
        """
        @compat.commit_on_success
        def db_action():
            m = UnimportantThing(pk=1, importance=1)
            m.save()

        db_action()
        self.assertEqual(UnimportantThing.objects.get(pk=1).importance, 1)

    def test_commit(self):
        """
        Test of commit
        """
        m = UnimportantThing(pk=2, importance=2)
        m.save()
        compat.commit()
        self.assertEqual(UnimportantThing.objects.get(pk=2).importance, 2)

    def test_rollback__with_sid(self):
        """
        Test of rollback with transaction savepoint
        """
        @compat.commit_on_success
        def db_action():
            m = UnimportantThing(pk=3, importance=3)
            m.save()
            return m

        @compat.commit_on_success
        def db_action_with_rollback(m):
            m.importance = 5
            sid = django.db.transaction.savepoint()
            m.save()
            compat.rollback(None, sid)

        if django.VERSION < (1, 5):  # Rollback doesn't work with SQLite
            return

        m = db_action()
        db_action_with_rollback(m)
        self.assertEqual(UnimportantThing.objects.get(pk=3).importance, 3)

    def test_rollback__without_sid(self):
        """
        Test of rollback without transaction savepoint
        """
        @compat.commit_on_success
        def db_action():
            m = UnimportantThing(pk=4, importance=4)
            m.save()
            return m

        @compat.commit_on_success
        def db_action_with_rollback(m):
            m.importance = 5
            m.save()
            compat.rollback()

        if django.VERSION < (1, 8):  # Rollback doesn't work after .save() if an exception isn't thrown
            return

        m = db_action()
        db_action_with_rollback(m)
        self.assertEqual(UnimportantThing.objects.get(pk=4).importance, 4)

    def test_url_template_tag(self):
        template = Template(
            '{% load url from compat %}'
            '<a href="{% url "logout" %}">Log out</a>'
        )
        html = template.render(Context({}))
        self.assertEqual(
            html,
            '<a href="/accounts/logout/">Log out</a>'
        )

    if django.VERSION < (1, 9):
        def test_add_to_builtins(self):
            from compat import add_to_builtins

            # Explicit import of tags
            template = Template(
                '{% load test_app_tags %}'
                '{% my_tag %}'
            )
            self.assertIn('Return value of my_tag', template.render(Context({})))

            # No import
            with self.assertRaises(TemplateSyntaxError):
                template = Template(
                    '{% my_tag %}'
                )
                template.render(Context({}))

            # No import but add_to_builtins call
            add_to_builtins('compat.tests.test_app.templatetags.test_app_tags')
            template = Template(
                '{% my_tag %}'
            )
            self.assertIn('Return value of my_tag', template.render(Context({})))

    def test_get_template_loaders(self):
        template_loaders = get_template_loaders()
        self.assertEqual(len(template_loaders), 2)
        self.assertIsInstance(template_loaders[0], django.template.loaders.filesystem.Loader)
        self.assertIsInstance(template_loaders[1], django.template.loaders.app_directories.Loader)

    class GetModelsTest(SimpleTestCase):
        """
        Sources:
        * https://github.com/django/django/blob/stable/1.9.x/tests/app_loading/tests.py
        * https://github.com/django/django/blob/stable/1.9.x/tests/apps/tests.py

        """
        def setUp(self):
            from compat.tests.utils_tests.not_installed import models
            self.not_installed_module = models

        def test_get_model_only_returns_installed_models(self):
            with self.assertRaises(LookupError):
                get_model("not_installed", "NotInstalledModel")

        def test_get_model(self):
            self.assertEqual(get_model('admin', 'LogEntry'), LogEntry)
            with self.assertRaises(LookupError):
                get_model('admin', 'LogExit')

            # App label is case-sensitive, Model name is case-insensitive.
            self.assertEqual(get_model('admin', 'loGentrY'), LogEntry)
            with self.assertRaises(LookupError):
                get_model('Admin', 'LogEntry')

            # A single argument is accepted.
            self.assertEqual(get_model('admin.LogEntry'), LogEntry)
            with self.assertRaises(LookupError):
                get_model('admin.LogExit')
            with self.assertRaises(ValueError):
                get_model('admin_LogEntry')


class VerbatimTagTestCase(TestCase):
    """
    Source: https://github.com/django/django/blob/master/tests/template_tests/syntax_tests/test_verbatim.py
    """

    def setUp(self):
        self.import_tag = '{% load verbatim from compat %}'

    def test_verbatim_tag01(self):
        template = Template(self.import_tag +
            '{% verbatim %}{{ bare }}{% endverbatim %}'
        )
        html = template.render(Context({}))
        self.assertEqual(html,
             '{{ bare }}'
        )

    def test_verbatim_tag02(self):
        template = Template(self.import_tag +
            '{% verbatim %}{% endif %}{% endverbatim %}'
        )
        html = template.render(Context({}))
        self.assertEqual(html,
             '{% endif %}'
        )

    def test_verbatim_tag03(self):
        template = Template(self.import_tag +
            '{% verbatim %}It\'s the {% verbatim %} tag{% endverbatim %}'
        )
        html = template.render(Context({}))
        self.assertEqual(html,
             'It\'s the {% verbatim %} tag'
        )

    def test_verbatim_tag04(self):
        with self.assertRaises(TemplateSyntaxError):
            Template(self.import_tag +
                '{% verbatim %}{% verbatim %}{% endverbatim %}{% endverbatim %}'
            )

    def test_verbatim_tag05(self):
        template = Template(self.import_tag +
            '{% verbatim %}{% endverbatim %}{% verbatim %}{% endverbatim %}'
        )
        html = template.render(Context({}))
        self.assertEqual(html, '')

    if django.VERSION >= (1, 5):  # Not implemented in 1.4
        def test_verbatim_tag06(self):
            template = Template(self.import_tag +
                '{% verbatim special %}'
                                  'Don\'t {% endverbatim %} just yet{% endverbatim special %}'
            )
            html = template.render(Context({}))
            self.assertEqual(html,
                 'Don\'t {% endverbatim %} just yet'
            )


class JsonResponseTests(SimpleTestCase):
    """
    Source: https://github.com/django/django/blob/master/tests/httpwrappers/tests.py
    """
    def test_json_response_non_ascii(self):
        data = {'key': 'łóżko'}
        response = JsonResponse(data)
        self.assertEqual(json.loads(response.content.decode()), data)

    def test_json_response_raises_type_error_with_default_setting(self):
        with self.assertRaises(TypeError):
            JsonResponse([1, 2, 3])

    def test_json_response_text(self):
        response = JsonResponse('foobar', safe=False)
        self.assertEqual(json.loads(response.content.decode()), 'foobar')

    def test_json_response_list(self):
        response = JsonResponse(['foo', 'bar'], safe=False)
        self.assertEqual(json.loads(response.content.decode()), ['foo', 'bar'])

    def test_json_response_uuid(self):
        u = uuid.uuid4()
        response = JsonResponse(u, safe=False)
        self.assertEqual(json.loads(response.content.decode()), str(u))

    def test_json_response_custom_encoder(self):
        class CustomDjangoJSONEncoder(DjangoJSONEncoder):
            def encode(self, o):
                return json.dumps({'foo': 'bar'})

        response = JsonResponse({}, encoder=CustomDjangoJSONEncoder)
        self.assertEqual(json.loads(response.content.decode()), {'foo': 'bar'})

    if django.VERSION >= (1, 9):
        def test_json_response_passing_arguments_to_json_dumps(self):
            response = JsonResponse({'foo': 'bar'}, json_dumps_params={'indent': 2})
            self.assertEqual(response.content.decode(), '{\n  "foo": "bar"\n}')

    def test_get_current_site(self):
        """
        Test of get_current_site
        """
        rf = RequestFactory()
        request = rf.get('/hello/')
        site = get_current_site(request)
        assert site


class RenderToStringTest(TestCase):

    template_name = 'test_context.html'

    def test_basic(self):
        self.assertEqual(render_to_string(self.template_name), 'obj:')

    def test_positional_arg(self):
        self.assertEqual(render_to_string(self.template_name, {'obj': 'test'}), 'obj:test')

    if django.VERSION < (1, 10):
        def test_dictionary_kwarg(self):
            self.assertEqual(render_to_string(self.template_name, dictionary={'obj': 'test'}), 'obj:test')

        def test_context_instance_kwarg(self):
            self.assertEqual(render_to_string(self.template_name, context_instance=Context({'obj': 'test'})), 'obj:test')

        def test_request_context(self):
            self.assertEqual(render_to_string(self.template_name, context_instance=RequestContext(None, {'obj': 'test'})), 'obj:test')

        def test_dictionary_and_context_instance_kwarg(self):
            self.assertEqual(render_to_string(self.template_name, dictionary={'obj': '1'}, context_instance=Context({'obj': '2'})), 'obj:1')

    # Fails 1.4
    def test_context_kwarg(self):
        self.assertEqual(render_to_string(self.template_name, context={'obj': 'test'}), 'obj:test')
