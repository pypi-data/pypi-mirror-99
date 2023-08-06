#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""
Module that contains constant definitions for tpDcc-tools-unittest
"""

from __future__ import print_function, division, absolute_import

TOOL_ID = 'tpDcc-tools-unittests'


class UnitTestStatus(object):

    NOT_RUN = 0
    SUCCESS = 1
    FAIL = 2
    ERROR = 3
    SKIPPED = 4
