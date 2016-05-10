# Source: https://github.com/django/django/tree/stable/1.9.x/tests/utils_tests/test_module

class SiteMock(object):
    _registry = {}
site = SiteMock()
