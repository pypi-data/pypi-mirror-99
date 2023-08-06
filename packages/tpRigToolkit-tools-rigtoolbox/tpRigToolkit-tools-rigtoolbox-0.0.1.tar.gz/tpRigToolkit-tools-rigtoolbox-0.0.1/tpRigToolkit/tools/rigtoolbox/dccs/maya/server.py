#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Module that contains rig toolbox server implementation for Maya
"""

from __future__ import print_function, division, absolute_import

__author__ = "Tomas Poveda"
__license__ = "MIT"
__maintainer__ = "Tomas Poveda"
__email__ = "tpovedatd@gmail.com"

import os
import traceback

from tpDcc import dcc
from tpDcc.core import server
from tpDcc.libs.python import path as path_utils
from tpDcc.dccs.maya.core import helpers

from tpDcc.tools.renamer.core import tool as renamer_tool
from tpDcc.tools.renamer.dccs.maya import server as renamer_server


from tpRigToolkit.tools.controlrig.core import tool as controlrig_tool
from tpRigToolkit.tools.controlrig.dccs.maya import server as controlrig_server
from tpRigToolkit.tools.jointorient.core import tool as jointorient_tool
from tpRigToolkit.tools.jointorient.dccs.maya import server as jointorient_server
from tpRigToolkit.tools.symmesh.core import tool as symmesh_tool
from tpRigToolkit.tools.symmesh.dccs.maya import server as symmesh_server

from tpRigToolkit.tools.rigtoolbox.dccs.maya.libs import general, joint, skin


class RigToolboxServer(server.DccServer, object):

    PORT = 19344

    def __init__(self, *args, **kwargs):
        super(RigToolboxServer, self).__init__(*args, **kwargs)

        self._renamer_client = None
        self._control_rig_client = None
        self._orient_joint_client = None
        self._symmesh_client = None

    # =================================================================================================================
    # RENAMER
    # =================================================================================================================

    def setup_renamer_client(self, data, reply):
        if not self._renamer_client:
            self._renamer_client = dcc.client(renamer_tool.RenamerTool.ID)
        try:
            try:
                self._renamer_client.close_connection()
            except Exception:
                pass
            self._renamer_client = renamer_server.RenamerServer()
        except Exception:
            print('Error while setting up renamer server: '.format(traceback.format_exc()))

        reply['success'] = True

    def setup_control_rig_client(self, data, reply):
        if not self._control_rig_client:
            self._control_rig_client = dcc.client(controlrig_tool.ControlRigTool.ID)
        try:
            try:
                self._control_rig_client.close_connection()
            except Exception:
                pass
            self._control_rig_client = controlrig_server.ControlRigServer()
        except Exception:
            print('Error while setting up control rig server: '.format(traceback.format_exc()))

        reply['success'] = True

    def setup_orient_joint_client(self, data, reply):
        if not self._orient_joint_client:
            self._orient_joint_client = dcc.client(jointorient_tool.JointOrientTool.ID)
        try:
            try:
                self._orient_joint_client.close_connection()
            except Exception:
                pass
            self._orient_joint_client = jointorient_server.JointOrientServer()
        except Exception:
            print('Error while setting up joint orient server: '.format(traceback.format_exc()))

        reply['success'] = True

    def setup_symmesh_client(self, data, reply):
        if not self._symmesh_client:
            self._symmesh_client = dcc.client(symmesh_tool.SymMeshTool.ID)
        try:
            try:
                self._symmesh_client.close_connection()
            except Exception:
                pass
            self._symmesh_client = symmesh_server.SymmeshServer()
        except Exception:
            print('Error while setting up symmesh server: '.format(traceback.format_exc()))

        reply['success'] = True

    # =================================================================================================================
    # GENERAL
    # =================================================================================================================

    def delete_history(self, data, reply):

        transforms = data['transforms']

        try:
            result = general.delete_history(transforms)
            reply.update(result)
        except Exception:
            if not reply['msg']:
                reply['msg'] = 'Something went wrong while deleting history: {}'.format(traceback.format_exc())
            reply['success'] = False

    def freeze_transforms(self, data, reply):

        transforms = data['transforms']

        try:
            result = general.freeze_transforms(transforms)
            reply.update(result)
        except Exception:
            if not reply['msg']:
                reply['msg'] = 'Something went wrong while freezing transforms: {}'.format(traceback.format_exc())
            reply['success'] = False

    def move_pivot_to_zero(self, data, reply):
        transforms = data['transforms']

        try:
            result = general.move_pivot_to_zero(transforms)
            reply.update(result)
        except Exception:
            if not reply['msg']:
                reply['msg'] = 'Something went wrong while moving pivots to zero: {}'.format(traceback.format_exc())
            reply['success'] = False

    def lock_all_transforms(self, data, reply):
        transforms = data['transforms']

        try:
            result = general.lock_all_transforms(transforms)
            reply.update(result)
        except Exception:
            if not reply['msg']:
                reply['msg'] = 'Something went wrong while locking all transforms channels: {}'.format(
                    traceback.format_exc())
            reply['success'] = False

    def lock_translation(self, data, reply):
        transforms = data['transforms']

        try:
            result = general.lock_translation(transforms)
            reply.update(result)
        except Exception:
            if not reply['msg']:
                reply['msg'] = 'Something went wrong while locking translate channels: {}'.format(
                    traceback.format_exc())
            reply['success'] = False

    def lock_rotation(self, data, reply):
        transforms = data['transforms']

        try:
            result = general.lock_rotation(transforms)
            reply.update(result)
        except Exception:
            if not reply['msg']:
                reply['msg'] = 'Something went wrong while locking rotate channels: {}'.format(traceback.format_exc())
            reply['success'] = False

    def lock_scale(self, data, reply):
        transforms = data['transforms']

        try:
            result = general.lock_scale(transforms)
            reply.update(result)
        except Exception:
            if not reply['msg']:
                reply['msg'] = 'Something went wrong while locking scale channel: {}'.format(traceback.format_exc())
            reply['success'] = False

    def lock_visibility(self, data, reply):
        transforms = data['transforms']

        try:
            result = general.lock_visibility(transforms)
            reply.update(result)
        except Exception:
            if not reply['msg']:
                reply['msg'] = 'Something went wrong while locking visibility channel: {}'.format(
                    traceback.format_exc())
            reply['success'] = False

    def unlock_all_transforms(self, data, reply):
        transforms = data['transforms']

        try:
            result = general.unlock_all_transforms(transforms)
            reply.update(result)
        except Exception:
            if not reply['msg']:
                reply['msg'] = 'Something went wrong while unlocking all transforms channels: {}'.format(
                    traceback.format_exc())
            reply['success'] = False

    def unlock_translation(self, data, reply):
        transforms = data['transforms']

        try:
            result = general.unlock_translation(transforms)
            reply.update(result)
        except Exception:
            if not reply['msg']:
                reply['msg'] = 'Something went wrong while unlocking translate channels: {}'.format(
                    traceback.format_exc())
            reply['success'] = False

    def unlock_rotation(self, data, reply):
        transforms = data['transforms']

        try:
            result = general.unlock_rotation(transforms)
            reply.update(result)
        except Exception:
            if not reply['msg']:
                reply['msg'] = 'Something went wrong while unlocking rotate channels: {}'.format(traceback.format_exc())
            reply['success'] = False

    def unlock_scale(self, data, reply):
        transforms = data['transforms']

        try:
            result = general.unlock_scale(transforms)
            reply.update(result)
        except Exception:
            if not reply['msg']:
                reply['msg'] = 'Something went wrong while unlocking scale channel: {}'.format(traceback.format_exc())
            reply['success'] = False

    def unlock_visibility(self, data, reply):
        transforms = data['transforms']

        try:
            result = general.unlock_visibility(transforms)
            reply.update(result)
        except Exception:
            if not reply['msg']:
                reply['msg'] = 'Something went wrong while unlocking visibility channel: {}'.format(
                    traceback.format_exc())
            reply['success'] = False

    def clean_student_license(self, data, reply):
        file_path = data.get('file_path', None)

        try:
            helpers.clean_student_line(file_path)
            reply['success'] = True
        except Exception:
            if not reply['msg']:
                reply['msg'] = 'Something went wrong while cleaning student license: {}'.format(
                    traceback.format_exc())
            reply['success'] = False

    def match_transform(self, data, reply):
        source_transform = data['source_transform']
        target_transform = data['target_transform']

        try:
            result = general.match_transform(source_transform, target_transform)
            reply.update(result)
        except Exception:
            if not reply['msg']:
                reply['msg'] = 'Something went wrong while matching transforms: {}'.format(traceback.format_exc())
            reply['success'] = False

    def match_translation(self, data, reply):
        source_transform = data['source_transform']
        target_transform = data['target_transform']

        try:
            result = general.match_translation(source_transform, target_transform)
            reply.update(result)
        except Exception:
            if not reply['msg']:
                reply['msg'] = 'Something went wrong while matching translation: {}'.format(traceback.format_exc())
            reply['success'] = False

    def match_rotation(self, data, reply):
        source_transform = data['source_transform']
        target_transform = data['target_transform']

        try:
            result = general.match_rotation(source_transform, target_transform)
            reply.update(result)
        except Exception:
            if not reply['msg']:
                reply['msg'] = 'Something went wrong while matching rotation: {}'.format(traceback.format_exc())
            reply['success'] = False

    def match_scale(self, data, reply):
        source_transform = data['source_transform']
        target_transform = data['target_transform']

        try:
            result = general.match_scale(source_transform, target_transform)
            reply.update(result)
        except Exception:
            if not reply['msg']:
                reply['msg'] = 'Something went wrong while matching scale: {}'.format(traceback.format_exc())
            reply['success'] = False

    def combine_meshes(self, data, reply):
        meshes = data['meshes']
        new_mesh_name = data['new_mesh_name']

        try:
            result = general.combine_meshes(meshes, new_mesh_name)
            reply.update(result)
        except Exception:
            if not reply['msg']:
                reply['msg'] = 'Something went wrong while combining meshes: {}'.format(traceback.format_exc())
            reply['success'] = False

    def separate_meshes(self, data, reply):
        meshes = data['meshes']

        try:
            result = general.separate_meshes(meshes)
            reply.update(result)
        except Exception:
            if not reply['msg']:
                reply['msg'] = 'Something went wrong while separating meshes: {}'.format(traceback.format_exc())
            reply['success'] = False

    def mirror_meshes(self, data, reply):
        meshes = data['meshes']

        try:
            result = general.mirror_mesh(meshes)
            reply.update(result)
        except Exception:
            if not reply['msg']:
                reply['msg'] = 'Something went wrong while mirroring mesh: {}'.format(traceback.format_exc())
            reply['success'] = False

    def mirror_meshes_options(self, data, reply):
        try:
            result = general.open_mirror_meshes_options()
            reply.update(result)
        except Exception:
            if not reply['msg']:
                reply['msg'] = 'Something went wrong while opening mirror mesh options: {}'.format(
                    traceback.format_exc())
            reply['success'] = False

    def open_symmetry_tool(self, data, reply):
        try:
            result = general.open_symmetry_tool()
            reply.update(result)
        except Exception:
            if not reply['msg']:
                reply['msg'] = 'Something went wrong while opening symmetry tool: {}'.format(traceback.format_exc())
            reply['success'] = False

    def detach_components(self, data, reply):
        components = data['components']

        try:
            result = general.detach_components(components)
            reply.update(result)
        except Exception:
            if not reply['msg']:
                reply['msg'] = 'Something went wrong while detaching components: {}'.format(traceback.format_exc())
            reply['success'] = False

    def curve_from_edge_loop(self, data, reply):
        mesh_edge_list = data['mesh_edge_list']

        try:
            result = general.create_curve_from_mesh_edge_loop(mesh_edge_list)
            reply.update(result)
        except Exception:
            if not reply['msg']:
                reply['msg'] = 'Something went wrong while creating curve from edge loop: {}'.format(
                    traceback.format_exc())
            reply['success'] = False

    # =================================================================================================================
    # MAYA - JOINTS
    # =================================================================================================================

    def start_joint_tool(self, data, reply):
        try:
            result = joint.start_joint_tool()
            reply.update(result)
        except Exception:
            if not reply['msg']:
                reply['msg'] = 'Something went wrong while opening joint tool: {}'.format(traceback.format_exc())
            reply['success'] = False

    def create_new_joint_on_center(self, data, reply):
        transforms = data['transforms']

        try:
            result = joint.create_new_joint_on_center(transforms=transforms)
            reply.update(result)
        except Exception:
            if not reply['msg']:
                reply['msg'] = 'Something went wrong while creating new ' \
                               'joints on the center of transforms: {}'.format(traceback.format_exc())
            reply['success'] = False

    def create_new_joints_on_selected_components(self, data, reply):
        try:
            result = joint.create_joints_on_selected_components_center()
            reply.update(result)
        except Exception:
            if not reply['msg']:
                reply['msg'] = 'Something went wrong while creating new ' \
                               'joints on the center of selected components: {}'.format(traceback.format_exc())
            reply['success'] = False

    def insert_joints(self, data, reply):
        joints = data['joints']
        num_joints = data['num_joints']

        try:
            result = joint.insert_joints(joints, num_joints)
            reply.update(result)
        except Exception:
            if not reply['msg']:
                reply['msg'] = 'Something went wrong while inserting joints: {}'.format(traceback.format_exc())
            reply['success'] = False

    def create_joints_on_curve(self, data, reply):
        curve = data['curve']
        num_joints = data['num_joints']

        try:
            result = joint.create_joints_on_curve(curve, num_joints)
            reply.update(result)
        except Exception:
            if not reply['msg']:
                reply['msg'] = 'Something went wrong while creating joints on curve: {}'.format(traceback.format_exc())
            reply['success'] = False

    def snap_joints_to_curve(self, data, reply):
        joints = data['joints']
        curve = data['curve']
        num_joints = data['num_joints']

        try:
            result = joint.snap_joints_to_curve(joints, curve, num_joints)
            reply.update(result)
        except Exception:
            if not reply['msg']:
                reply['msg'] = 'Something went wrong while snapping joints to curve: {}'.format(traceback.format_exc())
            reply['success'] = False

    def toggle_local_rotation_axis(self, data, reply):
        joints = data['joints']

        try:
            result = joint.toggle_local_rotation_axis(joints)
            reply.update(result)
        except Exception:
            if not reply['msg']:
                reply['msg'] = 'Something went wrong while toggling joints LRA: {}'.format(traceback.format_exc())
            reply['success'] = False

    def toggle_all_local_rotation_axis(self, data, reply):

        flag = data.get('flag', None)

        try:
            result = joint.toggle_all_local_rotation_axis(flag=flag)
            reply.update(result)
        except Exception:
            if not reply['msg']:
                reply['msg'] = 'Something went wrong while toggling all joints LRA: {}'.format(traceback.format_exc())
            reply['success'] = False

    def toggle_selected_local_rotation_axis(self, data, reply):

        flag = data.get('flag', None)

        try:
            result = joint.toggle_selected_local_rotation_axis(flag=flag)
            reply.update(result)
        except Exception:
            if not reply['msg']:
                reply['msg'] = 'Something went wrong while toggling selected joints LRA: {}'.format(
                    traceback.format_exc())
            reply['success'] = False

    def toggle_joints_xray(self, data, reply):
        try:
            result = joint.toggle_joints_xray()
            reply.update(result)
        except Exception:
            if not reply['msg']:
                reply['msg'] = 'Something went wrong while toggling joints X-Ray: {}'.format(traceback.format_exc())
            reply['success'] = False

    def set_joints_xray(self, data, reply):
        flag = data.get('flag', None)

        try:
            result = joint.set_joints_xray(flag=flag)
            reply.update(result)
        except Exception:
            if not reply['msg']:
                reply['msg'] = 'Something went wrong while setting joints X-Ray: {}'.format(traceback.format_exc())
            reply['success'] = False

    def set_joints_display_size(self, data, reply):
        value = data.get('value', None)

        try:
            result = joint.set_joints_display_size(value=value)
            reply.update(result)
        except Exception:
            if not reply['msg']:
                reply['msg'] = 'Something went wrong while setting joints display size: {}'.format(
                    traceback.format_exc())
            reply['success'] = False

    def select_hierarchy(self, data, reply):
        try:
            result = joint.select_hierarchy()
            reply.update(result)
        except Exception:
            if not reply['msg']:
                reply['msg'] = 'Something went wrong while selecting joints hierarchy: {}'.format(
                    traceback.format_exc())
            reply['success'] = False

    def orient_joints(self, data, reply):
        try:
            result = joint.orient_joints()
            reply.update(result)
        except Exception:
            if not reply['msg']:
                reply['msg'] = 'Something went wrong while orienting joints: {}'.format(
                    traceback.format_exc())
            reply['success'] = False

    def orient_all_joints(self, data, reply):
        try:
            result = joint.orient_all_joints()
            reply.update(result)
        except Exception:
            if not reply['msg']:
                reply['msg'] = 'Something went wrong while orienting all scene joints: {}'.format(
                    traceback.format_exc())
            reply['success'] = False

    def orient_selected_joints(self, data, reply):
        try:
            result = joint.orient_selected_joints()
            reply.update(result)
        except Exception:
            if not reply['msg']:
                reply['msg'] = 'Something went wrong while orienting selected joints: {}'.format(
                    traceback.format_exc())
            reply['success'] = False

    def add_orient_data(self, data, reply):
        try:
            result = joint.add_orient_data()
            reply.update(result)
        except Exception:
            if not reply['msg']:
                reply['msg'] = 'Something went wrong while adding orient data joints: {}'.format(
                    traceback.format_exc())
            reply['success'] = False

    def add_orient_data_all_joints(self, data, reply):
        try:
            result = joint.orient_all_joints()
            reply.update(result)
        except Exception:
            if not reply['msg']:
                reply['msg'] = 'Something went wrong while adding orient data to all scene joints: {}'.format(
                    traceback.format_exc())
            reply['success'] = False

    def add_orient_data_selected_joints(self, data, reply):
        try:
            result = joint.orient_selected_joints()
            reply.update(result)
        except Exception:
            if not reply['msg']:
                reply['msg'] = 'Something went wrong while adding orient data to selected joints: {}'.format(
                    traceback.format_exc())
            reply['success'] = False

    def clean_orient_data(self, data, reply):
        try:
            result = joint.clean_orient_data()
            reply.update(result)
        except Exception:
            if not reply['msg']:
                reply['msg'] = 'Something went wrong while cleaning orient data from joints: {}'.format(
                    traceback.format_exc())
            reply['success'] = False

    def clean_orient_data_all_joints(self, data, reply):
        try:
            result = joint.clean_orient_data_all_joints()
            reply.update(result)
        except Exception:
            if not reply['msg']:
                reply['msg'] = 'Something went wrong while cleaning orient data from scene joints: {}'.format(
                    traceback.format_exc())
            reply['success'] = False

    def clean_orient_data_selected_joints(self, data, reply):
        try:
            result = joint.clean_orient_data_selected_joints()
            reply.update(result)
        except Exception:
            if not reply['msg']:
                reply['msg'] = 'Something went wrong while cleaning orient data from selected joints: {}'.format(
                    traceback.format_exc())
            reply['success'] = False

    def zero_joint_orient(self, data, reply):
        try:
            result = joint.zero_joint_orient()
            reply.update(result)
        except Exception:
            if not reply['msg']:
                reply['msg'] = 'Something went wrong while zeroing out orient of joints: {}'.format(
                    traceback.format_exc())
            reply['success'] = False

    def zero_joint_orient_all_joints(self, data, reply):
        try:
            result = joint.zero_joint_orient_all_joints()
            reply.update(result)
        except Exception:
            if not reply['msg']:
                reply['msg'] = 'Something wrong while zeroing out orient of all joints in current scene: {}'.format(
                    traceback.format_exc())
            reply['success'] = False

    def zero_joint_orient_selected_joints(self, data, reply):
        try:
            result = joint.zero_joint_orient_selected_joints()
            reply.update(result)
        except Exception:
            if not reply['msg']:
                reply['msg'] = 'Something went wrong while zeroing out orient of selected joints: {}'.format(
                    traceback.format_exc())
            reply['success'] = False

    def mirror_joints(self, data, reply):
        try:
            result = joint.mirror_joints()
            reply.update(result)
        except Exception:
            if not reply['msg']:
                reply['msg'] = 'Something went wrong while mirroring joints: {}'.format(
                    traceback.format_exc())
            reply['success'] = False

    def mirror_all_joints(self, data, reply):
        try:
            result = joint.mirror_all_joints()
            reply.update(result)
        except Exception:
            if not reply['msg']:
                reply['msg'] = 'Something went wrong while mirroring all joints in current scene: {}'.format(
                    traceback.format_exc())
            reply['success'] = False

    def mirror_selected_joints(self, data, reply):
        try:
            result = joint.mirror_selected_joints()
            reply.update(result)
        except Exception:
            if not reply['msg']:
                reply['msg'] = 'Something went wrong while mirroring selected joints: {}'.format(
                    traceback.format_exc())
            reply['success'] = False

    def mirror_hierarchy_joints(self, data, reply):
        try:
            result = joint.mirror_hierarchy_joints()
            reply.update(result)
        except Exception:
            if not reply['msg']:
                reply['msg'] = 'Something went wrong while mirroring hierarchy joints: {}'.format(
                    traceback.format_exc())
            reply['success'] = False

    # =================================================================================================================
    # SKINNING
    # =================================================================================================================

    def smooth_bind_skin(self, data, reply):

        geo_node = data['geo_node']
        show_options = data['show_options']

        try:
            result = skin.apply_smooth_bind_skin(geo=geo_node, show_options=show_options)
            reply.update(result)
        except Exception:
            if not reply['msg']:
                reply['msg'] = 'Something went wrong while applying smooth bind skin: {}'.format(traceback.format_exc())
            reply['success'] = False

    def rigid_bind_skin(self, data, reply):

        geo_node = data['geo_node']
        show_options = data['show_options']

        try:
            result = skin.apply_rigid_skin(geo=geo_node, show_options=show_options)
            reply.update(result)
        except Exception:
            if not reply['msg']:
                reply['msg'] = 'Something went wrong while applying rigid bind skin: {}'.format(traceback.format_exc())
            reply['success'] = False

    def detach_bind_skin(self, data, reply):

        geo_node = data['geo_node']
        show_options = data['show_options']

        try:
            result = skin.detach_bind_skin(geo=geo_node, show_options=show_options)
            reply.update(result)
        except Exception:
            if not reply['msg']:
                reply['msg'] = 'Something went wrong while detaching bind skin: {}'.format(traceback.format_exc())
            reply['success'] = False

    def open_paint_skin_weights_tool(self, data, reply):

        show_options = data['show_options']

        try:
            result = skin.open_pain_skin_weights_tool(show_options=show_options)
            reply.update(result)
        except Exception:
            if not reply['msg']:
                reply['msg'] = 'Something went wrong while opening skin weights paint tool: {}'.format(
                    traceback.format_exc())
            reply['success'] = False

    def check_joints_labels(self, data, reply):

        joints = data['joints']

        try:
            result = joint.check_joint_labels(joints=joints)
            reply.update(result)
        except Exception:
            if not reply['msg']:
                reply['msg'] = 'Something went wrong while checking joints label: {}'.format(
                    traceback.format_exc())
            reply['success'] = False

    def mirror_skin_weights(self, data, reply):

        mesh = data['mesh']
        auto_assign_labels = data['auto_assign_labels']
        left_side_label = data['left_side_label']
        right_side_label = data['right_side_label']
        show_options = data['show_options']

        try:
            result = skin.mirror_skin_weights(
                mesh=mesh, auto_assign_labels=auto_assign_labels, left_side_label=left_side_label,
                right_side_label=right_side_label, show_options=show_options)
            reply.update(result)
        except Exception:
            if not reply['msg']:
                reply['msg'] = 'Something went wrong while mirroring skin weights: {}'.format(traceback.format_exc())
            reply['success'] = False

    def copy_skin_weights(self, data, reply):

        source_mesh = data['source_mesh']
        target_mesh = data['target_mesh']
        auto_assign_labels = data['auto_assign_labels']
        left_side_label = data['left_side_label']
        right_side_label = data['right_side_label']
        show_options = data['show_options']

        try:
            result = skin.copy_skin_weights(
                source_mesh=source_mesh, target_mesh=target_mesh, auto_assign_labels=auto_assign_labels,
                left_side_label=left_side_label, right_side_label=right_side_label, show_options=show_options)
            reply.update(result)
        except Exception:
            if not reply['msg']:
                reply['msg'] = 'Something went wrong while copying skin weights: {}'.format(traceback.format_exc())
            reply['success'] = False

    def prune_skin_weights(self, data, reply):
        show_options = data['show_options']
        mesh = data['mesh']

        try:
            result = skin.prune_skin_weights(geo=mesh, show_options=show_options)
            reply.update(result)
        except Exception:
            if not reply['msg']:
                reply['msg'] = 'Something went wrong while pruning skin weights: {}'.format(traceback.format_exc())
            reply['success'] = False

    def transfer_skin_uvs(self, data, reply):

        source_mesh = data['source_mesh']
        target_mesh = data['target_mesh']
        auto_assign_labels = data['auto_assign_labels']
        left_side_label = data['left_side_label']
        right_side_label = data['right_side_label']

        try:
            result = skin.transfer_uvs_to_skinned_geometry(
                source_mesh=source_mesh, target_mesh=target_mesh, auto_assign_labels=auto_assign_labels,
                left_side_label=left_side_label, right_side_label=right_side_label)
            reply.update(result)
        except Exception:
            if not reply['msg']:
                reply['msg'] = 'Something went wrong while transferring UVs to skinned geometry: {}'.format(
                    traceback.format_exc())
            reply['success'] = False

    def clean_skinned_mesh(self, data, reply):
        mesh = data['mesh']
        auto_assign_labels = data['auto_assign_labels']
        left_side_label = data['left_side_label']
        right_side_label = data['right_side_label']

        try:
            result = skin.freeze_skinned_mesh(
                mesh, auto_assign_labels=auto_assign_labels, left_side_label=left_side_label,
                right_side_label=right_side_label)
            reply.update(result)
        except Exception:
            if not reply['msg']:
                reply['msg'] = 'Something went wrong while cleaning skinned geometry: {}'.format(
                    traceback.format_exc())
            reply['success'] = False

    def combine_skinned_meshes(self, data, reply):
        meshes = data['meshes']

        try:
            result = skin.combine_skinned_meshes(meshes)
            reply.update(result)
        except Exception:
            if not reply['msg']:
                reply['msg'] = 'Something went wrong while combining skinned meshes: {}'.format(
                    traceback.format_exc())
            reply['success'] = False

    def extract_skinned_selected_faces(self, data, reply):
        components = data['components']
        auto_assign_labels = data['auto_assign_labels']
        left_side_label = data['left_side_label']
        right_side_label = data['right_side_label']

        try:
            result = skin.extract_skinned_selected_components(
                components, auto_assign_labels=auto_assign_labels, left_side_label=left_side_label,
                right_side_label=right_side_label)
            reply.update(result)
        except Exception:
            if not reply['msg']:
                reply['msg'] = 'Something went wrong while extracting skinned selected faces: {}'.format(
                    traceback.format_exc())
            reply['success'] = False

    def remove_unused_influences(self, data, reply):
        mesh = data['mesh']

        try:
            result = skin.delete_unused_influences(mesh)
            reply.update(result)
        except Exception:
            if not reply['msg']:
                reply['msg'] = 'Something went wrong while removing unused influences: {}'.format(
                    traceback.format_exc())
            reply['success'] = False

    def restore_bind_pose(self, data, reply):
        mesh = data['mesh']

        try:
            result = skin.restore_to_bind_pose(mesh)
            reply.update(result)
        except Exception:
            if not reply['msg']:
                reply['msg'] = 'Something went wrong while restoring bind pose: {}'.format(traceback.format_exc())
            reply['success'] = False

    def remove_bind_poses(self, data, reply):

        try:
            result = skin.remove_bind_poses()
            reply.update(result)
        except Exception:
            if not reply['msg']:
                reply['msg'] = 'Something went wrong while removing all bind poses from current scene: {}'.format(
                    traceback.format_exc())
            reply['success'] = False

    def weights_hammer(self, data, reply):

        vertices_to_hammer = data['vertices_to_hammer']

        try:
            result = skin.hammer_vertices(vertices_to_hammer)
            reply.update(result)
        except Exception:
            if not reply['msg']:
                reply['msg'] = 'Something went wrong while hammering weights: {}'.format(
                    traceback.format_exc())
            reply['success'] = False

    def average_vertex_weights(self, data, reply):
        components = data['components'] or dcc.selected_nodes_in_order(flatten=True)
        use_distance = data['use_distance']
        curve_weight_points = data['curve_weight_points']

        try:
            result = skin.average_vertices_weights(
                components, use_distance=use_distance, curve_weight_points=curve_weight_points)
            reply.update(result)
        except Exception:
            if not reply['msg']:
                reply['msg'] = 'Something went wrong while averaging vertex weights: {}'.format(traceback.format_exc())
            reply['success'] = False

    def move_skin_weights(self, data, reply):

        try:
            result = skin.move_skin_weights()
            reply.update(result)
        except Exception:
            if not reply['msg']:
                reply['msg'] = 'Something went wrong while moving skinning weights: {}'.format(traceback.format_exc())
            reply['success'] = False

    def swap_skin_weights(self, data, reply):

        try:
            result = skin.swap_skin_weights()
            reply.update(result)
        except Exception:
            if not reply['msg']:
                reply['msg'] = 'Something went wrong while moving skinning weights: {}'.format(traceback.format_exc())
            reply['success'] = False

    def select_influences(self, data, reply):

        try:
            result = skin.select_influencing_joints()
            reply.update(result)
        except Exception:
            if not reply['msg']:
                reply['msg'] = 'Something went wrong while selecting influences {}'.format(traceback.format_exc())
            reply['success'] = False

    def select_influence_components(self, data, reply):

        influence_joints = data['influence_joints']
        mesh_node = data['mesh_node']

        success = skin.select_influence_components(joint_nodes=influence_joints, mesh_name=mesh_node)

        reply['success'] = success

    def delete_influences(self, data, reply):

        mesh_nodes = data['mesh_nodes']
        influences_to_remove = data['influences_to_remove']
        fast_delete = data['fast_delete']

        success = skin.delete_influences(
            skinned_objects=mesh_nodes, influences_to_remove=influences_to_remove, fast=fast_delete)

        reply['success'] = success

    def br_smooth_weights(self, data, reply):

        options = data.get('options', False)

        success = skin.br_smooth_weights_options() if options else skin.br_smooth_weights()

        reply['success'] = success

    def br_transfer_weights(self, data, reply):

        options = data.get('options', False)

        success = skin.br_smooth_weights_options() if options else skin.br_transfer_weights()

        reply['success'] = success

    def ng_skin_tools(self, data, reply):

        success = skin.ng_skin_tools()

        reply['success'] = success

    def load_plugins(self, data, reply):

        do_reload = data['do_reload']

        plugins_path = path_utils.clean_path(os.path.join(os.path.abspath(os.path.dirname(__file__)), 'plugins'))
        if not os.path.isdir(plugins_path):
            reply['msg'] = 'Impossible to load tpRigToolkit-tools-rigtoolbox Maya plugins because plugin ' \
                           'folder was not found: "{}"'.format(plugins_path)
            reply['success'] = False
            return

        # Update Maya Plugin paths
        maya_plugin_path = os.getenv('MAYA_PLUG_IN_PATH', None)
        if not maya_plugin_path:
            os.environ['MAYA_PLUG_IN_PATH'] = plugins_path
        else:
            path_already_added = False
            current_plugin_paths = os.environ['MAYA_PLUG_IN_PATH'].split(os.pathsep)
            for current_plugin_path in current_plugin_paths:
                if path_utils.clean_path(current_plugin_path) == plugins_path:
                    path_already_added = True
                    break
            if not path_already_added:
                os.environ['MAYA_PLUG_IN_PATH'] = '{}{}{}'.format(
                    os.environ['MAYA_PLUG_IN_PATH'], os.pathsep, plugins_path)

        # Load plugins
        for plugin_file in os.listdir(plugins_path):
            if not plugin_file:
                continue
            plugin_ext = os.path.splitext(plugin_file)[-1]
            if not plugin_ext == '.py':
                continue
            plugin_path = path_utils.clean_path(os.path.join(plugins_path, plugin_file))
            if do_reload:
                if helpers.is_plugin_loaded(plugin_path):
                    helpers.unload_plugin(plugin_path)
            helpers.load_plugin(plugin_path)

        reply['success'] = True
