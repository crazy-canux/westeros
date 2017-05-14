#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Setup file used for install this package.

Copyright (C) 2016 Canux CHENG.
All rights reserved.
Name: setup.py
Author: Canux CHENG canuxcheng@gmail.com
Version: V1.0.0.0
Time: Fri 05 Aug 2016 09:59:29 AM CST

Description:
    ./setup.py -h
"""
import os

from setuptools import setup, find_packages

import pytestautomation

NAME = 'pytestautomation'
VERSION = pytestautomation.__version__
URL = 'https://github.com/crazy-canux/pytestautomation'
DESCRIPTION = 'Common interface of tons protocals, used for monitoring tools, like nagios/icinga...'
KEYWORDS = 'monitoring nagios icinga plugins'


def read(readme):
    """Give reST format README for pypi."""
    extend = os.path.splitext(readme)[1]
    if (extend == '.rst'):
        import codecs
        return codecs.open(readme, 'r', 'utf-8').read()
    elif (extend == '.md'):
        import pypandoc
        return pypandoc.convert(readme, 'rst')

INSTALL_REQUIRES = []

setup(
    name=NAME,
    version=VERSION,
    url=URL,
    description=DESCRIPTION,
    keywords=KEYWORDS,
    author='Canux CHENG',
    author_email='canuxcheng@gmail.com',
    maintainer='Canux CHENG',
    maintainer_email='canuxcheng@gmail.com',
    long_description=read('README.rst'),
    license='GPL',
    platforms='any',
    install_requires=INSTALL_REQUIRES,
    packages=find_packages(),
    zip_safe=False,
    include_package_data=True,
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Environment :: Plugins",
        "Intended Audience :: Developers",
        "Natural Language :: English",
        "License :: OSI Approved :: GNU General Public License (GPL)",
        "Operating System :: POSIX",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2.7",
        "Topic :: System :: Monitoring"
    ],
)
