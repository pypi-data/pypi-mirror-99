#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""
Module that contains definition for tpScriptEditor sessions
"""

from __future__ import print_function, division, absolute_import

__author__ = "Tomas Poveda"
__license__ = "MIT"
__maintainer__ = "Tomas Poveda"
__email__ = "tpovedatd@gmail.com"

import os
import codecs
import logging

from tpDcc.libs.python import fileio, folder, jsonio

LOGGER = logging.getLogger('tpDcc-tools-scripteditor')


class Session(object):
    def __init__(self, session_path):
        self._path = session_path
        if not os.path.isfile(session_path):
            session_path_dir = os.path.dirname(session_path)
            if not os.path.isdir(session_path_dir):
                folder.create_folder(session_path_dir)
            valid = fileio.create_file(os.path.basename(session_path), os.path.dirname(session_path))
            if not valid:
                LOGGER.warning('Impossible to create session file. Session functionality disabled ...')
                return
            with open(session_path, 'w') as fh:
                fh.write('{}')

    def read(self):
        """
        Reads the current session status
        :return: list
        """

        if not os.path.exists(self._path):
            return list()

        try:
            return jsonio.read_file(self._path)
        except Exception as exc:
            LOGGER.error('Error while reading Script Editor session file: {} | {}'.format(self._path, exc))
            return list()

    def write(self, data):
        """
        Writes session into disk
        :param data: dict
        :return:
        """

        jsonio.write_to_file(data, self._path, indent=4)

        return self._path
