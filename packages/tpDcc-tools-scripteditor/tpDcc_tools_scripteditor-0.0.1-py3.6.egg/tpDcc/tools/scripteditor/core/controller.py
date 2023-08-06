#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""
Module that contains model implementation for Script Editor
"""

from __future__ import print_function, division, absolute_import

import os
import sys
import logging
import traceback

from Qt.QtCore import QObject, QCoreApplication

from tpDcc import dcc
from tpDcc.libs.python import path as path_utils

from tpDcc.tools.scripteditor.core import model as script_model
from tpDcc.tools.scripteditor.core import consts

LOGGER = logging.getLogger('tpDcc-tools-scripteditor')


class ScriptEditorController(QObject):
    def __init__(self, model, client, load_session=True, settings=None):
        super(ScriptEditorController, self).__init__()

        self._model = model or script_model.ScriptEditorModel()
        self._client = client
        self._settings = settings

        if load_session:
            self.load_session()

        self.update_namespace({
            'self_main': self,
            'self._context': self._client.get_name()
        })

    @property
    def client(self):
        return self._client

    @property
    def settings(self):
        return self._settings

    def get_session(self):
        return self._model.session

    def set_output_text(self, value):
        self._model.output_text = value

    def append_output_text(self, value):
        current_text = self._model.output_text
        if current_text:
            self._model.output_text = '{}\n{}'.format(current_text, value)
        else:
            self._model.output_text = value

    def set_current_script(self, script_path):
        self._model.current_script = script_path

    def set_current_text(self, text):
        self._model.current_text = text

    def set_selected_text(self, text):
        self._model.selected_text = text

    def load_session(self, session_path=None):
        if not session_path:
            if self._settings:
                session_path = os.path.join(
                    os.path.normpath(os.path.dirname(self._settings.fileName())), consts.DEFAULT_SESSION_NAME)
            else:
                session_path = os.path.join(
                    path_utils.get_user_data_dir(), 'tpDcc-tools-scripteditor', consts.DEFAULT_SESSION_NAME)

        self._model.session_path = session_path

    def save_current_session(self):
        """
        Function that stores current session state
        """

        current_session = self._model.session
        if current_session:
            current_script = path_utils.clean_path(self._model.current_script)
            opened_scripts = list()
            for script_path, script_data in self._model.scripts.items():
                file_path = path_utils.clean_path(script_path)
                name = os.path.basename(file_path)
                if name.startswith(consts.TEMP_SCRIPT_PREFIX):
                    name = consts.DEFAULT_SCRIPTS_TAB_NAME
                text = script_data.get('text', '')
                size = script_data.get('font_size', 12)
                script = {
                    'name': name,
                    'text': text,
                    'file': file_path,
                    'active': file_path == current_script,
                    'size': size
                }
                opened_scripts.append(script)

            session_path = current_session.write(opened_scripts)
            LOGGER.debug('Script Editor Session saved: {}'.format(session_path.replace('\\', '/')))

        self.save_script()

    def update_namespace(self, namespace_dict):
        namespace = self._model.namespace.copy()
        namespace.update(namespace_dict)
        self._model.namespace = namespace

    def save_script(self, script_path=''):
        """
        Saves scripts opened in current tab into given file. If not given, a file dialog will allow the user to select
            the path of the file
        :param script_path: str
        """

        current_text = self._model.current_text
        current_script = self._model.current_script
        home_dir = os.getenv('HOME') or os.path.expanduser('~')

        if self._model.enable_save_script:
            script_path = script_path or current_script
            if not script_path or not os.path.isfile(script_path):
                script_path = dcc.save_file_dialog(
                    'Save Script', start_directory=home_dir, pattern='Python Files (*.py)')
                if not script_path:
                    return
            try:
                with open(script_path, 'w') as f:
                    f.write(current_text)
                self._model.save_script(script_path)
            except Exception:
                self.append_output_text('Error saving file: {} | {}'.format(script_path, traceback.format_exc))
        else:
            if current_script and os.path.isfile(current_script):
                self._model.save_script(current_script)

    def load_script(self, script_path=''):
        """
        Loads a script into script editor
        :param script_path: str, Path of script to load. If not given, a file dialog will allow the user to
            select the file to open
        """

        home_dir = os.getenv('HOME')
        if not home_dir:
            home_dir = os.path.expanduser('~')

        if not script_path:
            script_path = dcc.select_file_dialog('Open Script', start_directory=home_dir, pattern='Python Files (*.py)')
            if not script_path:
                return False

        if not os.path.isfile(script_path):
            LOGGER.warning('Given script does not exists: {}'.format(script_path))
            return False

        if not script_path or not os.path.isfile(script_path):
            LOGGER.warning('Impossible to open script that does not exists: "{}"'.format(script_path))
            return False

        return self._model.open_script(script_path)

    def execute_script(self, selected=False):
        """
        Executes current script
        :return:
        """

        current_text = self._model.selected_text if selected else self._model.current_text
        if not current_text:
            return

        self.append_output_text(current_text)
        self._execute_command(current_text)

    def _execute_command(self, cmd):
        """
        Internal function that executes the given command
        :param cmd: str, command to execute
        """

        if not cmd:
            return

        tmp_std_out = sys.stdout

        class StdOutProxy(object):
            def __init__(self, write_fn):
                self.write_fn = write_fn
                self.skip = False

            def write(self, text):
                if not self.skip:
                    stripped_text = text.rstrip('\n')
                    self.write_fn(stripped_text)
                    QCoreApplication.processEvents()
                self.skip = not self.skip

            def flush(self):
                pass
        sys.stdout = StdOutProxy(self.append_output_text)

        try:
            try:
                result = eval(cmd, self._model.namespace, self._model.namespace)
                if result is not None:
                    self.append_output_text(repr(result))
            except SyntaxError:
                exec(cmd, self._model.namespace)
        except SystemExit:
            pass
            # self.close()
        except Exception:
            traceback_lines = traceback.format_exc().split('\n')
            for i in (3, 2, 1, -1):
                traceback_lines.pop(i)
            self.append_output_text('\n'.join(traceback_lines))

        sys.stdout = tmp_std_out

    def convert_tab_to_spaces(self):

        script_text = self._model.current_text
        script_text = script_text.replace('\t', '    ')
        self.set_current_text(script_text)

    def close_all_scripts(self):
        self._model.close_all_scripts()
