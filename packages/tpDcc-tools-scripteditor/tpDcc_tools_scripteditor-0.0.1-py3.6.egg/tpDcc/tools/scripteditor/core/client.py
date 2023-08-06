#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Module that contains tpDcc-tools-scripteditor client implementation
"""

from __future__ import print_function, division, absolute_import

from tpDcc.core import client


class ScriptEditorClient(client.DccClient, object):

    PORT = 43451

    def get_dcc_completion_directory(self):
        """
        Returns directory where DCC API completion stubs files are located
        :return: str
        """

        cmd = {
            'cmd': 'get_dcc_completion_directory'
        }

        reply_dict = self.send(cmd)

        if not self.is_valid_reply(reply_dict):
            return False

        return reply_dict['result']

    def get_auto_import(self):
        cmd = {
            'cmd': 'get_auto_import'
        }

        reply_dict = self.send(cmd)

        if not self.is_valid_reply(reply_dict):
            return None

        return reply_dict['result']

    def wrap_dropped_text(self, namespace, text, alt_modifier=False):
        cmd = {
            'cmd': 'wrap_dropped_text',
            'namespace': namespace,
            'text': text,
            'alt_modifier': alt_modifier,
        }

        reply_dict = self.send(cmd)

        if not self.is_valid_reply(reply_dict):
            return None

        return reply_dict['result']

    def completer(self, namespace, line):
        cmd = {
            'cmd': 'completer',
            'namespace': namespace,
            'line': line
        }

        reply_dict = self.send(cmd)

        if not self.is_valid_reply(reply_dict):
            return None, None

        return reply_dict['result']
