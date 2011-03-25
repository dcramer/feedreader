#!/usr/bin/env python

from setuptools import setup, find_packages

import feedreader

setup(
    name='feedreader',
    version='0.3.1',
    author='David Cramer',
    author_email='dcramer@gmail.com',
    url='https://github.com/dcramer/feedreader',
    install_requires=[
        'lxml',
        'python-dateutil',
    ],
    description = 'A generic RSS/Atom feedparser.',
    packages=find_packages(),
    include_package_data=True,
    tests_require=['unittest2'],
    test_suite='unittest2.collector',
)
