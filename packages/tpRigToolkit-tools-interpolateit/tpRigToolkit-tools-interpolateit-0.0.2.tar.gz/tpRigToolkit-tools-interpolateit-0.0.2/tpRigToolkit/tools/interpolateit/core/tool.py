#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Tool to store/blend interpolate states of objects
"""

from __future__ import print_function, division, absolute_import

import os
import sys

from tpDcc.core import tool

from tpRigToolkit.tools.interpolateit.core import consts, client, toolset


class InterpolateItTool(tool.DccTool, object):

    ID = consts.TOOL_ID
    CLIENT_CLASS = client.InterpolateItClient
    TOOLSET_CLASS = toolset.InterpolateItToolset

    def __init__(self, *args, **kwargs):
        super(InterpolateItTool, self).__init__(*args, **kwargs)

    @classmethod
    def config_dict(cls, file_name=None):
        base_tool_config = tool.DccTool.config_dict(file_name=file_name)
        tool_config = {
            'name': 'Interpolate It',
            'id': cls.ID,
            'supported_dccs': {'maya': ['2017', '2018', '2019', '2020', '2021']},
            'logo': 'interpolateit',
            'icon': 'interpolateit',
            'tooltip': 'Tool to store/blend interpolate states of objects',
            'tags': ['tpRigToolkit', 'interpolate', 'animation', 'state', 'pose'],
            'menu_ui': {'label': 'Interpolate It', 'load_on_startup': False, 'color': '', 'background_color': ''},
            'size': [425, 600]
        }
        base_tool_config.update(tool_config)

        return base_tool_config

    def launch(self, *args, **kwargs):
        return self.launch_frameless(*args, **kwargs)


if __name__ == '__main__':
    import tpRigToolkit.loader
    from tpDcc.managers import tools

    tool_path = os.path.abspath(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__)))))
    if tool_path not in sys.path:
        sys.path.append(tool_path)

    tpRigToolkit.loader.init()

    tools.ToolsManager().launch_tool_by_id(InterpolateItTool.ID)
