django-compat
=============

For- and backwards compatibility layer for Django 1.4.x to 1.8-alpha

Consider [django-compat](https://github.com/arteria/django-compat) as an experiment based on the discussion [on reddit](http://redd.it/2jrr4l). 
Let's see where it goes. 

# Compatible objects

* BytesIO
* clean_manytomany_helptext
* EmailValidator
* force_text
* get_indent
* get_model_name
* get_user_model
* get_username_field
* handler404
* handler500
* HttpResponseBase
* import_module
* import_string
* include
* JsonResponse
* parse_qs
* patterns
* python_2_unicode_compatible
* simplejson
* smart_text
* StringIO
* unquote_plus
* url
* urlencode
* urlparse
* urlunparse
* URLValidator
* user_model_label
* View

# Manual adjustments

## ``url`` template tag 

The  ``url`` template tag works different in Django 1.4, see the [release notes](https://docs.djangoproject.com/en/1.4/releases/1.3/#changes-to-url-and-ssi) for more info. 

### Old, Django 1.4

	{% url url_name %} 
	{% url url_name argument1 argument2 %}
	
### New, Django 1.4 + using forwards compatibility.
	
	{% load url from future %}
	... 
	{% url 'url_name' %} 
	{% url 'url_name' argument1 argument2 %}
	
The following ``sed`` command can be used to update your templates. Note that the ``{% load url from future %}`` is missing and must be added manually.
	
	sed -i -r "s#\{% url ([a-zA-Z0-9_.:-]+)#\{% url '\1'#g" template.html


The inplace editing works great on Linux. If your are working on a Mac and you get the following error 
    
    	"\1 not defined in the RE"

try the following command:

	TMP_FILE=`mktemp /tmp/sed.XXXXXXXXXX`
	sed -E "s#\{% url ([a-zA-Z0-9_.:-]+)#\{% url '\1'#g" template.html > $TMP_FILE
	mv $TMP_FILE template.html

Source: [stackoverflow, Migrate url tags to Django 1.5](http://stackoverflow.com/a/13592772/485361)


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
- [ ] https://github.com/kennethreitz/requests/blob/master/requests/compat.py
- [ ] https://github.com/mitsuhiko/jinja2/blob/master/jinja2/_compat.py
 


 
