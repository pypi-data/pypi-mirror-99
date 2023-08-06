#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""
Module that contains widget for rig skinning functionality
"""

from __future__ import print_function, division, absolute_import

import logging

from Qt.QtCore import Signal, QObject
from Qt.QtWidgets import QWidget, QMessageBox

from tpDcc.libs.qt.core import qtutils
from tpDcc.libs.qt.widgets import layouts, checkbox

from tpRigToolkit.tools.rigtoolbox.core import consts
from tpRigToolkit.tools.rigtoolbox.widgets import base, fallofcurve
from tpRigToolkit.tools.rigtoolbox.dccs.maya.widgets import labelsdialog

LOGGER = logging.getLogger(consts.TOOL_ID)


class SkinningWidget(base.CommandRigToolBoxWidget, object):
    def __init__(self, client, commands_data, parent=None):

        self._model = SkinningWidgetModel()

        super(SkinningWidget, self).__init__(
            title='Skinning', commands_data=commands_data,
            controller=SkinningWidgetController(model=self._model, client=client), parent=parent)

        self.refresh()

    @property
    def model(self):
        return self._model

    @property
    def controller(self):
        return self._controller

    def ui(self):
        super(SkinningWidget, self).ui()

        self._average_falloff_widget = QWidget()
        average_falloff_layout = layouts.VerticalLayout(spacing=2, margins=(5, 5, 5, 5))
        self._average_falloff_widget.setLayout(average_falloff_layout)
        self._average_falloff_curve = fallofcurve.FallofCurveWidget(parent=self)
        average_falloff_layout.addWidget(self._average_falloff_curve)

        self._mirror_auto_assign_joints_labels_cbx = checkbox.BaseCheckBox('Auto Assign Labels', self)
        self._copy_skin_weights_auto_assign_joints_labels_cbx = checkbox.BaseCheckBox('Auto Assign Labels', self)
        self._transfer_skin_uvs_auto_assign_joints_labels_cbx = checkbox.BaseCheckBox('Auto Assign Labels', self)
        self._clean_skin_mesh_auto_assign_joints_labels_cbx = checkbox.BaseCheckBox('Auto Assign Labels', self)
        self._extract_skin_faces_auto_assign_joints_labels_cbx = checkbox.BaseCheckBox('Auto Assign Labels', self)

        self._distance_widget = QWidget()
        distance_layout = layouts.VerticalLayout(spacing=2, margins=(5, 5, 5, 5))
        self._distance_widget.setLayout(distance_layout)
        self._distance_average_cbx = checkbox.BaseCheckBox('On Distance', self)
        self._average_falloff_curve = fallofcurve.FallofCurveWidget(parent=self)
        distance_layout.addWidget(self._distance_average_cbx)
        distance_layout.addWidget(self._average_falloff_curve)
        self._fast_delete_cbx = checkbox.BaseCheckBox('Fast Delete', self)

        self._average_falloff_widget.setVisible(False)
        self._mirror_auto_assign_joints_labels_cbx.setVisible(False)
        self._copy_skin_weights_auto_assign_joints_labels_cbx.setVisible(False)
        self._transfer_skin_uvs_auto_assign_joints_labels_cbx.setVisible(False)
        self._clean_skin_mesh_auto_assign_joints_labels_cbx.setVisible(False)
        self._extract_skin_faces_auto_assign_joints_labels_cbx.setVisible(False)
        self._distance_widget.setVisible(False)
        self._fast_delete_cbx.setVisible(False)

        self.main_layout.addWidget(self._average_falloff_widget)
        self.main_layout.addWidget(self._mirror_auto_assign_joints_labels_cbx)
        self.main_layout.addWidget(self._copy_skin_weights_auto_assign_joints_labels_cbx)
        self.main_layout.addWidget(self._transfer_skin_uvs_auto_assign_joints_labels_cbx)
        self.main_layout.addWidget(self._clean_skin_mesh_auto_assign_joints_labels_cbx)
        self.main_layout.addWidget(self._extract_skin_faces_auto_assign_joints_labels_cbx)
        self.main_layout.addWidget(self._distance_widget)
        self.main_layout.addWidget(self._fast_delete_cbx)

    def setup_signals(self):
        self._mirror_auto_assign_joints_labels_cbx.toggled.connect(self._controller.set_mirror_auto_assign_labels)
        self._copy_skin_weights_auto_assign_joints_labels_cbx.toggled.connect(
            self._controller.set_copy_skin_weights_auto_assign_labels)
        self._transfer_skin_uvs_auto_assign_joints_labels_cbx.toggled.connect(
            self._controller.set_transfer_skin_uvs_auto_assign_labels)
        self._clean_skin_mesh_auto_assign_joints_labels_cbx.toggled.connect(
            self._controller.set_clean_skin_mesh_auto_assign_labels)
        self._extract_skin_faces_auto_assign_joints_labels_cbx.toggled.connect(
            self._controller.set_extract_skin_faces_auto_assign_labels)
        self._distance_average_cbx.toggled.connect(self._controller.set_distance_average)
        self._fast_delete_cbx.toggled.connect(self._controller.set_fast_delete)
        self._average_falloff_curve.curveUpdated.connect(self._controller.set_average_weights_curve_points)

        self._model.mirrorAutoAssignLabelsChanged.connect(self._mirror_auto_assign_joints_labels_cbx.setChecked)
        self._model.copySkinWeightsAutoAssignLabelsChanged.connect(
            self._copy_skin_weights_auto_assign_joints_labels_cbx.setChecked)
        self._model.transferSkinUVsAutoAssignLabelsChanged.connect(
            self._transfer_skin_uvs_auto_assign_joints_labels_cbx.setChecked)
        self._model.cleanSkinMeshAutoAssignLabelsChanged.connect(
            self._clean_skin_mesh_auto_assign_joints_labels_cbx.setChecked)
        self._model.extractSkinFacesAutoAssignLabelsChanged.connect(
            self._extract_skin_faces_auto_assign_joints_labels_cbx.setChecked)
        self._model.useDistanceAverageChanged.connect(self._distance_average_cbx.setChecked)
        self._model.fastDeleteChanged.connect(self._fast_delete_cbx.setChecked)

    def _check_command_availability(self, command_name):

        client = self._controller.client
        if not client:
            return False

        if command_name == 'br_smooth_weights' or command_name == 'br_transfer_weights':
            for plugin_name in ['rampWeights.mll', 'weightsServer.mll', 'weightDriver.mll', 'brSmoothWeights.mll']:
                client.load_plugin(plugin_name, quiet=True)
            plugin_name = 'brSmoothWeights.mll'
            return client.is_plugin_loaded(plugin_name)
        elif command_name == 'ng_skin_tools':
            plugin_names = ['ngSkinTools2.mll', 'ngSkinTools.mll']
            for plugin_name in plugin_names:
                client.load_plugin(plugin_name, quiet=True)
                if client.is_plugin_loaded(plugin_name):
                    return True
            return False

        return True

    def _on_show_context_menu(self):
        super(SkinningWidget, self)._on_show_context_menu()

        self._average_falloff_curve.update_view()

    def refresh(self):

        self._mirror_auto_assign_joints_labels_cbx.setChecked(self._model.mirror_auto_assign_labels)
        self._copy_skin_weights_auto_assign_joints_labels_cbx.setChecked(
            self._model.copy_skin_weights_auto_assign_labels)
        self._transfer_skin_uvs_auto_assign_joints_labels_cbx.setChecked(
            self._model.transfer_uvs_auto_assign_labels)
        self._clean_skin_mesh_auto_assign_joints_labels_cbx.setChecked(
            self._model.clean_skin_mesh_auto_assign_labels)
        self._extract_skin_faces_auto_assign_joints_labels_cbx.setChecked(
            self._model.extract_skin_faces_auto_assign_labels)
        self._distance_average_cbx.setChecked(self._model.use_distance_average)
        self._fast_delete_cbx.setChecked(self._model.fast_delete)

        # NOTE: We do this to force model, to have point list value on startup
        self._controller.set_average_weights_curve_points(self._average_falloff_curve.curve_as_points())


class SkinningWidgetModel(QObject, object):

    mirrorAutoAssignLabelsChanged = Signal(bool)
    copySkinWeightsAutoAssignLabelsChanged = Signal(bool)
    transferSkinUVsAutoAssignLabelsChanged = Signal(bool)
    cleanSkinMeshAutoAssignLabelsChanged = Signal(bool)
    extractSkinFacesAutoAssignLabelsChanged = Signal(bool)
    useDistanceAverageChanged = Signal(bool)
    fastDeleteChanged = Signal(bool)

    def __init__(self):
        super(SkinningWidgetModel, self).__init__()

        self._mirror_auto_assign_labels = True
        self._copy_skin_weights_auto_assign_labels = True
        self._transfer_skin_uvs_auto_assign_labels = True
        self._clean_skin_mesh_auto_assign_labels = True
        self._extract_skin_faces_auto_assign_labels = True
        self._use_distance_average = True
        self._fast_delete = True
        self._average_weights_curve_points = list()

    @property
    def mirror_auto_assign_labels(self):
        return self._mirror_auto_assign_labels

    @mirror_auto_assign_labels.setter
    def mirror_auto_assign_labels(self, flag):
        self._mirror_auto_assign_labels = bool(flag)
        self.mirrorAutoAssignLabelsChanged.emit(self._mirror_auto_assign_labels)

    @property
    def copy_skin_weights_auto_assign_labels(self):
        return self._copy_skin_weights_auto_assign_labels

    @copy_skin_weights_auto_assign_labels.setter
    def copy_skin_weights_auto_assign_labels(self, flag):
        self._copy_skin_weights_auto_assign_labels = bool(flag)
        self.copySkinWeightsAutoAssignLabelsChanged.emit(self._copy_skin_weights_auto_assign_labels)

    @property
    def transfer_uvs_auto_assign_labels(self):
        return self._transfer_skin_uvs_auto_assign_labels

    @transfer_uvs_auto_assign_labels.setter
    def transfer_uvs_auto_assign_labels(self, flag):
        self._transfer_skin_uvs_auto_assign_labels = bool(flag)
        self.transferSkinUVsAutoAssignLabelsChanged.emit(self._transfer_skin_uvs_auto_assign_labels)()

    @property
    def clean_skin_mesh_auto_assign_labels(self):
        return self._clean_skin_mesh_auto_assign_labels

    @clean_skin_mesh_auto_assign_labels.setter
    def clean_skin_mesh_auto_assign_labels(self, flag):
        self._clean_skin_mesh_auto_assign_labels = bool(flag)
        self.cleanSkinMeshAutoAssignLabelsChanged.emit(self._clean_skin_mesh_auto_assign_labels)

    @property
    def extract_skin_faces_auto_assign_labels(self):
        return self._extract_skin_faces_auto_assign_labels

    @extract_skin_faces_auto_assign_labels.setter
    def extract_skin_faces_auto_assign_labels(self, flag):
        self._extract_skin_faces_auto_assign_labels = bool(flag)
        self.extractSkinFacesAutoAssignLabelsChanged.emit(self._extract_skin_faces_auto_assign_labels)

    @property
    def use_distance_average(self):
        return self._use_distance_average

    @use_distance_average.setter
    def use_distance_average(self, flag):
        self._use_distance_average = bool(flag)
        self.useDistanceAverageChanged.emit(self._use_distance_average)

    @property
    def fast_delete(self):
        return self._fast_delete

    @fast_delete.setter
    def fast_delete(self, flag):
        self._fast_delete = bool(flag)
        self.fastDeleteChanged.emit(self._fast_delete)

    @property
    def average_weights_curve_points(self):
        return self._average_weights_curve_points

    @average_weights_curve_points.setter
    def average_weights_curve_points(self, widget):
        self._average_weights_curve_points = widget


class SkinningWidgetController(object):

    def __init__(self, client, model):
        super(SkinningWidgetController, self).__init__()

        self._model = model
        self._client = client

    @property
    def model(self):
        return self._model

    @property
    def client(self):
        return self._client

    def set_mirror_auto_assign_labels(self, flag):
        self._model.mirror_auto_assign_labels = flag

    def set_copy_skin_weights_auto_assign_labels(self, flag):
        self._model.copy_skin_weights_auto_assign_labels = flag

    def set_transfer_skin_uvs_auto_assign_labels(self, flag):
        self._model.transfer_skin_uvs_auto_assign_labels = flag

    def set_clean_skin_mesh_auto_assign_labels(self, flag):
        self._model.clean_skin_mesh_auto_assign_labels = flag

    def set_extract_skin_faces_auto_assign_labels(self, flag):
        self._model.extract_skin_faces_auto_assign_labels = flag

    def set_distance_average(self, flag):
        self._model.use_distance_average = flag

    def set_fast_delete(self, flag):
        self._model.fast_delete = flag

    def set_average_weights_curve_points(self, points_list):
        self._model.average_weights_curve_points = points_list

    def smooth_bind_skin(self):
        return self._client.smooth_bind_skin(show_options=True)

    def rigid_bind_skin(self):
        return self._client.rigid_bind_skin(show_options=True)

    def detach_skin(self):
        return self._client.detach_bind_skin(show_options=False)

    def detach_skin_options(self):
        return self._client.detach_bind_skin(show_options=True)

    def open_paint_skin_weights_tool(self):
        return self._client.open_paint_skin_weights_tool(show_options=False)

    def open_paint_skin_weights_tool_options(self):
        return self._client.open_paint_skin_weights_tool(show_options=True)

    def mirror_skin_weights(self):
        auto_assign_labels = self._model.mirror_auto_assign_labels
        left_side, right_side = self._check_labels(auto_assign_labels)

        return self._client.mirror_skin_weights(
            auto_assign_labels=auto_assign_labels, left_side_label=left_side,
            right_side_label=right_side, show_options=True)

    def copy_skin_weights(self):
        auto_assign_labels = self._model.copy_skin_weights_auto_assign_labels
        left_side, right_side = self._check_labels(auto_assign_labels)

        return self._client.copy_skin_weights(
            auto_assign_labels=auto_assign_labels, left_side_label=left_side,
            right_side_label=right_side, show_options=True)

    def prune_skin_weights(self):
        return self._client.prune_skin_weights(show_options=True)

    def transfer_skin_uvs(self):
        auto_assign_labels = self._model.transfer_skin_uvs_auto_assign_labels
        left_side, right_side = self._check_labels(auto_assign_labels)

        return self._client.transfer_skin_uvs(
            auto_assign_labels=auto_assign_labels, left_side_label=left_side, right_side_label=right_side)

    def clean_skinned_mesh(self):
        auto_assign_labels = self._model.clean_skin_mesh_auto_assign_labels
        left_side, right_side = self._check_labels(auto_assign_labels)

        return self._client.clean_skinned_mesh(
            auto_assign_labels=auto_assign_labels, left_side_label=left_side, right_side_label=right_side)

    def combine_skinned_meshes(self):
        return self._client.combine_skinned_meshes()

    def extract_skinned_faces(self):
        auto_assign_labels = self._model.extract_skin_faces_auto_assign_labels
        left_side, right_side = self._check_labels(auto_assign_labels)

        return self._client.extract_skinned_selected_faces(
            auto_assign_labels=auto_assign_labels, left_side_label=left_side, right_side_label=right_side)

    def remove_unused_influences(self):
        return self._client.remove_unused_influences()

    def restore_bind_pose(self):
        res = qtutils.show_question(None, 'Go to Bind Pose', 'Are you sure yo want to restore bind pose?')
        if res != QMessageBox.Yes:
            return False

        return self._client.restore_bind_pose()

    def remove_bind_poses(self):
        res = qtutils.show_question(
            None, 'Remove Bind Poses', 'Are you sure yo want to remove all bind poses from the current scene?')
        if res != QMessageBox.Yes:
            return False

        return self._client.remove_bind_poses()

    def weights_hammer(self):
        return self._client.weights_hammer()

    def average_vertex_weights(self):
        use_distance_average = self._model.use_distance_average
        curve_weight_points = self._model.average_weights_curve_points

        return self._client.average_vertex_weights(
            use_distance=use_distance_average, curve_weight_points=curve_weight_points)

    def move_skin_weights(self):
        return self._client.move_skin_weights()

    def swap_skin_weights(self):
        return self._client.swap_skin_weights()

    def select_influences(self):
        return self._client.select_influences()

    def select_influence_components(self):
        return self._client.select_influence_components()

    def delete_influences(self):
        fast_delete = self._model.fast_delete
        return self._client.delete_influences(fast_delete=fast_delete)

    def br_smooth_weights(self):
        return self._client.br_smooth_weights()

    def br_smooth_weights_options(self):
        return self._client.br_smooth_weights(options=True)

    def br_transfer_weights_options(self):
        return self._client.br_transfer_weights()

    def br_transfer_weights(self):
        return self._client.br_transfer_weights(options=True)

    def ng_skin_tools(self):
        return self._client.ng_skin_tools()

    def _check_labels(self, auto_assign_labels):
        left_side = None
        right_side = None
        if auto_assign_labels:
            check_joints_labels = self._client.check_joints_labels()
            if not check_joints_labels:
                labels_dialog = labelsdialog.JointsLabelDialog()
                labels_dialog.exec_()
                left_side, right_side = labels_dialog.get_sides()
                if not left_side or not right_side:
                    return False, False

        return left_side, right_side
