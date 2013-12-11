#!/usr/bin/env python
# -*- coding: utf-8 -*-

try:
    from setuptools import setup, find_packages
except:
    from distutils.core import setup, find_packages

setup(
    name = 'rewheel',
    version = '0.0.1',
    description = 'Short description',
    long_description = 'Long description',
    keywords = 'some, keywords',
    author = 'yourname',
    author_email = 'yourmail',
    license = 'MIT',
    packages = find_packages(),
    classifiers = ['Development Status :: 3 - Alpha',
                   'Intended Audience :: Developers',
                   'License :: OSI Approved :: MIT License',
                   'Operating System :: POSIX :: Linux',
                   'Programming Language :: Python',
                  ]
)
