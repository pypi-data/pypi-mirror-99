#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""
Unit Test widget model class implementation
"""

from __future__ import print_function, division, absolute_import

from Qt.QtCore import Signal, QObject

from tpDcc.libs.python import python


class UnitTestModel(QObject, object):

    treeModelChanged = Signal(object)
    rollbackImporterChanged = Signal(object)
    pathsListChanged = Signal(list)
    testSuiteToRunChanged = Signal(object)

    def __init__(self):
        super(UnitTestModel, self).__init__()

        self._unit_test_paths = list()
        self._rollback_importer = python.RollbackImporter()
        self._tree_model = None
        self._test_suite_to_run = None

    @property
    def unit_test_paths(self):
        return self._unit_test_paths

    @unit_test_paths.setter
    def unit_test_paths(self, paths_list):
        self._unit_test_paths = python.force_list(paths_list)
        self.pathsListChanged.emit(self._unit_test_paths)

    @property
    def rollback_importer(self):
        return self._rollback_importer

    @rollback_importer.setter
    def rollback_importer(self, value):
        self._rollback_importer = value
        self.rollbackImporterChanged.emit(self._rollback_importer)

    @property
    def tree_model(self):
        return self._tree_model

    @tree_model.setter
    def tree_model(self, value):
        self._tree_model = value
        self.treeModelChanged.emit(self._tree_model)

    @property
    def test_suite_to_run(self):
        return self._test_suite_to_run

    @test_suite_to_run.setter
    def test_suite_to_run(self, value):
        self._test_suite_to_run = value
        self.testSuiteToRunChanged.emit(self._test_suite_to_run)
