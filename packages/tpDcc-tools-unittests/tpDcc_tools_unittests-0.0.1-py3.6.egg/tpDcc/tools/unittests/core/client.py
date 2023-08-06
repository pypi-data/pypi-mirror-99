#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Module that contains tpDcc-tools-unittest client implementation
"""

from __future__ import print_function, division, absolute_import

from tpDcc.core import client


class UnitTestClient(client.DccClient, object):

    PORT = 17943
