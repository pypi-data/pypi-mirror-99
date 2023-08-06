#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""
Module that contains core implementation for Script Editor Tool
"""

from __future__ import print_function, division, absolute_import

import os
import sys
import logging

from tpDcc.libs.python import path as path_utils
from tpDcc.libs.qt.widgets import toolset

from tpDcc.tools.scripteditor.core import consts

LOGGER = logging.getLogger(consts.TOOL_ID)


class ScriptEditorToolset(toolset.ToolsetWidget, object):
    def __init__(self, *args, **kwargs):
        self._load_session = kwargs.pop('load_session', True)

        super(ScriptEditorToolset, self).__init__(*args, **kwargs)

    @property
    def model(self):
        return self._script_editor_model

    @property
    def view(self):
        return self._script_editor_view

    @property
    def controller(self):
        return self._script_editor_controller

    def contents(self):

        from tpDcc.tools.scripteditor.core import model, view, controller

        self._script_editor_model = model.ScriptEditorModel()
        self._script_editor_controller = controller.ScriptEditorController(
            model=self._script_editor_model, client=self.client, load_session=self._load_session,
            settings=self._settings)
        self._script_editor_view = view.ScriptEditorView(
            model=self._script_editor_model, controller=self._script_editor_controller, parent=self)

        return [self._script_editor_view]

    def set_attacher(self, attacher):
        super(ScriptEditorToolset, self).set_attacher(attacher)

        # Necessary to pass events from main window to view
        self.attacher.installEventFilter(self._script_editor_view)

    def _update_client(self):
        valid = super(ScriptEditorToolset, self)._update_client()
        if not valid:
            return

        # We make sure that DCC specific completion path directory is added to sys.path
        # NOTE: This function is called before any UI is instantiated
        completion_path = self._client.get_dcc_completion_directory()
        if completion_path and os.path.isdir(completion_path):
            completion_path = path_utils.clean_path(completion_path)
            if completion_path in sys.path:
                sys.path.remove(completion_path)
            sys.path.insert(0, completion_path)
