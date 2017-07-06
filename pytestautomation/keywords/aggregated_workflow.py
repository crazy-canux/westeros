#!/usr/bin/env python
# -*- coding: utf-8 -*-

from pytestautomation.utils.listener import Listener

class AggregatedWorkflow(object):
    ROBOT_LIBRARY_SCOPE = 'GLOBAL'
    ROBOT_LIBRARY_VERSION = '0.0.1'

    def __init__(self):
        self.ROBOT_LIBRARY_LISTENER = Listener()

    def my_keyword(self):
        print 'first test.'
