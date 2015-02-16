from django.test import TestCase

class CompatTests(TestCase):

    def test_compat(self):
        from importlib import import_module
        from compat import __all__
        
        compat = import_module('compat')

        for n in __all__:
            getattr(compat, n)

        self.assertTrue(True)