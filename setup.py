# -*- encoding: utf-8 -*-
import os, sys
from setuptools import setup
from setuptools import find_packages

# Make the open function accept encodings in python < 3.x
if sys.version_info[0] < 3:
    import codecs
    open = codecs.open  # pylint: disable=redefined-builtin

# Utility function to read the README file.
# Used for the long_description.  It's nice, because now 1) we have a top level
# README file and 2) it's easier to type in the README file than to put a raw
# string in below ...


def get_path(fname):
    return os.path.join(os.path.dirname(os.path.abspath(__file__)), fname)


def read(fname):
    return open(get_path(fname), 'r', encoding='utf8').read()

if sys.argv[-1] == 'genreadme':
    try:
        import pypandoc
        long_description = pypandoc.convert(get_path('README.md'), 'rst')
        long_description = long_description.split('<!---Illegal PyPi RST data -->')[0]
        f = open(get_path('README.rst'), 'w')
        f.write(long_description)
        f.close()
        print("Successfully converted README.md to README.rst")
    except (IOError, ImportError):
        pass
    sys.exit()

try:
    long_description=read('README.rst')
except (OSError, IOError):
    try:
        long_description=read('README.md')
    except (OSError, IOError):
        long_description = ""
    
    
install_requires = [
    'django>=1.4,<1.10',
    'six>=1.10.0',
]

setup(
    name="django-compat",
    version="1.0.10",
    author='arteria GmbH',
    author_email="admin@arteria.ch",
    packages=find_packages(),
    include_package_data=True,
    description="For- and backwards compatibility layer for Django 1.4, 1.7, 1.8, and 1.9",
    long_description=long_description,
    license='MIT',
    install_requires=install_requires,
    url="https://github.com/arteria/django-compat",
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Framework :: Django',
        'License :: OSI Approved :: MIT License',
        'Framework :: Django',
        'Framework :: Django :: 1.4',
        'Framework :: Django :: 1.6',
        'Framework :: Django :: 1.7',
        'Framework :: Django :: 1.8',
        'Framework :: Django :: 1.9',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 3',
    ],
)
