#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""
Module that contains core implementation for Script Editor Tool
"""

from __future__ import print_function, division, absolute_import

import logging

from tpDcc.core import tool

from tpDcc.tools.scripteditor.core import consts
from tpDcc.tools.scripteditor.core import client
from tpDcc.tools.scripteditor.core import toolset

LOGGER = logging.getLogger(consts.TOOL_ID)


class ScriptEditorTool(tool.DccTool, object):

    ID = consts.TOOL_ID
    CLIENT_CLASS = client.ScriptEditorClient
    TOOLSET_CLASS = toolset.ScriptEditorToolset

    def __init__(self, *args, **kwargs):
        super(ScriptEditorTool, self).__init__(*args, **kwargs)

    @classmethod
    def config_dict(cls, file_name=None):
        base_tool_config = tool.DccTool.config_dict(file_name=file_name)
        tool_config = {
            'name': 'Script Editor',
            'id': ScriptEditorTool.ID,
            'supported_dccs': {'maya': ['2017', '2018', '2019', '2020']},
            'icon': 'scripteditor',
            'tooltip': 'Renamer Tool to easily rename DCC objects in a visual way',
            'tags': ['tpDcc', 'dcc', 'tool', 'script', 'editor'],
            'is_checkable': False,
            'is_checked': False,
            'menu_ui': {'label': 'Script Editor', 'load_on_startup': False, 'color': '', 'background_color': ''},
        }
        base_tool_config.update(tool_config)

        return base_tool_config

    def launch(self, *args, **kwargs):
        return self.launch_frameless(*args, **kwargs)


if __name__ == '__main__':
    import tpDcc.loader
    from tpDcc.managers import tools
    tpDcc.loader.init()
    tools.ToolsManager().launch_tool_by_id('tpDcc-tools-scripteditor')
