#!/usr/bin/env python3
# -*- coding: utf-8 -*-

try:
    from setuptools import setup, find_packages
except:
    from distutils.core import setup, find_packages

setup(
    name = 'rewheel',
    version = '0.1.0',
    description = 'Recreate Wheel files from installed packages',
    long_description = 'Recreate Wheel files from installed packages',
    keywords = 'wheel',
    author = 'Slavek Kabrda',
    author_email = 'bkabrda@redhat.com',
    license = 'MIT',
    packages = find_packages(),
    entry_points = {'console_scripts': ['rewheel=rewheel:run']},
    classifiers = ['Development Status :: 3 - Alpha',
                   'Intended Audience :: Developers',
                   'License :: OSI Approved :: MIT License',
                   'Operating System :: POSIX :: Linux',
                   'Programming Language :: Python',
                  ]
)
