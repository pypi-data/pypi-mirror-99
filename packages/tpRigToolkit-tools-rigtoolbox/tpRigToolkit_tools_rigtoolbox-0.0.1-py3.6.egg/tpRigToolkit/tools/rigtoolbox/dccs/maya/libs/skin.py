#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""
Module that contains library with skinning related functions
"""

from __future__ import print_function, division, absolute_import

import logging
import cStringIO
import traceback

import maya.cmds
import maya.mel

from tpDcc import dcc
from tpDcc.libs.python import python, kdtree, bezier

from tpDcc.dccs.maya.api import skin as api_skin, mathlib as api_mathlib
from tpDcc.dccs.maya.core import decorators, geometry as geo_utils, mesh as mesh_utils, joint as joint_utils
from tpDcc.dccs.maya.core import skin as skin_utils

from tpRigToolkit.tools.rigtoolbox.widgets import library

LOGGER = logging.getLogger('tpRigToolkit-tools-rigtoolbox')


@decorators.undo
@decorators.repeat_static_command(__name__, skip_arguments=True)
def apply_smooth_bind_skin(geo=None, show_options=False):
    """
    Initializes joint tool
    """

    out_dict = {'success': False, 'result': None}

    geo_nodes = geo or dcc.selected_nodes_of_type(node_type='transform')
    geo_nodes = python.force_list(geo_nodes)
    valid_geo_nodes = list()
    for geo_node in geo_nodes:
        if not mesh_utils.is_a_mesh(geo_node):
            continue
        valid_geo_nodes.append(geo_node)
    if not valid_geo_nodes:
        out_dict['msg'] = 'No meshes to apply smooth bind skin into found.'
        return out_dict

    try:
        result = skin_utils.apply_smooth_bind(geo=valid_geo_nodes, show_options=show_options)
        out_dict['result'] = result
    except Exception as exc:
        out_dict['msg'] = 'Was not possible to apply smooth bind skin: {}'.format(exc)
        return out_dict

    out_dict['success'] = True

    return out_dict


@decorators.undo
@decorators.repeat_static_command(__name__, skip_arguments=True)
def apply_rigid_skin(geo=None, show_options=False):

    out_dict = {'success': False, 'result': None}

    geo_nodes = geo or dcc.selected_nodes_of_type(node_type='transform')
    geo_nodes = python.force_list(geo_nodes)
    valid_geo_nodes = list()
    for geo_node in geo_nodes:
        if not mesh_utils.is_a_mesh(geo_node):
            continue
        valid_geo_nodes.append(geo_node)
    if not valid_geo_nodes:
        out_dict['msg'] = 'No meshes to apply rigid bind skin into found.'
        return out_dict

    try:
        result = skin_utils.apply_rigid_skin(geo=valid_geo_nodes, show_options=show_options)
        out_dict['result'] = result
    except Exception as exc:
        out_dict['msg'] = 'Was not possible to apply smooth bind skin: {}'.format(exc)
        return out_dict

    out_dict['success'] = True

    return out_dict


@decorators.undo
@decorators.repeat_static_command(__name__, skip_arguments=True)
def detach_bind_skin(geo=None, show_options=False):

    out_dict = {'success': False, 'result': list()}

    geo_nodes = geo or dcc.selected_nodes_of_type(node_type='transform')
    geo_nodes = python.force_list(geo_nodes)
    valid_geo_nodes = list()
    for geo_node in geo_nodes:
        if not mesh_utils.is_a_mesh(geo_node):
            continue
        valid_geo_nodes.append(geo_node)
    if not valid_geo_nodes:
        out_dict['msg'] = 'No meshes to apply rigid bind skin into found.'
        return out_dict

    try:
        result = skin_utils.detach_bind_skin(geo=valid_geo_nodes, show_options=show_options)
        out_dict['result'].append(result)
    except Exception as exc:
        out_dict['msg'] = 'Was not possible to apply smooth bind skin: {}'.format(exc)
        return out_dict

    out_dict['success'] = True

    return out_dict


@decorators.undo
@decorators.repeat_static_command(__name__, skip_arguments=True)
def open_pain_skin_weights_tool(show_options=False):

    out_dict = {'success': False, 'result': None}

    try:
        result = skin_utils.open_pain_skin_weights_tool(show_options=show_options)
        out_dict['result'] = result
    except Exception as exc:
        out_dict['msg'] = 'Was not possible to apply smooth bind skin: {}'.format(exc)
        return out_dict

    out_dict['success'] = True

    return out_dict


@decorators.undo
@decorators.repeat_static_command(__name__, skip_arguments=True)
def mirror_skin_weights(mesh=None, show_options=False, **kwargs):

    out_dict = {'success': False, 'result': None}

    transforms = mesh or dcc.selected_nodes_of_type('transform')
    transforms = python.force_list(transforms)
    if not transforms:
        out_dict['msg'] = 'No meshes to mirror skin weights of found.'
        return out_dict

    try:
        result = skin_utils.mirror_skin_weights(mesh=mesh, show_options=show_options, **kwargs)
        out_dict['result'] = result
    except Exception as exc:
        out_dict['msg'] = 'Was not possible to mirror skin weights: {}'.format(exc)
        return out_dict

    out_dict['success'] = True

    return out_dict


@decorators.undo
@decorators.repeat_static_command(__name__, skip_arguments=True)
def copy_skin_weights(source_mesh=None, target_mesh=None, show_options=False, **kwargs):

    out_dict = {'success': False, 'result': None}

    selection = dcc.selected_nodes_of_type('transform')
    source_transform = source_mesh or (selection[0] if python.index_exists_in_list(selection, 1) else None)
    target_transform = target_mesh or (selection[1] if python.index_exists_in_list(selection, 1) else None)
    if not source_transform or not target_transform:
        out_dict['msg'] = 'Select source mesh and target mesh before executing Copy Skin Weights.'
        return out_dict

    try:
        result = skin_utils.copy_skin_weights(
            source_mesh=source_mesh, target_mesh=target_mesh, show_options=show_options, **kwargs)
        out_dict['result'] = result
    except Exception as exc:
        out_dict['msg'] = 'Was not possible to copy skin weights: {}'.format(exc)
        return out_dict

    out_dict['success'] = True

    return out_dict


@decorators.undo
@decorators.repeat_static_command(__name__, skip_arguments=True)
def prune_skin_weights(mesh=None, show_options=False, **kwargs):

    out_dict = {'success': False, 'result': None}

    transforms = mesh or dcc.selected_nodes_of_type('transform')
    transforms = python.force_list(transforms)
    if not transforms:
        out_dict['msg'] = 'No meshes to prune skin weights of found.'
        return out_dict

    try:
        result = skin_utils.prune_skin_weights(mesh=mesh, show_options=show_options, **kwargs)
        out_dict['result'] = result
    except Exception as exc:
        out_dict['msg'] = 'Was not possible to prune skin weights: {}'.format(exc)
        return out_dict

    out_dict['success'] = True

    return out_dict


@decorators.undo
@decorators.repeat_static_command(__name__, skip_arguments=True)
def transfer_uvs_to_skinned_geometry(source_mesh=None, target_mesh=None, use_intermediate_shape=False, **kwargs):

    out_dict = {'success': False, 'result': None}

    selection = dcc.selected_nodes_of_type('transform')
    source_transform = source_mesh or (selection[0] if python.index_exists_in_list(selection, 0) else None)
    target_transform = target_mesh or (selection[1] if python.index_exists_in_list(selection, 1) else None)
    if not source_transform or not target_transform:
        out_dict['msg'] = 'Select source mesh and target mesh before executing Transfers UVs to skinned geometry.'
        return out_dict

    try:
        result = skin_utils.transfer_uvs_to_skinned_geometry(
            source_mesh=source_mesh, target_mesh=target_mesh, use_intermediate_shape=use_intermediate_shape, **kwargs)
        out_dict['result'] = result
    except Exception as exc:
        out_dict['msg'] = 'Was not possible to transfers UVs to skinned geometry: {}'.format(exc)
        return out_dict

    out_dict['success'] = True

    return out_dict


@decorators.undo
@decorators.repeat_static_command(__name__, skip_arguments=True)
def freeze_skinned_mesh(skinned_mesh, **kwargs):

    out_dict = {'success': False, 'result': list()}

    meshes = skinned_mesh or dcc.selected_nodes_of_type('transform')
    meshes = python.force_list(meshes)
    if not meshes:
        return False

    if kwargs.pop('auto_assign_labels', False):
        joint_utils.auto_assign_labels_to_mesh_influences(
            meshes, input_left=kwargs.pop('left_side_label', None),
            input_right=kwargs.pop('right_side_label', None), check_labels=True)

    percentage = 100.0 / len(meshes)

    for i, mesh in enumerate(meshes):
        library.Command.progressCommand.emit(percentage * (i + 1), 'Cleaning Skinned Mesh: {}'.format(mesh))
        try:
            skin_cluster_name = skin_utils.find_related_skin_cluster(mesh)
            if not skin_cluster_name:
                continue
            attached_joints = maya.cmds.skinCluster(skin_cluster_name, query=True, inf=True)
            mesh_shape_name = maya.cmds.listRelatives(mesh, shapes=True)[0]
            out_influences_array = api_skin.get_skin_weights(skin_cluster_name, mesh_shape_name)
            maya.cmds.skinCluster(mesh_shape_name, edit=True, unbind=True)
            maya.cmds.delete(mesh, ch=True)
            maya.cmds.makeIdentity(mesh, apply=True)
            new_skin_cluster_name = maya.cmds.skinCluster(
                attached_joints, mesh, toSelectedBones=True, bindMethod=0, normalizeWeights=True)[0]
            api_skin.set_skin_weights(new_skin_cluster_name, mesh_shape_name, out_influences_array)
            out_dict['result'].append(mesh)
        except Exception as exc:
            out_dict['msg'] = 'Was not possible to freeze skinned meshes: "{}" | {}'.format(meshes, exc)
            return out_dict

    dcc.select_node(meshes)

    out_dict['success'] = True

    return out_dict


@decorators.undo
@decorators.repeat_static_command(__name__, skip_arguments=True)
def combine_skinned_meshes(meshes=None):

    out_dict = {'success': False, 'result': None}

    meshes = meshes or dcc.selected_nodes_of_type('transform')
    if not meshes:
        out_dict['msg'] = 'No meshes to combine found.'
        return out_dict

    try:
        result = skin_utils.combine_skinned_meshes(meshes)
        out_dict['result'] = result
    except Exception as exc:
        out_dict['msg'] = 'Was not possible to transfers UVs to skinned geometry: {}'.format(exc)
        return out_dict

    out_dict['success'] = True

    return out_dict


@decorators.undo
@decorators.repeat_static_command(__name__, skip_arguments=True)
def extract_skinned_selected_components(selected_components=None, **kwargs):

    out_dict = {'success': False, 'result': None}

    components = selected_components or dcc.selected_nodes(flatten=True)
    components = python.force_list(components)
    if not components:
        out_dict['msg'] = 'No components to extract from found.'
        return out_dict

    try:
        result = skin_utils.extract_skinned_selected_components(components, **kwargs)
        out_dict['result'] = result
    except Exception as exc:
        out_dict['msg'] = 'Was not possible to transfers UVs to skinned geometry: {}'.format(exc)
        return out_dict

    out_dict['success'] = True

    return out_dict


@decorators.undo
@decorators.repeat_static_command(__name__, skip_arguments=True)
def delete_unused_influences(skinned_objects=None):

    out_dict = {'success': False, 'result': list()}

    skinned_objects = skinned_objects or dcc.selected_nodes()
    skinned_objects = python.force_list(skinned_objects)
    if not skinned_objects:
        out_dict['msg'] = 'No components to extract from found.'
        return out_dict

    percentage = 100.0 / len(skinned_objects)

    for i, mesh in enumerate(skinned_objects):
        try:
            library.Command.progressCommand.emit(percentage * (i + 1), 'Deleting unused influences: {}'.format(mesh))
            skin_cluster_name = skin_utils.find_related_skin_cluster(mesh)
            if not skin_cluster_name:
                shape = maya.cmds.listRelatives(mesh, shapes=True) or None
                if shape:
                    LOGGER.warning(
                        'Impossible to delete unused influences because mesh "{}" '
                        'has no skin cluster attached to it!'.format(mesh))
                continue

            attached_joints = maya.cmds.skinCluster(skin_cluster_name, query=True, influence=True)
            weighted_joints = maya.cmds.skinCluster(skin_cluster_name, query=True, weightedInfluence=True)

            non_influenced = list()
            for attached in attached_joints:
                if attached in weighted_joints:
                    continue
                non_influenced.append(attached)

            for joint in non_influenced:
                maya.cmds.skinCluster(skin_cluster_name, edit=True, removeInfluence=joint)
            out_dict['result'].append(mesh)
        except Exception as exc:
            out_dict['msg'] = 'Was not possible to delete unused influences: "{}" | {}'.format(skinned_objects, exc)
            return out_dict

    return out_dict


@decorators.undo
@decorators.repeat_static_command(__name__, skip_arguments=True)
def restore_to_bind_pose(skinned_mesh=None):

    out_dict = {'success': False, 'result': None}

    skinned_meshes = skinned_mesh or dcc.selected_nodes_of_type('transform')
    skinned_meshes = python.force_list(skinned_meshes)
    if not skinned_meshes:
        skinned_meshes = list()
        meshes = dcc.list_nodes(node_type='mesh')
        for mesh in meshes:
            skinned_meshes.append(maya.cmds.listRelatives(mesh, parent=True)[0])
    if not skinned_meshes:
        out_dict['msg'] = 'No skinned meshes to restore bind poses of found.'
        return out_dict

    try:
        result = skin_utils.restore_to_bind_pose(skinned_mesh)
        out_dict['result'] = result
    except Exception as exc:
        out_dict['msg'] = 'Was not possible to restore skinned mesh to bind pose: {}'.format(exc)
        return out_dict

    out_dict['success'] = True

    return out_dict


@decorators.undo
@decorators.repeat_static_command(__name__, skip_arguments=True)
def remove_bind_poses():

    out_dict = {'success': False, 'result': None}

    try:
        result = skin_utils.remove_all_bind_poses_in_scene()
        out_dict['result'] = result
    except Exception as exc:
        out_dict['msg'] = 'Was not possible to remove all bind poses from current scene: {}'.format(exc)
        return out_dict

    out_dict['success'] = True

    return out_dict


def hammer_vertices(vertices_to_hammer=None, return_as_list=True):

    out_dict = {'success': False, 'result': None}

    try:
        result = skin_utils.hammer_vertices(vertices_to_hammer, return_as_list=return_as_list)
        out_dict['result'] = result
    except Exception as exc:
        out_dict['msg'] = 'Was not possible to hammer vertices: {}'.format(exc)
        return out_dict

    out_dict['success'] = True

    return out_dict


@decorators.undo
def average_vertices_weights(selection, use_distance, curve_weight_points=None):
    """
    Generates an average weight from all selected vertices to apply to the last selected vertex
    :param selection: list<Vertex>, list of vertices to average
    :param use_distance:
    :param curve_weight_points:
    :return:
    """

    out_dict = {'success': False, 'result': None}

    total_vertices = len(selection)
    if total_vertices < 2:
        out_dict['msg'] = 'Not enough vertices selected! Select a minimum of 2 vertices.'
        return out_dict

    obj = selection[0]
    if '.' in selection[0]:
        obj = selection[0].split('.')[0]

    is_edge_selection = False
    if '.e[' in selection[0]:
        is_edge_selection = True

    skin_cluster_name = skin_utils.find_related_skin_cluster(obj)
    maya.cmds.setAttr('{0}.envelope'.format(skin_cluster_name), 0)

    try:
        maya.cmds.skinCluster(obj, edit=True, normalizeWeights=True)
        if total_vertices == 2 or is_edge_selection:
            base_list = [selection]
            if is_edge_selection:
                base_list = mesh_utils.edges_to_smooth(edges_list=selection)

            percentage = 99.0 / len(base_list)

            for i, vert_list in enumerate(base_list):
                library.Command.progressCommand.emit(
                    percentage * (i + 1), 'Pass 1: Averaging vertex weights: {}'.format(i))

                start = vert_list[0]
                end = vert_list[-1]
                surface = start.split('.')[0]
                obj_type = maya.cmds.objectType(surface)
                if obj_type == 'transform':
                    shape = maya.cmds.listRelatives(surface, shapes=True)
                    if shape:
                        obj_type = maya.cmds.objectType(shape[0])

                poly = False
                if obj_type == 'mesh':
                    poly = True
                    order = mesh_utils.find_shortest_vertices_path_between_vertices(vert_list)
                    added = 0.0
                    amount = len(order) + 1
                    total_distance = api_mathlib.distance_between_nodes(order[-1], end)
                elif obj_type == 'nurbsSurface':
                    order, total_distance = geo_utils.find_shortest_path_between_surface_cvs(
                        vert_list, return_total_distance=True)
                    added = -2.0
                    amount = len(order) + 1
                elif obj_type == 'lattice':
                    order, total_distance = geo_utils.find_shortest_path_between_lattice_cvs(
                        vert_list, return_total_distance=True)
                    added = -2.0
                    amount = len(order) + 1
                else:
                    numbers = [int(start.split("[")[-1].split("]")[0]), int(end.split("[")[-1].split("]")[0])]
                    range_list = range(min(numbers), max(numbers) + 1)
                    amount = len(range_list)
                    added = -1.0
                    order = list()
                    total_distance = 0.0
                    for j, num in enumerate(range_list):
                        cv = '{}.cv[{}]'.format(surface, num)
                        order.append(cv)
                        if j == 0:
                            continue
                        total_distance += api_mathlib.distance_between_nodes(order[j - 1], cv)
                if not order:
                    return

                list_bone_influences = maya.cmds.skinCluster(obj, query=True, inf=True)
                weights_start = maya.cmds.skinPercent(skin_cluster_name, start, query=True, v=True)
                weights_end = maya.cmds.skinPercent(skin_cluster_name, end, query=True, v=True)

                lengths = list()
                if use_distance:
                    for j, vertex in enumerate(order):
                        if j == 0:
                            length = api_mathlib.distance_between_nodes(start, vertex)
                        else:
                            length = api_mathlib.distance_between_nodes(order[j - 1], vertex)
                        if poly:
                            total_distance += length
                        lengths.append(length)

                percentage = float(1.0) / (amount + added)
                current_length = 0.0

                for index, vertex in enumerate(order):
                    library.Command.progressCommand.emit(
                        percentage * (index + 1), 'Pass 2: Averaging vertex weights: {}'.format(index))
                    if use_distance:
                        current_length += lengths[index]
                        current_percentage = (current_length / total_distance)
                    else:
                        current_percentage = index * percentage
                        if poly:
                            current_percentage = (index + 1) * percentage
                    if curve_weight_points:
                        current_percentage = bezier.get_data_on_percentage(current_percentage, curve_weight_points)

                    new_weight_list = list()
                    for j, weight in enumerate(weights_start):
                        value1 = weights_end[j] * current_percentage
                        value2 = weights_start[j] * (1 - current_percentage)
                        new_weight_list.append((list_bone_influences[j], value1 + value2))

                    maya.cmds.skinPercent(skin_cluster_name, vertex, transformValue=new_weight_list)

                maya.cmds.select([start, end], r=True)

                maya.cmds.setAttr('{}.envelope'.format(skin_cluster_name), 1)
                maya.cmds.select(vert_list, replace=True)
                maya.cmds.refresh()
                library.Command.progressCommand.emit(
                    percentage * i, 'Pass 3: Updating skin cluster for vertex: {}'.format(i))
                maya.cmds.setAttr('{}.envelope'.format(skin_cluster_name), 0)
        else:
            last_selected = selection[-1]
            point_list = [x for x in selection if x != last_selected]
            mesh_name = last_selected.split('.')[0]

            list_joint_influences = maya.cmds.skinCluster(mesh_name, query=True, weightedInfluence=True)
            influence_size = len(list_joint_influences)

            temp_vertex_joints = list()
            temp_vertex_weights = list()
            for pnt in point_list:
                for jnt in range(influence_size):
                    point_weights = maya.cmds.skinPercent(
                        skin_cluster_name, pnt, transform=list_joint_influences[jnt], query=True, value=True)
                    if point_weights < 0.000001:
                        continue
                    temp_vertex_joints.append(list_joint_influences[jnt])
                    temp_vertex_weights.append(point_weights)

            total_values = 0.0
            average_values = list()
            clean_list = list()
            for i in temp_vertex_joints:
                if i not in clean_list:
                    clean_list.append(i)

            for i in range(len(clean_list)):
                working_value = 0.0
                for j in range(len(temp_vertex_joints)):
                    if not temp_vertex_joints[j] == clean_list[i]:
                        continue
                    working_value += temp_vertex_weights[j]
                num_points = len(point_list)
                average_values.append(working_value / num_points)
                total_values += average_values[i]

            summary = 0
            for value in range(len(average_values)):
                temp_value = average_values[value] / total_values
                average_values[value] = temp_value
                summary += average_values[value]

            cmd = cStringIO.StringIO()
            cmd.write('maya.cmds.skinPercent("%s","%s", transformValue=[' % (skin_cluster_name, last_selected))

            for count, skin_joint in enumerate(clean_list):
                cmd.write('("%s", %s)' % (skin_joint, average_values[count]))
                if not count == len(clean_list) - 1:
                    cmd.write(', ')
            cmd.write('])')
            eval(cmd.getvalue())
    except Exception:
        out_dict['msg'] = 'Was not possible to average vertex weights: {}'.format(traceback.format_exc())
        maya.cmds.setAttr('{}.envelope'.format(skin_cluster_name), 1)
        return out_dict
    finally:
        maya.cmds.setAttr('{}.envelope'.format(skin_cluster_name), 1)

    out_dict['success'] = True

    return out_dict


@decorators.undo
@decorators.repeat_static_command(__name__, skip_arguments=True)
def move_skin_weights(source_joint=None, target_joint=None, mesh=None):

    out_dict = {'success': False, 'result': None}

    selection = dcc.selected_nodes()
    source_joint = source_joint or (selection[0] if python.index_exists_in_list(selection, 0) else None)
    if not source_joint:
        out_dict['msg'] = 'No source joint found to move skin weights from.'
        return out_dict

    target_joint = target_joint or (selection[1] if python.index_exists_in_list(selection, 1) else None)
    if not target_joint:
        out_dict['msg'] = 'No target joint found to move skin weights to.'
        return out_dict

    mesh = mesh or (selection[2] if python.index_exists_in_list(selection, 2) else None)
    if not mesh:
        out_dict['msg'] = 'No mesh with skinning information found'
        return out_dict

    try:
        result = skin_utils.move_skin_weights(source_joint, target_joint, mesh)
        out_dict['result'] = result
    except Exception as exc:
        out_dict['msg'] = 'Was not possible to move skin weights: {}'.format(exc)
        return out_dict

    out_dict['success'] = True

    return out_dict


@decorators.undo
@decorators.repeat_static_command(__name__, skip_arguments=True)
def swap_skin_weights(source_joint=None, target_joint=None, mesh=None):

    out_dict = {'success': False, 'result': None}

    selection = dcc.selected_nodes()
    source_joint = source_joint or (selection[0] if python.index_exists_in_list(selection, 0) else None)
    if not source_joint:
        out_dict['msg'] = 'No source joint found to swap skin weights from.'
        return out_dict

    target_joint = target_joint or (selection[1] if python.index_exists_in_list(selection, 1) else None)
    if not target_joint:
        out_dict['msg'] = 'No target joint found to swap skin weights to.'
        return out_dict

    mesh = mesh or (selection[2] if python.index_exists_in_list(selection, 2) else None)
    if not mesh:
        out_dict['msg'] = 'No mesh with skinning information found'
        return out_dict

    try:
        result = skin_utils.swap_skin_weights(source_joint, target_joint, mesh)
        out_dict['result'] = result
    except Exception as exc:
        out_dict['msg'] = 'Was not possible to swap skin weights: {}'.format(exc)
        return out_dict

    out_dict['success'] = True

    return out_dict


@decorators.undo
@decorators.repeat_static_command(__name__, skip_arguments=True)
def select_influencing_joints(mesh_node=None):

    out_dict = {'success': False, 'result': None}

    mesh_nodes = mesh_node or dcc.selected_nodes_of_type(node_type='transform')
    mesh_nodes = python.force_list(mesh_nodes)
    mesh_node = mesh_nodes[0] if mesh_nodes else None
    if not mesh_node:
        out_dict['msg'] = 'No mesh selected to retrieve influences of'
        return out_dict

    try:
        result = skin_utils.select_influencing_joints(mesh_node)
        out_dict['result'] = result
    except Exception as exc:
        out_dict['msg'] = 'Was not possible to select influencing joints: {}'.format(exc)
        return out_dict

    out_dict['success'] = True

    return out_dict


@decorators.undo
@decorators.repeat_static_command(__name__, skip_arguments=True)
def select_influence_components(joint_nodes=None, mesh_node=None):

    out_dict = {'success': False, 'result': None}

    try:
        result = skin_utils.select_influence_vertices(joint_nodes=joint_nodes, mesh_node=mesh_node)
        out_dict['result'] = result
    except Exception as exc:
        out_dict['msg'] = 'Was not possible to select influencing joints: {}'.format(exc)
        return out_dict

    out_dict['success'] = True

    return out_dict


@decorators.undo
@decorators.repeat_static_command(__name__, skip_arguments=True)
def delete_influences(skinned_objects=None, influences_to_remove=None, fast=True):
    """
    Deletes given influences from given meshes and stores the unbind influences weights into other influences
    :param skinned_objects: list(str), meshes which joints need to be removed
    :param influences_to_remove: list(str), list of joints that need to be removed
    :param fast: list(str), bool, Whether to do the deletion using quick unbind method or not
    :return: bool
    """

    if fast:
        valid_deletion = unbind_influences_quick(
            skinned_objects=skinned_objects, influences_to_unbind=influences_to_remove, delete=True)
    else:
        valid_deletion = unbind_influences(
            skinned_objects=skinned_objects, influences_to_unbind=influences_to_remove, delete=True
        )

    return valid_deletion


@decorators.undo
def unbind_influences_quick(skinned_objects=None, influences_to_unbind=None, delete=False):
    """
    Unbind given influences from given meshes and stores the unbind influences weights into other influences
    The weights reassignation is handled by Maya
    :param skinned_objects: list(str), meshes which joints need to be removed
    :param influences_to_unbind: list(str), list of joints that need to be unbind
    :param delete: bool, Whether or not to delete unbind influences after unbind process is completed
    :return: bool
    """

    selected_transforms = dcc.selected_nodes_of_type('transform')
    selected_joints = dcc.selected_nodes_of_type('joint')
    influences_to_unbind = influences_to_unbind or selected_joints
    if not skinned_objects:
        skinned_objects = [xform for xform in selected_transforms if xform not in selected_joints]
    if not skinned_objects or not influences_to_unbind:
        return False
    skinned_objects = python.force_list(skinned_objects)
    influences_to_unbind = python.force_list(influences_to_unbind)
    influences_to_unbind_short = [dcc.node_short_name(joint_node) for joint_node in influences_to_unbind]

    skin_clusters = list()
    skin_percentage = 100.0 / len(skinned_objects)

    for i, skin_object in enumerate(skinned_objects):

        library.Command.progressCommand.emit(skin_percentage * (i + 1), 'Unbinding Influence: {}'.format(i))

        skin_cluster_name = skin_utils.find_related_skin_cluster(skin_object)
        if not skin_cluster_name:
            continue
        joints_attached = maya.cmds.skinCluster(skin_cluster_name, query=True, inf=True)

        influence_verts = skin_utils.get_influence_vertices(influences_to_unbind, skin_object)
        if not influence_verts:
            continue

        joints = list()
        for joint_to_remove in influences_to_unbind_short:
            if joint_to_remove not in joints_attached:
                continue
            joints.append((joint_to_remove, 0.0))

        maya.cmds.select(influence_verts, replace=True)
        maya.cmds.skinPercent(skin_cluster_name, transformValue=joints, normalize=True)

        skin_clusters.append(skin_cluster_name)

    for skin_cluster in skin_clusters:
        joints_attached = maya.cmds.skinCluster(skin_cluster, query=True, inf=True)
        for jnt in influences_to_unbind_short:
            if jnt not in joints_attached:
                continue
            maya.cmds.skinCluster(skin_cluster, edit=True, removeInfluence=jnt)

    if delete:
        for joint_to_remove in influences_to_unbind:
            child_joints = maya.cmds.listRelatives(joint_to_remove, children=True)
            parent = maya.cmds.listRelatives(joint_to_remove, parent=True)
            if not child_joints:
                continue
            if not parent:
                maya.cmds.parent(child_joints, world=True)
                continue
            maya.cmds.parent(child_joints, parent)
        maya.cmds.delete(influences_to_unbind)

    return True


@decorators.undo
def unbind_influences(skinned_objects=None, influences_to_unbind=None, delete=False, use_parent=True):
    """
    Unbind given influences from given meshes and stores the unbind influences weights into other influences

    :param skinned_objects: list(str), meshes which joints need to be removed
    :param influences_to_unbind: list(str), list of joints that need to be unbind
    :param delete: bool, Whether or not to delete unbind influences after unbind process is completed
    :param use_parent: bool, If True, removed influences weights will be stored on its parent; if False it will look
        for the closest joint using a point cloud system
    :return: bool
    """

    selected_transforms = dcc.selected_nodes_of_type('transform')
    selected_joints = dcc.selected_nodes_of_type('joint')
    influences_to_unbind = influences_to_unbind or selected_joints
    if not skinned_objects:
        skinned_objects = [xform for xform in selected_transforms if xform not in selected_joints]
    if not skinned_objects or not influences_to_unbind:
        return False
    skinned_objects = python.force_list(skinned_objects)
    influences_to_unbind = python.force_list(influences_to_unbind)
    influences_to_unbind_short = [dcc.node_short_name(joint_node) for joint_node in influences_to_unbind]

    skin_clusters = list()
    skin_percentage = 100.0 / len(skinned_objects)

    for skin_index, skin_object in enumerate(skinned_objects):
        skin_cluster_name = skin_utils.find_related_skin_cluster(skin_object)
        if not skin_cluster_name:
            continue
        joints_attached = maya.cmds.skinCluster(skin_cluster_name, query=True, inf=True)

        if not use_parent:
            for joint_to_remove in influences_to_unbind_short:
                if joint_to_remove in joints_attached:
                    joints_attached.remove(joint_to_remove)

        source_positions = list()
        source_joints = list()
        for joint_attached in joints_attached:
            pos = maya.cmds.xform(joint_attached, query=True, worldSpace=True, t=True)
            source_positions.append(pos)
            source_joints.append([joint_attached, pos])

        source_kdtree = kdtree.KDTree.construct_from_data(source_positions)

        joint_percentage = skin_percentage / len(influences_to_unbind)
        for joint_index, jnt in enumerate(influences_to_unbind):
            jnt1 = jnt
            if use_parent:
                jnt2 = maya.cmds.listRelatives(jnt, parent=True)
                jnt2 = jnt2[0] if jnt2 else None
                if jnt2 is None:
                    remove_pos = maya.cmds.xform(jnt, query=True, worldSpace=True, t=True)
                    points = source_kdtree.query(query_point=remove_pos, t=1)
                    for index, position in enumerate(source_joints):
                        if position[1] != points[0]:
                            continue
                        jnt2 = position[0]
            else:
                remove_pos = maya.cmds.xform(jnt, query=True, worldSpace=True, t=True)
                points = source_kdtree.query(query_point=remove_pos, t=True)
                for index, position in enumerate(source_joints):
                    if position[1] != points[0]:
                        continue
                    jnt2 = position[0]

            move_skin_weights(jnt1, jnt2, skin_object)

            library.Command.progressCommand.emit(
                ((joint_index + 1) * joint_percentage) + (skin_index * skin_percentage), 'Unbinding Influence: {}')

        skin_clusters.append(skin_cluster_name)

    for skin_cluster in skin_clusters:
        joints_attached = maya.cmds.skinCluster(skin_cluster, query=True, inf=True)
        for jnt in influences_to_unbind_short:
            if jnt not in joints_attached:
                continue
            maya.cmds.skinCluster(skin_cluster, edit=True, removeInfluence=jnt)

    if delete:
        for joint_to_remove in influences_to_unbind:
            child_joints = maya.cmds.listRelatives(joint_to_remove, children=True)
            parent = maya.cmds.listRelatives(joint_to_remove, parent=True)
            if not child_joints:
                continue
            if not parent:
                maya.cmds.parent(child_joints, world=True)
                continue
            maya.cmds.parent(child_joints, parent)
        maya.cmds.delete(influences_to_unbind)

    return True


@decorators.repeat_static_command(__name__, skip_arguments=True)
def br_smooth_weights():
    """
    Executes Brave Rabbit Smooth Weights command if available
    :return: bool
    """

    if not dcc.is_plugin_loaded('brSmoothWeights.mll'):
        return False

    maya.mel.eval('brSmoothWeightsToolCtx')

    return True


@decorators.repeat_static_command(__name__, skip_arguments=True)
def br_smooth_weights_options():
    """
    Opens Brave Rabbit Smooth Weights tool if available
    :return: bool
    """

    if not dcc.is_plugin_loaded('brSmoothWeights.mll'):
        return False

    maya.mel.eval('brSmoothWeightsToolCtx; toolPropertyWindow;')

    return True


@decorators.repeat_static_command(__name__, skip_arguments=True)
def br_transfer_weights():
    """
    Executes Brave Rabbit Transfer Weights command if available
    :return: bool
    """

    plugin_name = 'brSmoothWeights.mll'
    if not dcc.is_plugin_loaded(plugin_name):
        dcc.load_plugin(plugin_name, quiet=True)
        if not dcc.is_plugin_loaded(plugin_name):
            return False

    maya.mel.eval('brTransferWeightsToolCtx')

    return True


@decorators.repeat_static_command(__name__, skip_arguments=True)
def br_transfer_weights_options():
    """
    Opens Brave Rabbit Transfer Weights tool if available
    :return: bool
    """

    plugin_name = 'brSmoothWeights.mll'
    if not dcc.is_plugin_loaded(plugin_name):
        dcc.load_plugin(plugin_name, quiet=True)
        if not dcc.is_plugin_loaded(plugin_name):
            return False
        return False

    maya.mel.eval('brTransferWeightsToolCtx; toolPropertyWindow;')

    return True


@decorators.repeat_static_command(__name__, skip_arguments=True)
def ng_skin_tools():
    """
    Opens ngSkinTools tool if available
    First, we try to open ngSkinTools2 and if it is not available, we launch ngSkinTools1
    :return: bool
    """

    plugin_names = ['ngSkinTools2.mll', 'ngSkinTools.mll']
    for plugin_name in plugin_names:
        if not dcc.is_plugin_loaded(plugin_name):
            dcc.load_plugin(plugin_name, quiet=True)
        if dcc.is_plugin_loaded(plugin_name):
            if plugin_name == 'ngSkinTools2.mll':
                try:
                    import ngSkinTools2
                    ngSkinTools2.open_ui()
                    return True
                except Exception as exc:
                    LOGGER.warning(
                        'Impossible to launch ngSkinTool2. Trying to launch ngSkinTools1: "{}"'.format(exc))
                    continue
            else:
                try:
                    from ngSkinTools.ui.mainwindow import MainWindow
                    MainWindow.open()
                    return True
                except Exception as exc:
                    'Impossible to launch ngSkinTool1: "{}"'.format(exc)
                    continue

    return False
