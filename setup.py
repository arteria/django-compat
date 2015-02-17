# -*- encoding: utf-8 -*-

from setuptools import setup
from setuptools import find_packages

install_requires = [
    'django>=1.4,<1.9',
    'six',
]

setup(
    name="django-compat",
    version="1.0.0",
    author_email="admin@arteria.ch",
    packages=find_packages(),
    include_package_data=True,
    description="For- and backwards compatibility layer for Django 1.4 to 1.8",
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
