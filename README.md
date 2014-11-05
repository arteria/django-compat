django-compat
=============

For- and backwards compatibility layer for Django 1.4.+ to 1.7 .

Consider [django-compat](https://github.com/arteria/django-compat) as an experiment based on the discussion [on reddit](http://redd.it/2jrr4l). 
Let's see where it goes. 

# Compatible objects

* BytesIO
* clean_manytomany_helptext
* EmailValidator
* force_text
* get_model_name
* get_user_model
* get_username_field
* handler404
* handler500
* HttpResponseBase
* import_string
* include
* JsonResponse
* parse_qs
* patterns
* python_2_unicode_compatible
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



# Resources and references 

## Resources 
* https://github.com/ubernostrum/django-compat-lint
* https://docs.djangoproject.com/en/dev/misc/api-stability/
 
## compat.py

Bits and bites of the following projects are re-used to build [django-compat](https://github.com/arteria/django-compat).

- [x] https://github.com/lukaszb/django-guardian/blob/devel/guardian/compat.py
- [X] https://github.com/evonove/django-oauth-toolkit/blob/master/oauth2_provider/compat.py
- [X] https://github.com/toastdriven/django-tastypie/blob/master/tastypie/compat.py
- [X] https://github.com/tomchristie/django-rest-framework/blob/master/rest_framework/compat.py
	- [ ] TODO: MinValueValidator, MaxValueValidator et al. (other relevant bits are included) Django 1.8
- [ ] https://github.com/kennethreitz/requests/blob/master/requests/compat.py
- [ ] https://github.com/mitsuhiko/jinja2/blob/master/jinja2/_compat.py
 


 
