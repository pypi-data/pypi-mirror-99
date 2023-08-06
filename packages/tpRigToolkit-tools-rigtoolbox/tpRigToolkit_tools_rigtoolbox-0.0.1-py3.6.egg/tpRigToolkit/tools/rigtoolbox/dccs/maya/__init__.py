#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Init module of RigToolbox for Maya
"""

from __future__ import print_function, division, absolute_import

import logging
import traceback

from tpRigToolkit.tools.rigtoolbox.core import consts

LOGGER = logging.getLogger(consts.TOOL_ID)


def get_toolbox_widgets(client, commands_data, parent=None):

    all_widgets = list()
    try:
        from tpRigToolkit.tools.rigtoolbox.dccs.maya.widgets import general
        general_commands_data = commands_data.get('general', dict())
        if commands_data:
            general_widget = general.GeneralWidget(commands_data=general_commands_data, client=client, parent=parent)
            all_widgets.append(general_widget)
        else:
            LOGGER.warning('General widget not loaded because not commands data found!')
    except Exception:
        LOGGER.exception('Error while creating general widget: "{}"'.format(traceback.format_exc()))

    try:
        from tpRigToolkit.tools.rigtoolbox.dccs.maya.widgets import joint
        joint_commmand_data = commands_data.get('joint', dict())
        if joint_commmand_data:
            joint_widget = joint.JointWidget(commands_data=joint_commmand_data, client=client, parent=parent)
            all_widgets.append(joint_widget)
    except Exception:
        LOGGER.exception('Error while creating joint widget: "{}"'.format(traceback.format_exc()))

    try:
        from tpRigToolkit.tools.rigtoolbox.dccs.maya.widgets import skin
        skin_commmand_data = commands_data.get('skin', dict())
        skinning_widget = skin.SkinningWidget(commands_data=skin_commmand_data, client=client, parent=parent)
        skinning_widget.refresh()
        all_widgets.append(skinning_widget)
    except Exception:
        LOGGER.exception('Error while creating skinning widget: "{}"'.format(traceback.format_exc()))

    try:
        from tpRigToolkit.tools.rigtoolbox.dccs.maya.widgets import rename
        client.setup_renamer_client()
        rename_widget = rename.RenameWidget()
        rename_widget.setParent(parent)
        all_widgets.append(rename_widget)
    except Exception:
        LOGGER.exception('Error while creating renamer widget: "{}"'.format(traceback.format_exc()))

    try:
        from tpRigToolkit.tools.rigtoolbox.dccs.maya.widgets import control
        client.setup_control_rig_client()
        control_widget = control.ControlWidget()
        control_widget.setParent(parent)
        all_widgets.append(control_widget)
    except Exception:
        LOGGER.exception('Error while creating control widget: "{}"'.format(traceback.format_exc()))

    try:
        from tpRigToolkit.tools.rigtoolbox.dccs.maya.widgets import symmesh
        client.setup_symmesh_client()
        symmesh_widget = symmesh.SymmeshWidget()
        symmesh_widget.setParent(parent)
        all_widgets.append(symmesh_widget)
    except Exception:
        LOGGER.exception('Error while creating symmesh widget: "{}"'.format(traceback.format_exc()))

    return all_widgets
