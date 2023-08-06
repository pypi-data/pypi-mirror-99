#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""
Module that contains widget for rig control functionality
"""

from __future__ import print_function, division, absolute_import

from tpRigToolkit.tools.rigtoolbox.widgets import base

from tpRigToolkit.tools.controlrig.core import client, tool, toolset


class ControlRigToolset(toolset.ControlRigToolset):
    def __init__(self, *args, **kwargs):
        super(ControlRigToolset, self).__init__(*args, **kwargs)

        self._control_rig_client = client.ControlRigClient.create_and_connect_to_server(tool.ControlRigTool.ID)
        self.initialize(client=self._control_rig_client)
        self._title_frame.setVisible(False)


class ControlWidget(base.BaseRigToolBoxWidget, object):
    def __init__(self, parent=None):
        super(ControlWidget, self).__init__(title='Controls', parent=parent)

        ctrl_rig = ControlRigToolset(collapsable=False, parent=self)
        self.main_layout.addWidget(ctrl_rig)
