#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""
Module that contains widget for rename functionality
"""

from __future__ import print_function, division, absolute_import

from tpDcc.managers import configs
from tpDcc.tools.renamer.core import client, tool, toolset

from tpRigToolkit.tools.rigtoolbox.widgets import base


class RenameToolset(toolset.RenamerToolset):
    def __init__(self, *args, **kwargs):
        super(RenameToolset, self).__init__(*args, **kwargs)

        self._rename_client = client.RenamerClient.create_and_connect_to_server(tool.RenamerTool.ID)
        self.initialize(client=self._rename_client)
        self._title_frame.setVisible(False)


class RenameWidget(base.BaseRigToolBoxWidget, object):
    def __init__(self, dev=True, parent=None):
        super(RenameWidget, self).__init__(title='Rename', parent=parent)

        names_config = configs.get_config(
            config_name='tpRigToolkit-names', environment='development' if dev else 'production')
        naming_config = configs.get_config(
            config_name='tpRigToolkit-naming', environment='development' if dev else 'production')
        rename_widget = RenameToolset(
            names_config=names_config, naming_config=naming_config, parent=self)
        self.main_layout.addWidget(rename_widget)
