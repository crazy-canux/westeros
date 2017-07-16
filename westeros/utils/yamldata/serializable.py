#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
SUMMARY serializable.py

Copyright (C) 2017 Canux CHENG.
All rights reserved.

LICENSE GNU General Public License v3.0.

:author: Canux CHENG canuxcheng@gmail.com
:version: V1.0.0
:since: 07 12 2017 10:41:59

DESCRIPTION:
"""
import copy
import os

import yaml


def serializable(cls):

    class SerializableCls(yaml.YAMLObject, cls):
        yaml_tag = '!{tag}'.format(tag=cls.__name__)

        def __init__(self, *args, **kwargs):
            # yaml.YAMLObject.__init__(self)
            # cls.__init__(self, *args, **kwargs)
            super(SerializableCls, self).__init__(*args, **kwargs)

        def dump(self, path):
            try:
                data = copy.deepcopy(self)
                for key, value in vars(self).iteritems():
                    if hasattr(value, '__dict__') and (
                            not isinstance(value, yaml.YAMLObject)
                    ):
                        delattr(data, key)

                with open(path, 'w') as stream:
                    yaml.dump(data, stream)
            except IOError as e:
                raise e
            except yaml.YAMLError as e:
                raise e
            except Exception as e:
                raise RuntimeError(e.message)

        @staticmethod
        def load(path):
            if not os.path.isfile(path):
                raise IOError('Invalid file path.')
            try:
                with open(path, 'r') as stream:
                    model = yaml.load(stream)
            except IOError as e:
                model = e.message
            except yaml.YAMLError:
                model = yaml.YAMLObject
            except Exception as e:
                raise e
            return model

    return type(
        cls.__name__,
        (SerializableCls,),
        dict(SerializableCls.__dict__)
    )
