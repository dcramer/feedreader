#!/usr/bin/env python

from setuptools import setup, find_packages

import feedreader

setup(
    name='feedreader',
    version=".".join(map(str, feedreader.__version__)),
    author='David Cramer',
    author_email='dcramer@gmail.com',
    url='http://github.com/dcramer/feedreader',
    install_requires=[
        'lxml',
        'python-dateutil',
    ],
    description = 'A generic RSS/Atom feedparser.',
    packages=find_packages(),
    include_package_data=True,
)
