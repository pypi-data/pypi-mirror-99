#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""
Unit Test widget controller class implementation
"""

from __future__ import print_function, division, absolute_import

import unittest

from tpDcc.libs.python import python

from tpDcc.libs.unittests.core import unittestlib


class UnitTestController(object):
    def __init__(self, client, model):

        self._client = client
        self._model = model

    @property
    def client(self):
        return self._client

    @property
    def model(self):
        return self._model

    def set_unit_test_paths(self, value):
        self._model.unit_test_paths = value

    def set_tree_model(self, model):
        self._model.tree_model = model

    def uninstall_rollback_importer(self):
        self._model.rollback_importer.uninstall()

    def reset_rollback_importer(self):
        if self._model.rollback_importer:
            self._model.rollback_importer.uninstall()
        self._model.rollback_importer = python.RollbackImporter()

    def get_tests(self):
        return unittestlib.get_tests(self._model.unit_test_paths)

    def run_all_tests(self):
        self.reset_rollback_importer()
        test_suite = unittest.TestSuite()
        unittestlib.get_tests(directories=self._model.unit_test_paths, test_suite=test_suite)
        self._model.test_suite_to_run = test_suite

    def run_selected_tests(self):
        print('Running selected tests ...')

    def run_failed_tests(self):
        print('Running failed tests ...')
