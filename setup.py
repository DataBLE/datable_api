#!/usr/bin/env python
from setuptools import setup, find_packages

setup(
    name='cloud',
    version='1.0',
    description="",
    author="Juan Carlos Ferrer",
    author_email='juan.carlos@micronixsolutions.com',
    url='',
    packages=find_packages(),
    package_data={'cloud': ['static/*.*', 'templates/*.*']},
    scripts=['manage.py'],
)
