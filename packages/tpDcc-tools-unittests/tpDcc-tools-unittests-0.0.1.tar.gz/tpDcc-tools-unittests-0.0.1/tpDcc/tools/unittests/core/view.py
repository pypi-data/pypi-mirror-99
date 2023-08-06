#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""
Unit Test widget view class implementation
"""

from __future__ import print_function, division, absolute_import

from Qt.QtCore import Qt
from Qt.QtWidgets import QSizePolicy, QMenuBar, QToolBar, QAction, QSplitter, QAbstractItemView

from tpDcc import dcc
from tpDcc.managers import resources
from tpDcc.libs.qt.core import base
from tpDcc.libs.qt.widgets import dividers, views

from tpDcc.libs.unittests.core import settings
from tpDcc.tools.unittests.widgets import console, tree


class UnitTestView(base.BaseWidget, object):
    def __init__(self, model, controller, unit_test_paths=None, parent=None):

        self._model = model
        self._controller = controller

        super(UnitTestView, self).__init__(parent=parent)

        self._controller.set_unit_test_paths(unit_test_paths)
        test_suite = self._controller.get_tests()
        root_node = tree.UnitTestTreeNodeModel(test_suite)
        self._controller.set_tree_model(tree.UnitTestTreeModel(root_node, self))
        self._tree_view.expand_tree(root_node)

    @property
    def model(self):
        return self._model

    @property
    def controller(self):
        return self._controller

    def ui(self):
        super(UnitTestView, self).ui()

        self._menu_bar = self._setup_menubar()
        self._tool_bar = self._setup_toolbar()

        splitter = QSplitter(Qt.Horizontal, parent=self)
        splitter.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self._tree_view = views.BaseTreeView(parent=self)
        self._tree_view.setSelectionMode(QAbstractItemView.ExtendedSelection)
        self._console = console.Console(parent=self)
        splitter.addWidget(self._tree_view)
        splitter.addWidget(self._console)
        splitter.setStretchFactor(1, 4)

        self.main_layout.addWidget(self._menu_bar)
        self.main_layout.addWidget(self._tool_bar)
        self.main_layout.addWidget(dividers.Divider())
        self.main_layout.addWidget(splitter)

        self.refresh()

    def setup_signals(self):
        self._model.treeModelChanged.connect(self._tree_view.setModel)
        self._model.testSuiteToRunChanged.connect(self._on_run_test_suite)

    def closeEvent(self, event):
        pass

    def refresh(self):
        pass

    def _setup_menubar(self):
        menubar = QMenuBar(parent=self)
        settings_menu = menubar.addMenu('Settings')

        if dcc.is_maya():
            action = settings_menu.addAction('Buffer Output')
            action.setToolTip('Only display output during a failed test.')
            action.setCheckable(True)
            action.setChecked(settings.UnitTestSettings().buffer_output)
            action.toggled.connect(settings.UnitTestSettings().set_buffer_output)

            action = settings_menu.addAction('New Scene Between Test')
            action.setToolTip('Creates a new scene file after each test')
            action.setCheckable(True)
            action.setChecked(settings.UnitTestSettings().file_new)
            action.toggled.connect(settings.UnitTestSettings().set_file_new)

        return menubar

    def _setup_toolbar(self):
        toolbar = QToolBar(parent=self)
        toolbar.setContextMenuPolicy(Qt.PreventContextMenu)

        run_all_tests_action = QAction('Run All Tests', parent=self)
        run_all_tests_action.setIcon(resources.icon('play'))
        run_all_tests_action.triggered.connect(self._controller.run_all_tests)
        run_all_tests_action.setToolTip('Run all tests')

        run_selected_tests_action = QAction('Run Selected Tests', self)
        run_selected_tests_action.setIcon(resources.icon('play_selected'))
        run_selected_tests_action.triggered.connect(self._controller.run_selected_tests)
        run_selected_tests_action.setToolTip('Run selected tests')

        run_failed_tests_action = QAction('Run Failed Tests', self)
        run_failed_tests_action.setIcon(resources.icon('play_error'))
        run_failed_tests_action.triggered.connect(self._controller.run_failed_tests)
        run_failed_tests_action.setToolTip('Run all failed tests')

        for action in [run_all_tests_action, run_selected_tests_action, run_failed_tests_action]:
            toolbar.addAction(action)

        return toolbar

    def _on_run_test_suite(self, test_suite):
        self._console.flush()
        self._tree_view.model().run_tests(self._console, test_suite)
