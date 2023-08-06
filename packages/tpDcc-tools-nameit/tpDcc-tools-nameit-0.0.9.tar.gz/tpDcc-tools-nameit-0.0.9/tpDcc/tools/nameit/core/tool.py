#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Tool that manages the nomenclature of your pipelines
"""

from __future__ import print_function, division, absolute_import

import os
import sys

from tpDcc.core import tool

from tpDcc.tools.nameit.core import consts, toolset


class NameItTool(tool.DccTool, object):

    ID = consts.TOOL_ID
    TOOLSET_CLASS = toolset.NameItToolset

    def __init__(self, *args, **kwargs):
        super(NameItTool, self).__init__(*args, **kwargs)

    @classmethod
    def config_dict(cls, file_name=None):
        base_tool_config = tool.DccTool.config_dict(file_name=file_name)
        tool_config = {
            'name': 'NameIt',
            'id': cls.ID,
            'icon': 'nameit',
            'tooltip': 'Tool that manages the nomenclature of your pipelines',
            'tags': ['tpDcc', 'dcc', 'tool', 'nomenclature', 'paths', 'nameit'],
            'is_checkable': False,
            'is_checked': False,
            'menu_ui': {'label': 'Renamer', 'load_on_startup': False, 'color': '', 'background_color': ''},
        }
        base_tool_config.update(tool_config)

        return base_tool_config

    def launch(self, *args, **kwargs):
        return self.launch_frameless(*args, **kwargs)


if __name__ == '__main__':
    import tpDcc.loader
    from tpDcc.managers import tools

    tool_path = os.path.abspath(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__)))))
    if tool_path not in sys.path:
        sys.path.append(tool_path)

    tpDcc.loader.init(dev=False)

    tools.ToolsManager().launch_tool_by_id(NameItTool.ID)
