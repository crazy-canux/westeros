#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Setup file used for install this package.

Copyright (C) 2017 Canux CHENG.
All rights reserved.
Name: setup.py
Author: Canux CHENG canuxcheng@gmail.com
Version: V0.0.1
Time: Fri 05 Aug 2016 09:59:29 AM CST

Description:
    ./setup.py -h
"""
import os

from setuptools import setup, find_packages
from setuptools.command.install import install

import westeros

NAME = 'westeros'
VERSION = westeros.__version__
URL = 'https://github.com/crazy-canux/westeros'
DESCRIPTION = 'Test automation framework based on robot framework.'
KEYWORDS = 'test automation robot framework'


def read(readme):
    """Give reST format README for pypi."""
    extend = os.path.splitext(readme)[1]
    if (extend == '.rst'):
        import codecs
        return codecs.open(readme, 'r', 'utf-8').read()
    elif (extend == '.md'):
        import pypandoc
        return pypandoc.convert(readme, 'rst')


class InstInstall(install):
    def run(self):
        print "PreInst for westeros."
        # TODO
        install.run(self)
        print "PostInst for westeros."
        # TODO


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
    scripts=['bin/westeros'],
    data_files=[
        ('/etc/westeros/conf', [
            'etc/global.yaml',
            'etc/shared.yaml'
        ]),
        ('/etc/westeros/robot', [
            'examples/westeros.robot'
        ]),
        ('/etc/westeros/data', [
            'data/westeros.data'
        ])
    ],
    cmdclass={
        "install": InstInstall
    },
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Environment :: Other Environment",
        "Framework :: Robot Framework",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: GNU General Public License (GPL)",
        "Natural Language :: English",
        "Operating System :: POSIX",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2.7",
        "Topic :: Software Development :: Quality Assurance",
    ],
)
