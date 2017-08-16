#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
SUMMARY workflowcontext.py

Copyright (C) 2017 Canux CHENG.
All rights reserved.

LICENSE GNU General Public License v3.0.

:author: Canux CHENG canuxcheng@gmail.com
:version: V1.0.0
:since: 08 14 2017 14:53:04

DESCRIPTION:
"""
from datamodel import DataModel
from datacontext import DataContext


class WorkflowContext(DataContext):
    def __init__(
            self,
            global_conf_file=None,
            *workflow_conf_files
    ):
        self.global_tag = 'global'
        self.local_tag = 'local'
        self.shared_tag = 'shared'

        super(WorkflowContext, self).__init__(
            global_conf_file, self.global_tag
        )

        self[self.local_tag] = {}

        if vars(self[self.global_tag]):
            self[self.local_tag] += self[self.global_tag]

        for workflow_conf_file in workflow_conf_files:
            self.update_node_from_file(
                workflow_conf_file, self.local_tag
            )

    @property
    def globals(self):
        return self[self.global_tag]

    @property
    def locals(self):
        return self[self.local_tag]

    @property
    def shared(self):
        return getattr(self[self.local_tag], self.shared_tag, None)

    @shared.setter
    def shared(self, value):
        raise AssertionError('Unreachable setter')

    def __getattr__(self, item):
        if item:
            _val_attribute = getattr(self.locals, item, None) \
                             or getattr(self.shared, item, None)
        else:
            raise AttributeError('Invalid attribute item')
        return _val_attribute or DataModel()


