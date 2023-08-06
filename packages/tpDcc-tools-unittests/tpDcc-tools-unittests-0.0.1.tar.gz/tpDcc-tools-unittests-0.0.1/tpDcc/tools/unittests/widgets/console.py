#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""
Modules that contains unit test console implementation
"""

from __future__ import print_function, division, absolute_import

from Qt.QtCore import Signal, QObject
from Qt.QtWidgets import QTextEdit
from Qt.QtGui import QColor

from tpDcc.libs.python import python


class Console(QTextEdit, object):

    SUCCESS_COLOR = (92, 184, 92)
    FAIL_COLOR = (240, 173, 78)
    ERROR_COLOR = (217, 83, 79)
    SKIP_COLOR = (88, 165, 204)
    NORMAL_COLOR = (200, 200, 200)

    def __init__(self, parent=None):
        super(Console, self).__init__(parent=parent)

        self._model = ConsoleModel()
        self._controller = ConsoleController(model=self._model)

        self.setReadOnly(True)

        self._setup_signals()

        self.refresh()

    def write(self, text):
        if text.startswith('ok'):
            self._controller.set_text_color(self.SUCCESS_COLOR)
        elif text.startswith('FAIL'):
            self._controller.set_text_color(self.FAIL_COLOR)
        elif text.startswith('ERROR'):
            self._controller.set_text_color(self.ERROR_COLOR)
        elif text.startswith('skipped'):
            self._controller.set_text_color(self.SKIP_COLOR)
        self._controller.insert_text(text)
        self._controller.set_text_color(self.NORMAL_COLOR)

    def flush(self):
        self._controller.clear()

    def refresh(self):
        self._controller.set_text(self._model.text)
        self._controller.set_text_color(self._model.text_color)

    def _setup_signals(self):
        self._model.textChanged.connect(self.setPlainText)
        self._model.textInserted.connect(self.insertPlainText)
        self._model.textColorChanged.connect(self._on_text_color_changed)

        self.textChanged.connect(self._on_text_changed)

    def _on_text_changed(self):
        current_text = self.toPlainText()
        self.blockSignals(True)
        try:
            self._controller.set_text(current_text)
        finally:
            self.blockSignals(False)

    def _on_text_color_changed(self, color_tuple):
        self.setTextColor(QColor(*color_tuple))


class ConsoleModel(QObject):

    textChanged = Signal(str)
    textInserted = Signal(str)
    textColorChanged = Signal(tuple)

    def __init__(self):
        super(ConsoleModel, self).__init__()

        self._text = ''
        self._text_color = Console.SUCCESS_COLOR

    @property
    def text(self):
        return self._text

    @text.setter
    def text(self, value):
        self._text = str(value)
        self.textChanged.emit(self._text)

    @property
    def text_color(self):
        return self._text_color

    @text_color.setter
    def text_color(self, color_tuple):
        self._text_color = python.force_list(color_tuple)
        self.textColorChanged.emit(self._text_color)

    def _insert_text(self, text):
        self.textInserted.emit(text)


class ConsoleController(object):
    def __init__(self, model):
        super(ConsoleController, self).__init__()

        self._model = model

    def set_text(self, text):
        self._model.text = text

    def insert_text(self, text):
        self._model._insert_text(text)

    def set_text_color(self, color_tuple):
        self._model.text_color = color_tuple

    def clear(self):
        self._model.text_color = Console.NORMAL_COLOR
        self._model.text = ''
