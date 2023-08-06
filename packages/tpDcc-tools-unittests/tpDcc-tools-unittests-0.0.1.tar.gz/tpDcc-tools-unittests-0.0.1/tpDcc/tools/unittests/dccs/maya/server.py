#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Module that contains tpDcc-tools-renameserver server implementation
"""

from __future__ import print_function, division, absolute_import

from tpDcc.core import server


class UnitTestServer(server.DccServer, object):

    PORT = 17943

    def _process_command(self, command_name, data_dict, reply_dict):
        super(UnitTestServer, self)._process_command(command_name, data_dict, reply_dict)
