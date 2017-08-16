#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
SUMMARY requestswrapper.py

Copyright (C) 2017 Canux CHENG.
All rights reserved.

LICENSE GNU General Public License v3.0.

:author: Canux CHENG canuxcheng@gmail.com
:version: V1.0.0
:since: 08 15 2017 15:54:42

DESCRIPTION:
"""
import json
from urlparse import urljoin

from requests.auth import HTTPBasicAuth
from requests.packages import urllib3
from requests.sessions import Session

from westeros.utils.yamldata.datamodel import DataModel


class RestWrapper(Session):
    def __init__(self, base_url, username, password, hostname=None, domain=None):
        if (not username) or (not isinstance(username, str)):
            raise ValueError('Non-deterministic credential: username')

        if (not password) or (not isinstance(password, str)):
            raise ValueError('Non-deterministic credential: password')

        self.username = username
        self.password = password
        self.base_url = base_url
        self.hostname = hostname
        self.domain = domain

        self.verify = False
        self.auth = HTTPBasicAuth(self.username, self.password)
        urllib3.disable_warnings()

    def get(self, path, **kwargs):
        url = urljoin(self.base_url, path)
        kwargs.setdefault('timeout', 60)
        kwargs.setdefault('allow_redirects', True)
        return self.request('GET', url, **kwargs)

    def post(self, path, data=None, json=None, **kwargs):
        url = urljoin(self.base_url, path)
        kwargs.setdefault('timeout', 60)
        return self.request('POST', url, data=data, json=json, **kwargs)

    def put(self, path, data=None, **kwargs):
        url = urljoin(self.base_url, path)
        kwargs.setdefault('timeout', 60)
        return self.request('PUT', url, data=data, **kwargs)

    def delete(self, path, **kwargs):
        url = urljoin(self.base_url, path)
        return self.request(url, **kwargs)

    @staticmethod
    def decode(json_string):
        _model = {}
        try:
            _model = DataModel(**json.loads(json_string))
        except Exception:
            pass
        return _model

    @staticmethod
    def encode(model):
        def _unicode_encoder(data):
            _json = {}
            for key, value in data.__dict__.iteritems():
                if isinstance(value, list):
                    value = [
                        _unicode_encoder(item)
                        for item in value
                        if isinstance(item, DataModel)
                    ] + [
                        item
                        for item in value
                        if not isinstance(item, DataModel)
                    ]

                if isinstance(value, DataModel):
                    value = _unicode_encoder(value)

                _json[key] = value

            return _json

        if not isinstance(model, DataModel):
            return json.dumps(model)

        return json.dumps(
            _unicode_encoder(model), indent=2, sort_keys=True
        )

