# -*- encoding: utf-8 -*-

from setuptools import setup
from setuptools import find_packages

setup(
    name="django-compat",
    version="0.0.1",
    author_email="admin@arteria.ch",
    packages=find_packages(),
    include_package_data=True,
    description="For- and backwards compatibility layer for Django 1.4 to 1.7",
)
