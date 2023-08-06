#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Toolset implementation for tpDcc-tools-unittests
"""

from __future__ import print_function, division, absolute_import

from tpDcc.libs.qt.widgets import toolset


class UnitTestsToolsetWidget(toolset.ToolsetWidget, object):
    def __init__(self, *args, **kwargs):

        self._unit_test_paths = kwargs.get('unit_test_paths', list())
        self._unit_test_paths.extend([r'D:\tpDcc\tpDcc-libs-nameit\tests'])

        super(UnitTestsToolsetWidget, self).__init__(*args, **kwargs)

    def contents(self):

        from tpDcc.tools.unittests.core import model, view, controller

        unit_test_model = model.UnitTestModel()
        unit_test_controller = controller.UnitTestController(client=self._client, model=unit_test_model)
        unit_test_view = view.UnitTestView(
            unit_test_paths=self._unit_test_paths, model=unit_test_model, controller=unit_test_controller, parent=self)

        return [unit_test_view]
