
django-compat
=============
[![Build Status](https://travis-ci.org/arteria/django-compat.svg?branch=master)](https://travis-ci.org/arteria/django-compat)
[![Stories in Ready](https://badge.waffle.io/arteria/django-compat.png?label=ready&title=Ready)](https://waffle.io/arteria/django-compat)

Forward and backwards compatibility layer for Django 1.4, 1.7, 1.8, and 1.9

~~Consider [django-compat](https://github.com/arteria/django-compat) as an experiment based on the discussion [on reddit](http://redd.it/2jrr4l). Let's see where it goes.~~

What started as an experiment based on [this discussion on reddit](http://redd.it/2jrr4l) has proven to be true in real life. 

django-compat is under active development. To learn about other features, bug fixes, and changes, please refer to the [changelog](https://github.com/arteria/django-compat#changelog). 

# Who uses django-compat

Two popular examples of open source reusable app that uses django-compat are [django-hijack](https://github.com/arteria/django-hijack/) and [django-background-tasks](https://github.com/arteria/django-background-tasks).   
Want to have yours listed here? Send us a PR. 

# Why use django-compat

* Be able to use the LTS versions of Django and support newer versions in your app
* Use features from newer Django versions in an old one
* Manage and master the gap between different framework versions

# How to use django-compat

Install compat from the [PyPI](https://pypi.python.org/pypi/django-compat) or download and install manually. All relevant  releases are listed [here under releases](https://github.com/arteria/django-compat/releases).

Using one of the compatible objects is easy. For example

	from compat import patterns, url

	urlpatterns = patterns('ABC.views',
    		url(r'^abc/$', 'abc', name='abc-link'),
   	...
	
See a full example [here](https://github.com/arteria/django-hijack/blob/4966d8865e7e829a562ff2724771628c6590f841/hijack/urls.py#L1).



# Compatible objects

|Compatible object|Specifically tested|1.4|1.7|1.8|1.9|Notes|
|---|---|---|---|---|---|---|
|`BytesIO`|:heavy_multiplication_x:|:heavy_check_mark:|:heavy_check_mark:|:heavy_check_mark:|:heavy_check_mark:||
|`DjangoJSONEncoder`|:heavy_check_mark:|:heavy_check_mark:|:heavy_check_mark:|:heavy_check_mark:|:heavy_check_mark:||
|`EmailValidator`|:heavy_multiplication_x:|:heavy_check_mark:|:heavy_check_mark:|:heavy_check_mark:|:heavy_check_mark:||
|`GenericForeignKey`|:heavy_multiplication_x:|:heavy_check_mark:|:heavy_check_mark:|:heavy_check_mark:|:x:||
|`models.GenericForeignKey`|:heavy_multiplication_x:|:heavy_check_mark:|:heavy_check_mark:|:heavy_check_mark:|:heavy_check_mark:||
|`HttpResponseBase`|:heavy_multiplication_x:|:heavy_check_mark:|:heavy_check_mark:|:heavy_check_mark:|:heavy_check_mark:||
|`JsonResponse`|:heavy_check_mark:|:heavy_check_mark:|:heavy_check_mark:|:heavy_check_mark:|:heavy_check_mark:||
|`SortedDict`|:heavy_multiplication_x:|:heavy_check_mark:|:heavy_check_mark:|:heavy_check_mark:|:heavy_check_mark:||
|`StringIO`|:heavy_multiplication_x:|:heavy_check_mark:|:heavy_check_mark:|:heavy_check_mark:|:heavy_check_mark:||
|`URLValidator`|:heavy_multiplication_x:|:heavy_check_mark:|:heavy_check_mark:|:heavy_check_mark:|:heavy_check_mark:||
|`VariableNode`|:heavy_multiplication_x:|:heavy_check_mark:|:heavy_check_mark:|:heavy_check_mark:|:heavy_check_mark:||
|`View`|:heavy_multiplication_x:|:heavy_check_mark:|:heavy_check_mark:|:heavy_check_mark:|:heavy_check_mark:||
|`add_to_builtins`|:heavy_multiplication_x:|:heavy_check_mark:|:heavy_check_mark:|:heavy_check_mark:|:x:||
|`atomic`|:heavy_multiplication_x:|:heavy_check_mark:|:heavy_check_mark:|:heavy_check_mark:|:heavy_check_mark:||
|`clean_manytomany_helptext`|:heavy_multiplication_x:|:heavy_check_mark:|:heavy_check_mark:|:heavy_check_mark:|:heavy_check_mark:||
|`close_connection`|:heavy_multiplication_x:|:heavy_check_mark:|:heavy_check_mark:|:heavy_check_mark:|:heavy_check_mark:||
|`commit`|:heavy_check_mark:|:heavy_check_mark:|:heavy_check_mark:|:heavy_check_mark:|:heavy_check_mark:||
|`commit_on_success`|:heavy_check_mark:|:heavy_check_mark:|:heavy_check_mark:|:heavy_check_mark:|:heavy_check_mark:|`commit_on_success` replaced by `atomic` in Django >= 1.8|
|`force_text`|:heavy_multiplication_x:|:heavy_check_mark:|:heavy_check_mark:|:heavy_check_mark:|:heavy_check_mark:||
|`format_html`|:heavy_check_mark:|:heavy_check_mark:|:heavy_check_mark:|:heavy_check_mark:|:heavy_check_mark:||
|`get_ident`|:heavy_multiplication_x:|:heavy_check_mark:|:heavy_check_mark:|:heavy_check_mark:|:heavy_check_mark:||
|`get_model`|:heavy_multiplication_x:|:heavy_check_mark:|:heavy_check_mark:|:heavy_check_mark:|:heavy_check_mark:||
|`get_model_name`|:heavy_multiplication_x:|:heavy_check_mark:|:heavy_check_mark:|:heavy_check_mark:|:heavy_check_mark:||
|`get_template_loaders`|:heavy_check_mark:|:heavy_check_mark:|:heavy_check_mark:|:heavy_check_mark:|:heavy_check_mark:||
|`get_user_model`|:heavy_multiplication_x:|:heavy_check_mark:|:heavy_check_mark:|:heavy_check_mark:|:heavy_check_mark:||
|`get_username_field`|:heavy_multiplication_x:|:heavy_check_mark:|:heavy_check_mark:|:heavy_check_mark:|:heavy_check_mark:||
|`handler404`|:heavy_multiplication_x:|:heavy_check_mark:|:heavy_check_mark:|:heavy_check_mark:|:heavy_check_mark:||
|`handler500`|:heavy_multiplication_x:|:heavy_check_mark:|:heavy_check_mark:|:heavy_check_mark:|:heavy_check_mark:||
|`import_module`|:heavy_check_mark:|:heavy_check_mark:|:heavy_check_mark:|:heavy_check_mark:|:heavy_check_mark:||
|`import_string`|:heavy_multiplication_x:|:heavy_check_mark:|:heavy_check_mark:|:heavy_check_mark:|:heavy_check_mark:||
|`include`|:heavy_multiplication_x:|:heavy_check_mark:|:heavy_check_mark:|:heavy_check_mark:|:heavy_check_mark:||
|`parse_qs`|:heavy_multiplication_x:|:heavy_check_mark:|:heavy_check_mark:|:heavy_check_mark:|:heavy_check_mark:||
|`patterns`|:heavy_multiplication_x:|:heavy_check_mark:|:heavy_check_mark:|:heavy_check_mark:|:heavy_check_mark:||
|`python_2_unicode_compatible`|:heavy_multiplication_x:|:heavy_check_mark:|:heavy_check_mark:|:heavy_check_mark:|:heavy_check_mark:||
|`render_to_string`|:heavy_check_mark:|:heavy_check_mark:|:heavy_check_mark:|:heavy_check_mark:|:heavy_check_mark:|The new function signature (https://docs.djangoproject.com/en/1.9/releases/1.8/#dictionary-and-context-instance-arguments-of-rendering-functions) is backported to pre-1.8.|
|`resolve_url`|:heavy_check_mark:|:heavy_check_mark:|:heavy_check_mark:|:heavy_check_mark:|:heavy_check_mark:||
|`rollback`|:heavy_check_mark:|:heavy_check_mark:|:heavy_check_mark:|:heavy_check_mark:|:heavy_check_mark:|Transaction savepoint (sid) is required for Django < 1.8|
|`simplejson`|:heavy_multiplication_x:|:heavy_check_mark:|:heavy_check_mark:|:heavy_check_mark:|:heavy_check_mark:||
|`slugify`|:heavy_multiplication_x:|:heavy_check_mark:|:heavy_check_mark:|:heavy_check_mark:|:heavy_check_mark:||
|`smart_text`|:heavy_multiplication_x:|:heavy_check_mark:|:heavy_check_mark:|:heavy_check_mark:|:heavy_check_mark:||
|`unquote_plus`|:heavy_multiplication_x:|:heavy_check_mark:|:heavy_check_mark:|:heavy_check_mark:|:heavy_check_mark:||
|`url`|:heavy_multiplication_x:|:heavy_check_mark:|:heavy_check_mark:|:heavy_check_mark:|:heavy_check_mark:|Function used in `urlpatterns`|
|`templatetags.compat.url`|:heavy_check_mark:|:heavy_check_mark:|:heavy_check_mark:|:heavy_check_mark:|:heavy_check_mark:|Templatetag; import with `{% load url from compat %}`|
|`urlencode`|:heavy_multiplication_x:|:heavy_check_mark:|:heavy_check_mark:|:heavy_check_mark:|:heavy_check_mark:||
|`urlparse`|:heavy_multiplication_x:|:heavy_check_mark:|:heavy_check_mark:|:heavy_check_mark:|:heavy_check_mark:||
|`urlunparse`|:heavy_multiplication_x:|:heavy_check_mark:|:heavy_check_mark:|:heavy_check_mark:|:heavy_check_mark:||
|`user_model_label`|:heavy_multiplication_x:|:heavy_check_mark:|:heavy_check_mark:|:heavy_check_mark:|:heavy_check_mark:||
|`templatetags.compat.verbatim`|:heavy_check_mark:|:warning:|:heavy_check_mark:|:heavy_check_mark:|:heavy_check_mark:|Templatetag; import with `{% load verbatim from compat %}`. 1.4: Does not allow specific closing tags, e.g. `{% endverbatim myblock %}`, and does not preserve whitespace inside tags.|

# Resources and references 

## Resources 
* https://github.com/ubernostrum/django-compat-lint
* https://docs.djangoproject.com/en/dev/misc/api-stability/
* https://docs.djangoproject.com/en/dev/topics/python3/
* http://andrewsforge.com/presentation/upgrading-django-to-17/ 
 
## compat.py

Bits and bites of the following projects were re-used to build [django-compat](https://github.com/arteria/django-compat).

- [x] https://github.com/lukaszb/django-guardian/blob/devel/guardian/compat.py
- [X] https://github.com/evonove/django-oauth-toolkit/blob/master/oauth2_provider/compat.py
- [X] https://github.com/toastdriven/django-tastypie/blob/master/tastypie/compat.py
- [X] https://github.com/tomchristie/django-rest-framework/blob/master/rest_framework/compat.py
	- [ ] TODO: MinValueValidator, MaxValueValidator et al. (other relevant bits are included) Django 1.8
- [X] https://gist.github.com/theskumar/ff8de60ff6a33bdacaa8
- [X] https://github.com/evonove/django-oauth-toolkit/blob/master/oauth2_provider/templatetags/compat.py
- [ ] https://github.com/kennethreitz/requests/blob/master/requests/compat.py
- [ ] https://github.com/mitsuhiko/jinja2/blob/master/jinja2/_compat.py
- [ ] https://github.com/jaraco/setuptools/blob/master/setuptools/compat.py 
- [ ] https://github.com/mariocesar/sorl-thumbnail/blob/master/sorl/thumbnail/compat.py


# Changelog

### 2015/11/12

* Added `{% load url from compat %}`

### 2015/11/11

* 1.9 compatibility for existing objects with the following changes:
	* ``add_to_builtins`` was removed for Django >= 1.9
	* ``GenericForeignKey` was moved to ``compat.models`` for Django >= 1.9

### 2015/07/15

* ``add_to_builtins`` was added 

### 2015/07/08 
* ``get_query_set``/``get_queryset`` support was dropped again (see [#29](https://github.com/arteria/django-compat/issues/29)) 
