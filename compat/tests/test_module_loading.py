import sys

import imp

from django.test import TestCase
from django.utils.module_loading import module_has_submodule

from compat import import_module


class DefaultLoader(TestCase):
    def setUp(self):
        sys.meta_path.insert(0, ProxyFinder())

    def tearDown(self):
        sys.meta_path.pop(0)

    def test_loader(self):
        "Normal module existence can be tested"
        test_module = import_module('compat.tests.utils_tests.test_module')
        test_no_submodule = import_module(
            'compat.tests.utils_tests.test_no_submodule')

        # An importable child
        self.assertTrue(module_has_submodule(test_module, 'good_module'))
        mod = import_module('compat.tests.utils_tests.test_module.good_module')
        self.assertEqual(mod.content, 'Good Module')

        # A child that exists, but will generate an import error if loaded
        self.assertTrue(module_has_submodule(test_module, 'bad_module'))
        with self.assertRaises(ImportError):
            import_module('compat.tests.utils_tests.test_module.bad_module')

        # A child that doesn't exist
        self.assertFalse(module_has_submodule(test_module, 'no_such_module'))
        with self.assertRaises(ImportError):
            import_module('compat.tests.utils_tests.test_module.no_such_module')

        # A child that doesn't exist, but is the name of a package on the path
        self.assertFalse(module_has_submodule(test_module, 'django'))
        with self.assertRaises(ImportError):
            import_module('compat.tests.utils_tests.test_module.django')

        # Don't be confused by caching of import misses
        import types  # NOQA: causes attempted import of utils_tests.types
        self.assertFalse(module_has_submodule(sys.modules['compat.tests.utils_tests'], 'types'))

        # A module which doesn't have a __path__ (so no submodules)
        self.assertFalse(module_has_submodule(test_no_submodule, 'anything'))
        with self.assertRaises(ImportError):
            import_module('compat.tests.utils_tests.test_no_submodule.anything')


class ProxyFinder(object):
    def __init__(self):
        self._cache = {}

    def find_module(self, fullname, path=None):
        tail = fullname.rsplit('.', 1)[-1]
        try:
            fd, fn, info = imp.find_module(tail, path)
            if fullname in self._cache:
                old_fd = self._cache[fullname][0]
                if old_fd:
                    old_fd.close()
            self._cache[fullname] = (fd, fn, info)
        except ImportError:
            return None
        else:
            return self  # this is a loader as well

    def load_module(self, fullname):
        if fullname in sys.modules:
            return sys.modules[fullname]
        fd, fn, info = self._cache[fullname]
        try:
            return imp.load_module(fullname, fd, fn, info)
        finally:
            if fd:
                fd.close()
