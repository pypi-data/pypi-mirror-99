#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""
Modules that contains unit test tree models
"""

from __future__ import print_function, division, absolute_import

import unittest

from Qt.QtCore import Qt, QModelIndex, QAbstractItemModel
from Qt.QtGui import QIcon

from tpDcc.managers import resources
from tpDcc.libs.qt.core import qtutils

from tpDcc.tools.unittests.core import consts
from tpDcc.libs.unittests.core import settings, result


class BaseUnitTestTreeModel(QAbstractItemModel, object):
    """
    The model used to populate the test tree view
    """

    def __init__(self, root, parent=None):
        super(BaseUnitTestTreeModel, self).__init__(parent)

        self.root_node = root

    def rowCount(self, parent):
        """
        Return the number of rows with this parent
        """

        if not parent.isValid():
            parent_node = self.root_node
        else:
            parent_node = parent.internalPointer()
        return parent_node.childCount()

    def columnCount(self, parent):
        return 1

    def data(self, index, role):
        if not index.isValid():
            return None
        node = index.internalPointer()
        if role == Qt.DisplayRole:
            return node.name()
        elif role == Qt.DecorationRole:
            return node.get_icon()
        elif role == Qt.ToolTipRole:
            return node.toolTip

    def setData(self, index, value, role=Qt.EditRole):
        node = index.internalPointer()
        if qtutils.is_pyqt4() or qtutils.is_pyside():
            data_changed_kwargs = [index, index]
        else:
            data_changed_kwargs = [index, index, []]

        if role == Qt.EditRole:
            self.dataChanged.emit(*data_changed_kwargs)
            node.status = value
        if role == Qt.DecorationRole:
            node.status = value
            self.dataChanged.emit(*data_changed_kwargs)
            if node.parent() is not self.root_node:
                self.setData(self.parent(index), value, role)
        elif role == Qt.ToolTipRole:
            node.toolTip = value
            self.dataChanged.emit(*data_changed_kwargs)

    def headerData(self, section, orientation, role):
        return 'TreeModel'

    def flags(self, index):
        return Qt.ItemIsEnabled | Qt.ItemIsSelectable

    def parent(self, index):
        node = index.internalPointer()
        parent_node = node.parent()
        if parent_node == self.root_node:
            return QModelIndex()
        return self.createIndex(parent_node.row(), 0, parent_node)

    def index(self, row, column, parent):
        if not parent.isValid():
            parent_node = self.root_node
        else:
            parent_node = parent.internalPointer()

        child_item = parent_node.child(row)
        if child_item:
            return self.createIndex(row, column, child_item)
        else:
            return QModelIndex()

    def get_index_of_node(self, node):
        if node is self.root_node:
            return QModelIndex()
        return self.index(node.row(), 0, self.get_index_of_node(node.parent()))


class UnitTestTreeModel(BaseUnitTestTreeModel, object):
    """
    The model used to populate the test tree view
    """

    def __init__(self, root, parent=None):
        super(UnitTestTreeModel, self).__init__(root=root, parent=parent)

        self._node_lookup = dict()

        # Create a lookup so we can find the TestNode given a TestCase or TestSuite
        self.create_node_lookup(self.root_node)

    def create_node_lookup(self, node):
        """
        Create a lookup so we can find the TestNode given a TestCase or TestSuite. The lookup will be used
        to set test statuses anad tool tips after a test run
        :param node: Node to add to the map
        """

        self._node_lookup[str(node.test)] = node
        for child in node.children:
            self.create_node_lookup(child)

    def run_tests(self, stream, testSuite):
        """
        Runs the given TestSuite
        :param stream: A stream object with write functionality to capture the test output
        :param testSuite: The TestSuite to run
        """

        runner = unittest.TextTestRunner(stream=stream, verbosity=2, resultclass=result.UnitTestResult(as_class=True))
        runner.failfast = False
        try:
            runner.buffer = settings.UnitTestSettings().buffer_output
        except Exception:
            pass
        test_result = runner.run(testSuite)

        self._set_test_result_data(test_result.failures, consts.UnitTestStatus.FAIL)
        self._set_test_result_data(test_result.errors, consts.UnitTestStatus.ERROR)
        self._set_test_result_data(test_result.skipped, consts.UnitTestStatus.SKIPPED)

        for test in test_result.successes:
            node = self._node_lookup[str(test)]
            index = self.get_index_of_node(node)
            self.setData(index, 'Test Passed', Qt.ToolTipRole)
            self.setData(index, consts.UnitTestStatus.SUCCESS, Qt.DecorationRole)

    def _set_test_result_data(self, testList, status):
        """
        Store the test result data in model
        :param testList: A list of tuples of test results
        :param status: A tpTestStatus value
        """

        for test, reason in testList:
            node = self._node_lookup[str(test)]
            index = self.get_index_of_node(node)
            self.setData(index, reason, Qt.ToolTipRole)
            self.setData(index, status, Qt.DecorationRole)

    def data(self, index, role):
        if not index.isValid():
            return None
        node = index.internalPointer()
        if role == Qt.DisplayRole:
            return node.name()
        elif role == Qt.DecorationRole:
            return node.get_icon()
        elif role == Qt.ToolTipRole:
            return node.toolTip

    def headerData(self, section, orientation, role):
        return 'Tests'

    def parent(self, index):
        node = index.internalPointer()
        parent_node = node.parent()
        if parent_node == self.root_node:
            return QModelIndex()
        return self.createIndex(parent_node.row(), 0, parent_node)

    def index(self, row, column, parent):
        if not parent.isValid():
            parent_node = self.root_node
        else:
            parent_node = parent.internalPointer()

        child_item = parent_node.child(row)
        if child_item:
            return self.createIndex(row, column, child_item)
        else:
            return QModelIndex()

    def get_index_of_node(self, node):
        if node is self.root_node:
            return QModelIndex()
        return self.index(node.row(), 0, self.get_index_of_node(node.parent()))


class BaseUnitTestTreeNodeModel(object):

    def __init__(self, parent=None):
        self.children = list()
        self._parent = parent

        if parent is not None:
            parent.add_child(self)

    def add_child(self, child):
        """
        Add a child to the node
        :param int child: Child node to add
        """

        if child not in self.children:
            self.children.append(child)

    def remove(self):
        """
        Remove this node and all its children from the tree
        """

        if self._parent:
            row = self.getRow()
            self._parent.children.pop(row)
            self._parent = None
        for child in self.children:
            child.remove()

    def child(self, row):
        """
        Get the child at the specified index
        :param int row: The child index
        :return: The tree node at the given index or None if the index was out of bounds
        """

        try:
            return self.children[row]
        except IndexError:
            return None

    def childCount(self):
        """
        Get the number of children in the node
        """

        return len(self.children)

    def parent(self):
        """
        Get the parent of node
        """

        return self._parent

    def row(self):
        """
        Get the index of the node relative to the parent
        """

        if self._parent is not None:
            return self._parent.children.index(self)
        return 0

    def data(self, column):
        """
        Get the table display data
        """

        return ''


class UnitTestTreeNodeModel(BaseUnitTestTreeNodeModel, object):

    """
    A node representing a Test, TestCase or TestSuite for display in a QTreeView
    """

    def __init__(self, test, parent=None):
        super(UnitTestTreeNodeModel, self).__init__(parent=parent)
        self.test = test
        self.tool_tip = str(test)
        self.status = consts.UnitTestStatus.NOT_RUN

        if isinstance(self.test, unittest.TestSuite):
            for test_ in self.test:
                if isinstance(test_, unittest.TestCase) or test_.countTestCases():
                    self.add_child(UnitTestTreeNodeModel(test_, self))

    @staticmethod
    def success_icon():
        return QIcon(resources.icon(name='ok'))

    @staticmethod
    def fail_icon():
        return QIcon(resources.icon(name='cancel'))

    @staticmethod
    def error_icon():
        return QIcon(resources.icon(name='high_priority'))

    @staticmethod
    def skip_icon():
        return QIcon(resources.icon(name='warning'))

    def base_icon(self):
        return QIcon(resources.icon(name='python'))
        # if (isinstance(self.test, lib.MayaTestCase) or 'Maya' in self.name()):
        #     return resourcemanager.ResourceManager.icon(name='maya', theme='color', extension='png')
        # else:
        #     return resourcemanager.ResourceManager.icon(name='python', theme='color', extension='png')

    def name(self):

        """
        Get the name to print in the view
        """

        if isinstance(self.test, unittest.TestCase):
            return self.test._testMethodName
        elif isinstance(self.child(0).test, unittest.TestCase):
            return self.child(0).test.__class__.__name__
        else:
            return self.child(0).child(0).test.__class__.__module__

    def path(self):
        """
        Gets the import path of the test. Used for finding the test by name
        """

        if self.parent() and self.parent().parent():
            return '{0}.{1}'.format(self.parent().path(), self.name())
        else:
            return self.name()

    def get_status(self):
        """
        Get the status of the tpTestNode
        Nodes with children like the TestSuites, will get their status based on the
        status of the leaf nodes (the TestCases)
        @return: A status value from TestStatus
        """

        if not self.children:
            return self.status
        status = consts.UnitTestStatus.NOT_RUN
        for child in self.children:
            child_status = child.get_status()
            if child_status == consts.UnitTestStatus.ERROR:
                # Error status has highest priority so propagate that up to the parent
                return child_status
            elif child_status == consts.UnitTestStatus.FAIL:
                status = child_status
            elif child_status == consts.UnitTestStatus.SUCCESS and status != consts.UnitTestStatus.FAIL:
                status = child_status
            elif child_status == consts.UnitTestStatus.SKIPPED and status != consts.UnitTestStatus.FAIL:
                status = child_status

        return status

    def get_icon(self):
        """
        Get the status icon to display with the Test
        """

        status = self.get_status()
        icon = [self.base_icon(), self.success_icon(), self.fail_icon(), self.error_icon(), self.skip_icon()][status]

        # Our resource manager returns a Icon instance. For some reason, tree views does not like it, we must convert
        # it to icon before returning it
        return icon
