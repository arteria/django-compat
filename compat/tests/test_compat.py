from django.test import TestCase

from compat import format_html

class CompatTests(TestCase):

    def test_compat(self):
        from importlib import import_module
        from compat import __all__

        compat = import_module('compat')

        for n in __all__:
            getattr(compat, n)

        self.assertTrue(True)

    def test_format_html(self):
        """
        Test: format_html
        url: https://github.com/django/django/blob/stable/1.8.x/tests/utils_tests/test_html.py#L44-L53

        """

        from django.utils import html

        from compat import format_html

        self.assertEqual(
            format_html("{} {} {third} {fourth}",
                             "< Dangerous >",
                             html.mark_safe("<b>safe</b>"),
                             third="< dangerous again",
                             fourth=html.mark_safe("<i>safe again</i>")
                             ),
            "&lt; Dangerous &gt; <b>safe</b> &lt; dangerous again <i>safe again</i>"
        )