
try:
    from compat import GenericForeignKey
except ImportError:  # Django >= 1.9
    from django.contrib.contenttypes.fields import GenericForeignKey

# the tests will try to import these
__all__ = [
    'GenericForeignKey',
]
