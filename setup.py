# -*- encoding: utf-8 -*-
import os
from setuptools import setup
from setuptools import find_packages

# Utility function to read the README file.
# Used for the long_description.  It's nice, because now 1) we have a top level
# README file and 2) it's easier to type in the README file than to put a raw
# string in below ...


def get_path(fname):
    return os.path.join(os.path.dirname(os.path.abspath(__file__)), fname)


def read(fname):
    return open(get_path(fname)).read()


try:
    import pypandoc
    long_description = pypandoc.convert(get_path('README.md'), 'rst')
    long_description = long_description.split('<!---Illegal PyPi RST data -->')[0]
    f = open(get_path('README.rst'), 'w')
    f.write(long_description)
    f.close()
    print("Successfully converted README.md to README.rst")
except (IOError, ImportError):
    # No long description... but nevermind, it's only for PyPi uploads.
    long_description = ""
    
    
install_requires = [
    'django>=1.4,<1.9',
    'six',
]

setup(
    name="django-compat",
    version="1.0.6",
    author_email="admin@arteria.ch",
    packages=find_packages(),
    include_package_data=True,
    description="For- and backwards compatibility layer for Django 1.4, 1.7 and 1.8",
    long_description=long_description,
    license='MIT',
    install_requires=install_requires,
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Framework :: Django',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 3',
    ],
)
