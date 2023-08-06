#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Collection of rigging tools
"""

from __future__ import print_function, division, absolute_import

import os
import sys
import logging

from tpDcc.core import tool
from tpDcc.managers import resources

from tpRigToolkit.tools.rigtoolbox.core import consts, client, toolset

LOGGER = logging.getLogger(consts.TOOL_ID)


class RigToolboxTool(tool.DccTool, object):

    ID = consts.TOOL_ID
    CLIENT_CLASS = client.RigToolboxClient
    TOOLSET_CLASS = toolset.RigToolboxToolset

    def __init__(self, *args, **kwargs):
        super(RigToolboxTool, self).__init__(*args, **kwargs)

        resources_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'resources')
        resources.register_resource(resources_path)

    @classmethod
    def config_dict(cls, file_name=None):
        base_tool_config = tool.DccTool.config_dict(file_name=file_name)
        tool_config = {
            'name': 'Rig ToolBox',
            'id': RigToolboxTool.ID,
            'supported_dccs': {'maya': ['2017', '2018', '2019', '2020']},
            'logo': 'rigtoolbox',
            'icon': 'rigtoolbox',
            'tooltip': 'Collection of tools to improve the rigging process',
            'tags': ['tpRigToolkit', 'rig', 'tools', 'toolbox'],
            'logger_dir': os.path.join(os.path.expanduser('~'), 'tpRigToolkit', 'logs', 'tools'),
            'logger_level': 'INFO',
            'is_checkable': False,
            'is_checked': False,
            'menu_ui': {'label': 'Rig ToolBox', 'load_on_startup': False, 'color': '', 'background_color': ''}
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
    tools.ToolsManager().launch_tool_by_id(consts.TOOL_ID)
