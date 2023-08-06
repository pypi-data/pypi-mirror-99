#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""
Module that contains library with joint functions
"""

from __future__ import print_function, division, absolute_import

import maya.cmds

from tpDcc import dcc
from tpDcc.libs.python import python

from tpDcc.dccs.maya.core import decorators, joint as joint_utils, curve as curve_utils


def get_valid_joints(joints=None):

    valid_joints = list()
    joints = joints or dcc.selected_nodes_of_type(node_type='joint', full_path=False)
    joints = python.force_list(joints)
    for joint in joints:
        if not dcc.object_type(joint) == 'joint':
            continue
        valid_joints.append(joint)
    if not valid_joints:
        valid_joints = dcc.list_nodes(node_type='joint')

    return valid_joints


@decorators.undo
@decorators.repeat_static_command(__name__, skip_arguments=True)
def start_joint_tool():
    """
    Initializes joint tool
    """

    out_dict = {'success': False, 'result': list()}

    try:
        dcc.start_joint_tool()
    except Exception as exc:
        out_dict['msg'] = 'Was not possible to open joint tool: {}'.format(exc)
        return out_dict

    out_dict['success'] = True

    return out_dict


@decorators.undo
@decorators.repeat_static_command(__name__, skip_arguments=True)
def create_new_joint_on_center(transforms=None):
    """
    Creates a new joint in the center of the selected transforms
    """

    out_dict = {'success': False, 'result': None}

    try:
        selection = maya.cmds.ls(sl=True)
        if transforms:
            result = joint_utils.create_joint_on_center()
        else:
            if '.[' in selection:
                result = joint_utils.create_joints_on_selected_components_center()
            else:
                result = joint_utils.create_joint_on_center()
        out_dict['result'] = result
    except Exception as exc:
        out_dict['msg'] = 'Was not possible to open joint tool: {}'.format(exc)
        return out_dict

    out_dict['success'] = True

    return out_dict


@decorators.undo
@decorators.repeat_static_command(__name__, skip_arguments=True)
def create_joints_on_selected_components_center():
    """
    Creates new joints on the selected components center
    """

    out_dict = {'success': False, 'result': None}

    try:

        new_joints = joint_utils.create_joints_on_selected_components_center()
        out_dict['result'] = new_joints
    except Exception as exc:
        out_dict['success'] = False
        out_dict['msg'] = 'Was not possible to create joints on selected components center: {}'.format(exc)
        return out_dict

    if not new_joints:
        out_dict['success'] = False
        out_dict['msg'] = 'No components to create joints on'
        return out_dict

    out_dict['success'] = True

    return out_dict


@decorators.undo
@decorators.repeat_static_command(__name__, skip_arguments=True)
def insert_joints(joints=None, num_joints=1):
    """
    Inserts new joints between selected joint and its direct child
    :param joints: int
    :param num_joints: int
    """

    out_dict = {'success': False, 'result': None}

    joints = joints or dcc.selected_nodes_of_type(node_type='joint')
    joints = python.force_list(joints)
    if not joints:
        out_dict['msg'] = 'No joints to insert joints into found.'
        return out_dict

    try:

        result = joint_utils.insert_joints(joints=joints, joint_count=num_joints)
        out_dict['result'] = result
    except Exception as exc:
        out_dict['msg'] = 'Was not possible to insert joints: {}'.format(exc)
        return out_dict

    out_dict['success'] = True

    return out_dict


@decorators.undo
@decorators.repeat_static_command(__name__, skip_arguments=True)
def create_joints_on_curve(curve=None, num_joints=1):

    out_dict = {'success': False, 'result': list()}

    valid_curves = list()
    curves = curve or dcc.selected_nodes_of_type(node_type='transform')
    curves = python.force_list(curves)
    for curve in curves:
        if not curve_utils.is_a_curve(curve):
            continue
        valid_curves.append(curve)
    if not valid_curves:
        out_dict['msg'] = 'No curves to create joints on found.'
        return out_dict

    try:
        for curve in valid_curves:
            new_joint = joint_utils.create_oriented_joints_along_curve(curve, num_joints)
            out_dict['result'].append(new_joint)
    except Exception as exc:
        out_dict['msg'] = 'Was not possible to create joints on curve: {}'.format(exc)
        return out_dict

    out_dict['success'] = True

    return out_dict


@decorators.undo
@decorators.repeat_static_command(__name__, skip_arguments=True)
def snap_joints_to_curve(joints=None, curve=None, num_joints=1):

    out_dict = {'success': False, 'result': dict()}

    valid_joints = list()
    joints = joints or dcc.selected_nodes_of_type(node_type='joint')
    joints = python.force_list(joints)
    for joint in joints:
        if not dcc.object_type(joint) == 'joint':
            continue
        valid_joints.append(joint)
    if not valid_joints:
        out_dict['msg'] = 'No joints to snap to curve found.'
        return out_dict

    valid_curves = list()
    curves = curve or dcc.selected_nodes_of_type(node_type='transform')
    curves = python.force_list(curves)
    for curve in curves:
        if not curve_utils.is_a_curve(curve):
            continue
        valid_curves.append(curve)

    try:
        for curve in valid_curves:
            new_joints = curve_utils.snap_joints_to_curve(valid_joints, curve=curve, count=num_joints)
            out_dict['result'][curve] = new_joints
    except Exception as exc:
        out_dict['msg'] = 'Was not possible to snap joints to curve: {}'.format(exc)
        return out_dict

    out_dict['success'] = True

    return out_dict


def check_joint_labels(joints=None):

    out_dict = {'success': False, 'result': False}

    valid_joints = list()
    joints = joints or dcc.selected_nodes_of_type(node_type='joint')
    joints = python.force_list(joints)
    for joint in joints:
        if not dcc.object_type(joint) == 'joint':
            continue
        valid_joints.append(joint)
    if not valid_joints:
        out_dict['msg'] = 'No joints to check found.'
        return out_dict

    try:
        result = joint_utils.check_joint_labels(valid_joints)
        out_dict['result'] = result
    except Exception as exc:
        out_dict['msg'] = 'Was not possible to check joints label: {}'.format(exc)
        return out_dict

    out_dict['success'] = True

    return out_dict


@decorators.undo
@decorators.repeat_static_command(__name__, skip_arguments=True)
def toggle_local_rotation_axis(joints=None):
    """
     Toggles the visibility of all (if the user has nothing selected) or all joints local rotation axis
     """

    out_dict = {'success': False, 'result': dict()}

    valid_joints = list()
    joints = joints or dcc.selected_nodes_of_type(node_type='joint')
    joints = python.force_list(joints)
    for joint in joints:
        if not dcc.object_type(joint) == 'joint':
            continue
        valid_joints.append(joint)
    if not valid_joints:
        valid_joints = None

    dcc.set_joint_local_rotation_axis_visibility(flag=None, joints_to_apply=valid_joints)

    out_dict['success'] = True

    return out_dict


@decorators.undo
@decorators.repeat_static_command(__name__, skip_arguments=True)
def toggle_all_local_rotation_axis(flag=None):
    """
    Toggles the visibility of all joints local rotation axis
    """

    out_dict = {'success': False, 'result': dict()}

    dcc.set_joint_local_rotation_axis_visibility(flag=flag, joints_to_apply=None)

    out_dict['success'] = True

    return out_dict


@decorators.undo
@decorators.repeat_static_command(__name__, skip_arguments=True)
def toggle_selected_local_rotation_axis(flag=None):
    """
    Toggles the visibility of selected joints local rotation axis
    """

    out_dict = {'success': False, 'result': dict()}

    joints = dcc.selected_nodes_of_type(node_type='joint')
    if not joints:
        out_dict['msg'] = 'No joints to toggle LRA of found.'
        return out_dict

    dcc.set_joint_local_rotation_axis_visibility(flag=flag, joints_to_apply=joints)

    out_dict['success'] = True

    return out_dict


@decorators.undo
@decorators.repeat_static_command(__name__, skip_arguments=True)
def toggle_joints_xray():
    out_dict = {'success': False, 'result': dict()}

    dcc.toggle_xray_joints()

    out_dict['success'] = True

    return out_dict


@decorators.undo
@decorators.repeat_static_command(__name__, skip_arguments=True)
def set_joints_xray(flag=None):
    out_dict = {'success': False, 'result': dict()}

    if flag is None:
        dcc.toggle_xray_joints()
    else:
        current_panel = maya.cmds.getPanel(withFocus=True)
        maya.cmds.modelEditor(current_panel, edit=True, jointXray=flag)

    out_dict['success'] = True

    return out_dict


@decorators.undo
@decorators.repeat_static_command(__name__, skip_arguments=True)
def set_joints_display_size(value=None):
    out_dict = {'success': False, 'result': dict()}

    if value is None:
        value = dcc.get_joint_display_size()

    dcc.set_joint_display_size(value)

    out_dict['success'] = True

    return out_dict


@decorators.undo
@decorators.repeat_static_command(__name__, skip_arguments=True)
def select_hierarchy():
    out_dict = {'success': False, 'result': dict()}

    dcc.select_hierarchy()

    out_dict['success'] = True

    return out_dict


@decorators.undo
@decorators.repeat_static_command(__name__, skip_arguments=True)
def orient_joints(joints=None, force_orient_attributes=True):
    """
    Orients all joints that have OrientJointAttributes added
    :param joints: list(str) or None
    :param force_orient_attributes: bool, Whether to force the orientation through OrientJointAttributes or not
    """

    out_dict = {'success': False, 'result': dict()}

    valid_joints = get_valid_joints(joints)
    if not valid_joints:
        valid_joints = dcc.list_nodes(node_type='joint')
    if not valid_joints:
        out_dict['msg'] = 'No joints to orient found.'
        return out_dict

    dcc.orient_joints(joints_to_orient=valid_joints, force_orient_attributes=force_orient_attributes)

    out_dict['success'] = True

    return out_dict


@decorators.undo
@decorators.repeat_static_command(__name__, skip_arguments=True)
def orient_all_joints(force_orient_attributes=True):
    """
    Orients all joints
    :param force_orient_attributes: bool, Whether to force the orientation through OrientJointAttributes or not
    """

    out_dict = {'success': False, 'result': dict()}

    all_joints = dcc.list_nodes(node_type='joint', full_path=False)
    if not all_joints:
        out_dict['msg'] = 'No joints to orient found.'
        return out_dict

    dcc.orient_joints(joints_to_orient=all_joints, force_orient_attributes=force_orient_attributes)

    out_dict['success'] = True

    return out_dict


@decorators.undo
@decorators.repeat_static_command(__name__, skip_arguments=True)
def orient_selected_joints(force_orient_attributes=True):
    """
    Orient selected joints
    :param force_orient_attributes: bool, Whether to force the orientation through OrientJointAttributes or not
    """

    out_dict = {'success': False, 'result': dict()}

    valid_joints = get_valid_joints()
    if not valid_joints:
        out_dict['msg'] = 'No joints to orient found.'
        return out_dict

    dcc.orient_joints(joints_to_orient=valid_joints, force_orient_attributes=force_orient_attributes)

    out_dict['success'] = True

    return out_dict


@decorators.undo
@decorators.repeat_static_command(__name__, skip_arguments=True)
def add_orient_data(joints=None):
    """
    Add orient data to joints
    """

    out_dict = {'success': False, 'result': dict()}

    valid_joints = get_valid_joints(joints)
    if not valid_joints:
        valid_joints = dcc.list_nodes(node_type='joint')
    if not valid_joints:
        out_dict['msg'] = 'No joints to add orient data to found.'
        return out_dict

    joint_utils.OrientJointAttributes.add_orient_attributes(valid_joints)

    out_dict['success'] = True

    return out_dict


@decorators.undo
@decorators.repeat_static_command(__name__, skip_arguments=True)
def add_orient_data_all_joints():
    """
    Add orient data to all joints in current scene
    """

    out_dict = {'success': False, 'result': dict()}

    all_joints = dcc.list_nodes(node_type='joint', full_path=False)
    if not all_joints:
        out_dict['msg'] = 'No joints to add orient data to found.'
        return out_dict

    joint_utils.OrientJointAttributes.add_orient_attributes(all_joints)

    out_dict['success'] = True

    return out_dict


@decorators.undo
@decorators.repeat_static_command(__name__, skip_arguments=True)
def add_orient_data_selected_joints():
    """
    Add orient data to selected joints
    """

    out_dict = {'success': False, 'result': dict()}

    valid_joints = get_valid_joints()
    if not valid_joints:
        out_dict['msg'] = 'No joints to add orient data to found.'
        return out_dict

    joint_utils.OrientJointAttributes.add_orient_attributes(valid_joints)

    out_dict['success'] = True

    return out_dict


@decorators.undo
@decorators.repeat_static_command(__name__, skip_arguments=True)
def clean_orient_data(joints=None):
    """
    Clean orient data from joints
    """

    out_dict = {'success': False, 'result': dict()}

    valid_joints = get_valid_joints(joints)
    if not valid_joints:
        valid_joints = dcc.list_nodes(node_type='joint')
    if not valid_joints:
        out_dict['msg'] = 'No joints to remove orient data from found.'
        return out_dict

    joint_utils.OrientJointAttributes.remove_orient_attributes(valid_joints)

    out_dict['success'] = True

    return out_dict


@decorators.undo
@decorators.repeat_static_command(__name__, skip_arguments=True)
def clean_orient_data_all_joints():
    """
    Clean orient data from all joints in current scene
    """

    out_dict = {'success': False, 'result': dict()}

    all_joints = dcc.list_nodes(node_type='joint', full_path=False)
    if not all_joints:
        out_dict['msg'] = 'No joints to remove orient data from found.'
        return out_dict

    joint_utils.OrientJointAttributes.remove_orient_attributes(all_joints)

    out_dict['success'] = True

    return out_dict


@decorators.undo
@decorators.repeat_static_command(__name__, skip_arguments=True)
def clean_orient_data_selected_joints():
    """
    Cleans orient data from selected joints
    """

    out_dict = {'success': False, 'result': dict()}

    valid_joints = get_valid_joints()
    if not valid_joints:
        out_dict['msg'] = 'No joints to remove orient data from found.'
        return out_dict

    joint_utils.OrientJointAttributes.remove_orient_attributes(valid_joints)

    out_dict['success'] = True

    return out_dict


@decorators.undo
@decorators.repeat_static_command(__name__, skip_arguments=True)
def zero_joint_orient(joints=None):
    """
    Zeroes out the data of joints
    """

    out_dict = {'success': False, 'result': dict()}

    valid_joints = get_valid_joints(joints)
    if not valid_joints:
        valid_joints = dcc.list_nodes(node_type='joint')
    if not valid_joints:
        out_dict['msg'] = 'No joints to zero out orient of found.'
        return out_dict

    joint_utils.OrientJointAttributes.zero_orient_joint(valid_joints)

    out_dict['success'] = True

    return out_dict


@decorators.undo
@decorators.repeat_static_command(__name__, skip_arguments=True)
def zero_joint_orient_all_joints():
    """
    Zeroes out the orient of all joints in current scene
    """

    out_dict = {'success': False, 'result': dict()}

    all_joints = dcc.list_nodes(node_type='joint', full_path=False)
    if not all_joints:
        out_dict['msg'] = 'No joints to remove orient data from found.'
        return out_dict

    joint_utils.OrientJointAttributes.zero_orient_joint(all_joints)

    out_dict['success'] = True

    return out_dict


@decorators.undo
@decorators.repeat_static_command(__name__, skip_arguments=True)
def zero_joint_orient_selected_joints():
    """
    Zeroes out the orient of selected joints
    """

    out_dict = {'success': False, 'result': dict()}

    valid_joints = get_valid_joints()
    if not valid_joints:
        out_dict['msg'] = 'No joints to remove orient data from found.'
        return out_dict

    joint_utils.OrientJointAttributes.zero_orient_joint(valid_joints)

    out_dict['success'] = True

    return out_dict


@decorators.undo
@decorators.repeat_static_command(__name__, skip_arguments=True)
def mirror_joints(joints=None):
    """
    Mirror joints
    """

    out_dict = {'success': False, 'result': dict()}

    valid_joints = get_valid_joints(joints)
    if not valid_joints:
        valid_joints = dcc.list_nodes(node_type='joint')
    if not valid_joints:
        out_dict['msg'] = 'No joints to mirror found.'
        return out_dict

    dcc.mirror_transform(valid_joints)

    out_dict['success'] = True

    return out_dict


@decorators.undo
@decorators.repeat_static_command(__name__, skip_arguments=True)
def mirror_all_joints():
    """
    Mirror all joints in current scene
    """

    out_dict = {'success': False, 'result': dict()}

    all_joints = dcc.list_nodes(node_type='joint', full_path=False)
    if not all_joints:
        out_dict['msg'] = 'No joints to mirror found.'
        return out_dict

    dcc.mirror_transform(all_joints, create_if_missing=True)

    out_dict['success'] = True

    return out_dict


@decorators.undo
@decorators.repeat_static_command(__name__, skip_arguments=True)
def mirror_selected_joints():
    """
    Mirror selected joints
    """

    out_dict = {'success': False, 'result': dict()}

    valid_joints = get_valid_joints()
    if not valid_joints:
        out_dict['msg'] = 'No joints to mirror found.'
        return out_dict

    dcc.mirror_transform(create_if_missing=True, transforms=valid_joints)

    out_dict['success'] = True

    return out_dict


@decorators.undo
@decorators.repeat_static_command(__name__, skip_arguments=True)
def mirror_hierarchy_joints():
    """
    Mirror hierarchy joints
    """

    out_dict = {'success': False, 'result': dict()}

    all_joints = list()

    valid_joints = get_valid_joints()
    if not valid_joints:
        out_dict['msg'] = 'No joints to mirror found.'
        return out_dict

    for joint in valid_joints:
        all_joints.append(joint)
        children = dcc.list_children(joint, full_path=False, children_type='transform')
        found = list()
        if children:
            for child in children:
                if dcc.node_type(child).find('Constraint') > -1:
                    continue
                found.append(child)
        all_joints.extend(found)

    all_joints = list(set(all_joints))

    dcc.mirror_transform(transforms=all_joints, create_if_missing=True)

    out_dict['success'] = True

    return out_dict
