#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Module that contains tpDcc-tools-scripteditor server implementation for Maya
"""

from __future__ import print_function, division, absolute_import

from tpDcc.core import server

import os
import re

import maya.cmds

# TODO: This is slow as hell. Change to cmds
import pymel.core
NODE_TYPES_CACHE = pymel.core.allNodeTypes()


class ScriptEditorServer(server.DccServer, object):

    PORT = 43451

    def _process_command(self, command_name, data_dict, reply_dict):
        if command_name == 'get_dcc_completion_directory':
            self.get_dcc_completion_directory(data_dict, reply_dict)
        elif command_name == 'get_auto_import':
            self.get_auto_import(data_dict, reply_dict)
        elif command_name == 'wrap_dropped_text':
            self.wrap_dropped_text(data_dict, reply_dict)
        elif command_name == 'completer':
            self.completer(data_dict, reply_dict)
        else:
            super(ScriptEditorServer, self)._process_command(command_name, data_dict, reply_dict)

    def get_dcc_completion_directory(self, data, reply):

        completion_path = os.path.join(
            os.environ['MAYA_LOCATION'], 'devkit/other/pymel/extras/completion/py').replace('\\', '/')

        reply['result'] = completion_path
        reply['success'] = True

    def get_auto_import(self, data, reply):
        reply['success'] = True
        reply['result'] = None

    def wrap_dropped_text(self, data, reply):
        namespace = data.get('namespace', dict())
        text = data['text']
        alt_modifier = data['alt_modifier']

        reply['success'] = True
        reply['result'] = None

        reply['result'] = text or ''

        if not alt_modifier:
            return

        # update given namespace with the namespace of the DCC
        # otherweise DCC specific modules will not be available
        namespace.update(__import__('__main__').__dict__)

        # pymel with namespace
        for k, m in namespace.items():
            if hasattr(m, '__name__'):
                if m.__name__ == 'pymel.core' and not k == 'm':
                    syntax = []
                    for node in text.split():
                        if namespace[k].objExists(node):
                            syntax.append(k + '.PyNode("%s")' % node)
                        else:
                            syntax.append(node)
                    reply['result'] = '\n'.join(syntax)
        # pymel no namespace
        if 'PyNode' in namespace.keys():
            syntax = []
            for node in text.split():
                if namespace['objExists'](node):
                    syntax.append('PyNode("%s")' % node)
                else:
                    syntax.append(node)
            reply['result'] = '\n'.join(syntax)

        # cmds with namespace
        for k, m in namespace.items():
            if hasattr(m, '__name__'):
                if m.__name__ == 'maya.cmds' and not k == 'm':
                    syntax = []
                    for node in text.split():
                        if namespace[k].objExists(node):
                            syntax.append('"%s"' % node)
                        else:
                            syntax.append(node)
                    reply['result'] = '\n'.join(syntax)

        # cmds without namespace
        if 'about' in namespace.keys():
            try:
                syntax = []
                for node in text.split():
                    if namespace['objExists'](node):
                        syntax.append('"%s"' % node)
                    else:
                        syntax.append(node)
                reply['result'] = '\n'.join(syntax)
                return
            except Exception:
                pass

        reply['result'] = text

    def completer(self, data, reply):
        namespace = data['namespace']
        line = data['line']

        reply['success'] = True

        # create node
        p = r"createNode\(['\"](\w*)$"
        m = re.search(p, line)
        if m:
            name = m.group(1)
            if name:
                auto = [x for x in NODE_TYPES_CACHE if x.lower().startswith(name.lower())]
                name_length = len(name)
                reply['result'] = [(x, x[name_length:], True) for x in auto], None
                return
        # exists nodes
        p = r"PyNode\(['\"](\w*)$"
        m = re.search(p, line)
        if m:
            name = m.group(1)
            exists_nodes = sorted(maya.cmds.ls(sl=True))
            name_length = len(name)
            if name:
                auto = [x for x in exists_nodes if x.lower().startswith(name.lower())]
                reply['result'] = [(x, x[name_length:], True) for x in auto], None
            else:
                reply['result'] = [(x, x, True) for x in exists_nodes], None

        reply['result'] = None, None
