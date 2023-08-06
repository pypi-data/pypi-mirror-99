#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""
Module that contains model implementation for Script Editor
"""

from __future__ import print_function, division, absolute_import

import os

from Qt.QtCore import Signal, QObject

from tpDcc.libs.python import path as path_utils

from tpDcc.tools.scripteditor.core import consts, session


class ScriptEditorModel(QObject):

    sessionPathChanged = Signal(str)
    namespaceChanged = Signal(dict)
    enableSaveScriptChanged = Signal(bool)
    outputTextChanged = Signal(str)
    scriptOpened = Signal(str)
    scriptClosed = Signal(str)
    scriptSaved = Signal(str)
    currentScriptChanged = Signal(str)
    currentTextChanged = Signal(str)
    selectedTextChanged = Signal(str)
    fontSizeChanged = Signal(int)
    consoleVisibleChanged = Signal(bool)
    toolbarVisibleChanged = Signal(bool)
    menubarVisibleChanged = Signal(bool)

    def __init__(self):
        super(ScriptEditorModel, self).__init__()

        self._session_path = ''
        self._namespace = __import__('__main__').__dict__
        self._enable_save_script = True
        self._output_text = ''
        self._scripts = dict()
        self._console_visible = True
        self._toolbar_visible = True
        self._menubar_visible = True

        self._current_script = ''
        self._session = None

        # if dcc.is_houdini():
        #     size = self._scripts_tab.widget(item).editor.font_size
        # else:
        #     size = self._scripts_tab.widget(item).editor.font().pointSize()

    @property
    def scripts(self):
        return self._scripts

    @property
    def session(self):
        return self._session

    @property
    def session_path(self):
        return self._session_path

    @session_path.setter
    def session_path(self, value):
        self._session_path = str(value)
        self._session = session.Session(self._session_path)
        self.sessionPathChanged.emit(self._session_path)

    @property
    def namespace(self):
        return self._namespace

    @namespace.setter
    def namespace(self, namespace_dit):
        self._namespace = namespace_dit
        self.namespaceChanged.emit(self._namespace)

    @property
    def enable_save_script(self):
        return self._enable_save_script

    @enable_save_script.setter
    def enable_save_script(self, flag):
        self._enable_save_script = bool(flag)
        self.enableSaveScriptChanged.emit(self._enable_save_script)

    @property
    def output_text(self):
        return self._output_text

    @output_text.setter
    def output_text(self, value):
        self._output_text = str(value)
        self.outputTextChanged.emit(self._output_text)

    @property
    def current_script(self):
        return self._current_script

    @current_script.setter
    def current_script(self, value):
        self._current_script = value
        self.currentScriptChanged.emit(self._current_script)

    @property
    def current_text(self):
        current_text = self._scripts.get(self._current_script, dict()).get('text', '')
        return current_text

    @current_text.setter
    def current_text(self, value):
        if not self._current_script:
            return
        current_text = str(value).strip()
        self._scripts.setdefault(self._current_script, dict())['text'] = current_text
        self.currentTextChanged.emit(current_text)

    @property
    def selected_text(self):
        selected_text = self._scripts.get(self._current_script, dict()).get('selected_text', '')
        return selected_text

    @selected_text.setter
    def selected_text(self, value):
        if not self._current_script:
            return
        selected_text = str(value).strip()
        self._scripts.setdefault(self._current_script, dict())['selected_text'] = selected_text
        self.selectedTextChanged.emit(selected_text)

    @property
    def font_size(self):
        font_size = self._scripts.get(self._current_script, dict()).get('font_size', consts.DEFAULT_FONT_SIZE)
        return font_size

    @font_size.setter
    def font_size(self, value):
        if not self._current_script:
            return
        font_size = int(value)
        self._scripts.setdefault(self._current_script, dict())['font_size'] = font_size
        self.fontSizeChanged.emit(font_size)

    @property
    def console_visible(self):
        return self._console_visible

    @console_visible.setter
    def console_visible(self, flag):
        self._console_visible = bool(flag)
        self.consoleVisibleChanged.emit(flag)

    @property
    def toolbar_visible(self):
        return self._toolbar_visible

    @toolbar_visible.setter
    def toolbar_visible(self, flag):
        self._toolbar_visible = bool(flag)
        self.toolbarVisibleChanged.emit(self._toolbar_visible)

    @property
    def menubar_visible(self):
        return self._menubar_visible

    @menubar_visible.setter
    def menubar_visible(self, flag):
        self._menubar_visible = bool(flag)
        self.menubarVisibleChanged.emit(self._menubar_visible)

    def open_script(self, script_path):
        script_path = path_utils.clean_path(script_path)
        if script_path in self._scripts:
            return False
        self._scripts[script_path] = dict()
        self.scriptOpened.emit(script_path)

        return True

    def save_script(self, script_path):
        if not script_path or not os.path.isfile(script_path):
            return
        if script_path not in self._scripts:
            self._scripts[script_path] = dict()
        self.scriptSaved.emit(script_path)

    def close_all_scripts(self):
        closed_scripts = list()
        for script_file_path in list(self._scripts.keys()):
            closed_scripts.append(script_file_path)
        self._scripts.clear()
        for closed_script in closed_scripts:
            self.scriptClosed.emit(closed_script)
