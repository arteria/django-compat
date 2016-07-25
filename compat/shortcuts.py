

from compat import urlresolvers
from django.utils.functional import Promise


def resolve_url(to, *args, **kwargs):
    """
    Return a URL appropriate for the arguments passed.
    The arguments could be:
        * A model: the model's `get_absolute_url()` function will be called.
        * A view name, possibly with arguments: `urlresolvers.reverse()` will
          be used to reverse-resolve the name.
        * A URL, which will be returned as-is.
    """
    from compat import six, force_text

    # If it's a model, use get_absolute_url()
    if hasattr(to, 'get_absolute_url'):
        return to.get_absolute_url()

    if isinstance(to, Promise):
        # Expand the lazy instance, as it can cause issues when it is passed
        # further to some Python functions like urlparse.
        to = force_text(to)

    if isinstance(to, six.string_types):
        # Handle relative URLs
        if any(to.startswith(path) for path in ('./', '../')):
            return to

    # Next try a reverse URL resolution.
    try:
        return urlresolvers.reverse(to, args=args, kwargs=kwargs)
    except urlresolvers.NoReverseMatch:
        # If this is a callable, re-raise.
        if callable(to):
            raise
        # If this doesn't "feel" like a URL, re-raise.
        if '/' not in to and '.' not in to:
            raise

    # Finally, fall back and assume it's a URL
    return to
