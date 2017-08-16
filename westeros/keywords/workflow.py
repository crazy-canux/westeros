#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
SUMMARY workflow.py

Copyright (C) 2017 Canux CHENG.
All rights reserved.

LICENSE GNU General Public License v3.0.

:author: Canux CHENG canuxcheng@gmail.com
:version: V1.0.0
:since: 08 14 2017 15:58:22

DESCRIPTION:
"""
import os
import tempfile

from westeros import __version__
from westeros.utils.listener import Listener
from westeros.utils.yamldata.workflowcontext import WorkflowContext


class Workflow(object):
    ROBOT_LIBRARY_SCOPE = 'GLOBAL'
    ROBOT_LIBRARY_VERSION = __version__
    ROBOT_LIBRARY_DOC_FORMAT = 'ROBOT'

    def __init__(
            self,
            generic_conf_file=None,
            *specific_conf_files
    ):
        self.ROBOT_LIBRARY_LISTENER = Listener()

        self.ctx = self.load_configurations(
            generic_conf_file,
            *specific_conf_files
        )

        self.ctx_store_directory = os.path.join(
            tempfile.gettempdir(), '.4robot'
        )

        if not os.path.exists(self.ctx_store_directory):
            os.mkdir(self.ctx_store_directory)

    def load_configurations(
            self,
            global_conf_file=None,
            *workflow_conf_files,
            **kwargs
    ):
        self.ctx = WorkflowContext(
            global_conf_file,
            *workflow_conf_files
        )

        self.ctx[self.ctx.local_tag] += kwargs
        return self.ctx

    def clean_up_environment(self):
        pass

    def tear_down(self):
        pass

    def user_open_browser(self):
        pass

    def user_close_browser(self):
        pass
