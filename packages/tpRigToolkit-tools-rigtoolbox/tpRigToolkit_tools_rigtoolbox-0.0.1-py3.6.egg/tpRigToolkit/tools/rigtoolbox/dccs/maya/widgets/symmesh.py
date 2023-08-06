#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""
Module that contains widget for symmesh functionality
"""

from __future__ import print_function, division, absolute_import

from tpRigToolkit.tools.symmesh.core import client, tool, toolset
from tpRigToolkit.tools.rigtoolbox.widgets import base


class SymmeshToolset(toolset.SymMeshToolset):
    def __init__(self, *args, **kwargs):
        super(SymmeshToolset, self).__init__(*args, **kwargs)

        self._symmesh_client = client.SymmeshClient.create_and_connect_to_server(tool.SymMeshTool.ID)
        self.initialize(client=self._symmesh_client)
        self._title_frame.setVisible(False)


class SymmeshWidget(base.BaseRigToolBoxWidget, object):
    def __init__(self, parent=None):
        super(SymmeshWidget, self).__init__(title='SymMesh', parent=parent)

        rename_widget = SymmeshToolset(parent=self)
        self.main_layout.addWidget(rename_widget)
