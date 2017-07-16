#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
SUMMARY datamodel.py

Copyright (C) 2017 Canux CHENG.
All rights reserved.

LICENSE GNU General Public License v3.0.

:author: Canux CHENG canuxcheng@gmail.com
:version: V1.0.0
:since: 07 12 2017 16:58:59

DESCRIPTION:
"""
import yaml

from .serializable import serializable


@serializable
class DataModel(object):
    def __init__(self, **kwargs):
        for key, value in kwargs.iteritems():
            self[key] = value

    def __getitem__(self, item):
        if item:
            return self.getattr(self, item, None)
        else:
            raise AttributeError(
                'Invalid attribute item.'
            )

    def __setitem__(self, key, value):
        if hasattr(value, 'iteritems'):
            value = DataModel(**value)
        elif hasattr(value, '__iter__'):
            node = []
            for item in value:
                if hasattr(item, 'iteritems'):
                    child = DataModel(**item)
                elif isinstance(item, yaml.YAMLObject):
                    child = item
                else:
                    try:
                        child = yaml.safe_load(
                            yaml.safe_dump(item)
                        )
                    except yaml.YAMLError as e:
                        child = e.message
                node.append(child)
            value = node
        elif isinstance(value, yaml.YAMLObject):
            pass
        else:
            try:
                value = yaml.safe_load(yaml.safe_dump(value))
            except yaml.YAMLError as e:
                value = e.message
        self.__dict__[key] = value

    def __iadd__(self, other):
        if getattr(other, 'iteritems', None):
            other = DataModel(**other)

        if isinstance(other, type(self)):
            for key, value in vars(other).iteritems():
                if not getattr(self, key, None) or (
                    isinstance(value, basestring) or (
                            value is None)
                ):
                    self.__dict__[key] = value
                else:
                    self.__dict__[key] += value
        else:
            raise ValueError(
                'The argument {} is invalid.'.format(other)
            )
        return self




