#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""
Module that contains widget with joint functionality
"""

import logging

from Qt.QtCore import Signal, QObject
from Qt.QtWidgets import QWidget

from tpDcc import dcc
from tpDcc.libs.qt.core import contexts as qt_contexts
from tpDcc.libs.qt.widgets import layouts, label, spinbox, checkbox

from tpRigToolkit.tools.rigtoolbox.core import consts
from tpRigToolkit.tools.rigtoolbox.widgets import base

LOGGER = logging.getLogger(consts.TOOL_ID)


class JointWidget(base.CommandRigToolBoxWidget, object):

    def __init__(self, client, commands_data, parent=None):

        self._model = JointWidgetModel()

        super(JointWidget, self).__init__(
            title='Joint', commands_data=commands_data,
            controller=JointWidgetController(model=self._model, client=client), parent=parent)

        self.refresh()

    @property
    def model(self):
        return self._model

    @property
    def controller(self):
        return self._controller

    def ui(self):
        super(JointWidget, self).ui()

        self._joints_to_insert_widget = QWidget()
        joints_to_insert_layout = layouts.HorizontalLayout(spacing=0, margins=(0, 0, 0, 0))
        self._joints_to_insert_widget.setLayout(joints_to_insert_layout)
        joints_to_insert_lbl = label.BaseLabel('Num. Joints: ', parent=self)
        self._joints_to_insert_spn = spinbox.BaseSpinBox(parent=self)
        self._joints_to_insert_spn.setMinimum(1)
        self._joints_to_insert_spn.setMaximum(99999999)
        joints_to_insert_layout.addWidget(joints_to_insert_lbl)
        joints_to_insert_layout.addWidget(self._joints_to_insert_spn)

        self._create_joints_on_curve_widget = QWidget()
        create_joints_on_curve_layout = layouts.HorizontalLayout(spacing=0, margins=(0, 0, 0, 0))
        self._create_joints_on_curve_widget.setLayout(create_joints_on_curve_layout)
        create_joints_on_curve_lbl = label.BaseLabel('Num. Joints: ', parent=self)
        self._create_joints_on_curve_spn = spinbox.BaseSpinBox(parent=self)
        self._create_joints_on_curve_spn.setMinimum(1)
        self._create_joints_on_curve_spn.setMaximum(99999999)
        create_joints_on_curve_layout.addWidget(create_joints_on_curve_lbl)
        create_joints_on_curve_layout.addWidget(self._create_joints_on_curve_spn)

        self._snap_joints_to_curve_widget = QWidget()
        snap_joints_to_curve_layout = layouts.HorizontalLayout(spacing=0, margins=(0, 0, 0, 0))
        self._snap_joints_to_curve_widget.setLayout(snap_joints_to_curve_layout)
        snap_joints_to_curve_lbl = label.BaseLabel('Num. Joints: ', parent=self)
        self._snap_joints_to_curve_spn = spinbox.BaseSpinBox(parent=self)
        self._snap_joints_to_curve_spn.setMinimum(0)
        self._snap_joints_to_curve_spn.setMaximum(99999999)
        snap_joints_to_curve_layout.addWidget(snap_joints_to_curve_lbl)
        snap_joints_to_curve_layout.addWidget(self._snap_joints_to_curve_spn)

        self._joints_display_size_widget = QWidget()
        joint_display_size_layout = layouts.HorizontalLayout(spacing=0, margins=(0, 0, 0, 0))
        self._joints_display_size_widget.setLayout(joint_display_size_layout)
        joint_display_size_lbl = label.BaseLabel('Joints Size: ', parent=self)
        self._joints_display_size_spn = spinbox.BaseDoubleSpinBox(parent=self)
        self._joints_display_size_spn.setSingleStep(0.5)
        self._joints_display_size_spn.setMinimum(0.1)
        self._joints_display_size_spn.setMaximum(999)
        self._joints_display_live_cbx = checkbox.BaseCheckBox('Live', parent=self)
        joint_display_size_layout.addWidget(joint_display_size_lbl)
        joint_display_size_layout.addWidget(self._joints_display_size_spn)
        joint_display_size_layout.addWidget(self._joints_display_live_cbx)

        self._joints_to_insert_widget.setVisible(False)
        self._create_joints_on_curve_widget.setVisible(False)
        self._snap_joints_to_curve_widget.setVisible(False)
        self._joints_display_size_widget.setVisible(False)

        self.main_layout.addWidget(self._joints_to_insert_widget)
        self.main_layout.addWidget(self._create_joints_on_curve_widget)
        self.main_layout.addWidget(self._snap_joints_to_curve_widget)
        self.main_layout.addWidget(self._joints_display_size_widget)

    def setup_signals(self):
        self._joints_to_insert_spn.valueChanged.connect(self._controller.change_joints_to_insert)
        self._create_joints_on_curve_spn.valueChanged.connect(self._controller.change_joints_on_curve)
        self._snap_joints_to_curve_spn.valueChanged.connect(self._controller.change_snap_joints_to_curve)
        self._joints_display_size_spn.valueChanged.connect(self._controller.change_joints_display_size)
        self._joints_display_live_cbx.toggled.connect(self._controller.change_joints_display_size_live)

        self._model.jointsToInsertChanged.connect(self._joints_to_insert_spn.setValue)
        self._model.jointsOnCurveChanged.connect(self._create_joints_on_curve_spn.setValue)
        self._model.snapJointsToCurveChanged.connect(self._snap_joints_to_curve_spn.setValue)
        self._model.jointsDisplaySizeChanged.connect(self._on_joints_display_size_changed)
        self._model.jointsDisplaySizeLiveChanged.connect(self._joints_display_live_cbx.setChecked)

    def refresh(self):
        self._joints_to_insert_spn.setValue(self._model.joints_to_insert)
        self._joints_display_size_spn.setValue(self._model.joints_display_size)
        self._joints_display_live_cbx.setChecked(self._model.joints_display_size_live)
        self._create_joints_on_curve_spn.setValue(self._model.joints_on_curve)
        self._snap_joints_to_curve_spn.setValue(self._model.snap_joints_to_curve)

    def _on_joints_display_size_changed(self, value):
        live = self._model.joints_display_size_live

        with qt_contexts.block_signals(self._joints_display_size_spn):
            self._joints_display_size_spn.setValue(value)

        if live:
            self._controller.joint_display_size()

    # def _setup_mirror_tools(self):

    #     mirror_icon = resources.icon('mirror', extension='png')
    #     mirror_all_icon = resources.icon('mirror_all', extension='png')
    #     mirror_selection_icon = resources.icon('mirror_selection', extension='png')
    #     mirror_joint_btn = buttons.BaseToolButton(parent=self)
    #     mirror_joint_btn.setPopupMode(QToolButton.MenuButtonPopup)
    #     mirror_joint_btn.setToolButtonStyle(Qt.ToolButtonTextUnderIcon)
    #     mirror_joint_btn.setIcon(mirror_icon)
    #     mirror_joint_btn.setText('Mirror Joint')
    #     mirror_joint_menu = QMenu(mirror_joint_btn)
    #     mirror_joint_btn.setMenu(mirror_joint_menu)
    #     mirror_all_joints_action = QAction(mirror_all_icon, 'Mirror All Joints', mirror_joint_menu)
    #     mirror_selected_joints_action = QAction(mirror_selection_icon, 'Mirror Selected Joints', mirror_joint_menu)
    #     mirror_hierarchy_joints_action = QAction(mirror_selection_icon, 'Mirror Hierarchy Joints', mirror_joint_menu)
    #     mirror_joint_menu.addAction(mirror_all_joints_action)
    #     mirror_joint_menu.addAction(mirror_selected_joints_action)
    #     mirror_joint_menu.addAction(mirror_hierarchy_joints_action)
    #     mirror_joint_btn.clicked.connect(self._controller.mirror_all_joints)
    #     mirror_selected_joints_action.triggered.connect(self._controller.mirror_selected_joints)
    #     mirror_all_joints_action.triggered.connect(self._controller.mirror_all_joints)
    #     mirror_hierarchy_joints_action.triggered.connect(self._controller.mirror_hierarchy_joints)
    #     self.mirror_layout.addWidget(mirror_joint_btn)
    #
    #     mirror_create_icon = resources.icon('mirror2', extension='png')
    #     mirror_create_all_icon = resources.icon('mirror2', extension='png')
    #     mirror_create_btn = buttons.BaseToolButton(parent=self)
    #     mirror_create_btn.setPopupMode(QToolButton.MenuButtonPopup)
    #     mirror_create_btn.setToolButtonStyle(Qt.ToolButtonTextUnderIcon)
    #     mirror_create_btn.setIcon(mirror_create_icon)
    #     mirror_create_btn.setText('Mirror Create')
    #     mirror_create_menu = QMenu(mirror_create_btn)
    #     mirror_create_btn.setMenu(mirror_create_menu)
    #     mirror_create_all_joints_action = QAction(
    #         mirror_create_all_icon, 'Mirror Create All Joints', mirror_create_menu)
    #     mirror_create_menu.addAction(mirror_create_all_joints_action)
    #     mirror_create_btn.clicked.connect(self._controller.mirror_create_all_joints)
    #     mirror_create_all_joints_action.triggered.connect(self._controller.mirror_create_all_joints)
    #     self.mirror_layout.addWidget(mirror_create_btn)
    #
    #     return mirror_widget
    #
    # def _setup_pose_tools(self):
    #     pose_widget = QWidget()
    #     self.pose_layout = layouts.FlowLayout()
    #     self.pose_layout.setAlignment(Qt.AlignLeft)
    #     pose_widget.setLayout(self.pose_layout)
    #
    #     go_to_bindpose_btn = buttons.BaseButton('Go to Bindpose', parent=self)
    #     self.pose_layout.addWidget(go_to_bindpose_btn)
    #
    #     return pose_widget


class JointWidgetModel(QObject, object):

    jointsToInsertChanged = Signal(int)
    jointsOnCurveChanged = Signal(int)
    snapJointsToCurveChanged = Signal(int)
    jointsDisplaySizeChanged = Signal(float)
    jointsDisplaySizeLiveChanged = Signal(bool)

    def __init__(self):
        super(JointWidgetModel, self).__init__()

        self._joints_to_insert = 1
        self._joints_on_curve = 10
        self._snap_joints_to_curve = 0
        self._joints_display_size_live = True

        try:
            self._joints_display_size = dcc.client().get_joint_display_size()
        except Exception:
            LOGGER.warning('Impossible to retrieve current DCC joint display size. Using 1.0 by default ...')
            self._joints_display_size = 1.0

    @property
    def joints_to_insert(self):
        return self._joints_to_insert

    @joints_to_insert.setter
    def joints_to_insert(self, value):
        self._joints_to_insert = int(value)
        self.jointsToInsertChanged.emit(self._joints_to_insert)

    @property
    def joints_on_curve(self):
        return self._joints_on_curve

    @joints_on_curve.setter
    def joints_on_curve(self, value):
        self._joints_on_curve = int(value)
        self.jointsOnCurveChanged.emit(self._joints_on_curve)

    @property
    def snap_joints_to_curve(self):
        return self._snap_joints_to_curve

    @snap_joints_to_curve.setter
    def snap_joints_to_curve(self, value):
        self._snap_joints_to_curve = int(value)
        self.snapJointsToCurveChanged.emit(self._snap_joints_to_curve)

    @property
    def joints_display_size_live(self):
        return self._joints_display_size_live

    @joints_display_size_live.setter
    def joints_display_size_live(self, flag):
        self._joints_display_size_live = bool(flag)
        self.jointsDisplaySizeLiveChanged.emit(self._joints_display_size_live)

    @property
    def joints_display_size(self):
        return self._joints_display_size

    @joints_display_size.setter
    def joints_display_size(self, value):
        self._joints_display_size = float(value)
        self.jointsDisplaySizeChanged.emit(self._joints_display_size)


class JointWidgetController(object):

    def __init__(self, model, client):
        super(JointWidgetController, self).__init__()

        self._model = model
        self._client = client

    @property
    def model(self):
        return self._model

    @property
    def client(self):
        return self._client

    def change_joints_to_insert(self, value):
        self._model.joints_to_insert = value

    def change_joints_on_curve(self, value):
        self._model.joints_on_curve = value

    def change_snap_joints_to_curve(self, value):
        self._model.snap_joints_to_curve = value

    def change_joints_display_size(self, value):
        self._model.joints_display_size = value

    def change_joints_display_size_live(self, flag):
        self._model.joints_display_size_live = flag

    def start_joint_tool(self):
        return self._client.start_joint_tool()

    def create_new_joint_on_center(self):
        return self._client.create_new_joint_on_center()

    def create_new_joints_on_selected_components(self):
        return self._client.create_new_joints_on_selected_components()

    def insert_joints(self):
        joint_count = self._model.joints_to_insert
        return self._client.insert_joints(num_joints=joint_count)

    def create_joints_on_curve(self):
        joints_on_curve = self._model.joints_on_curve
        return self._client.create_joints_on_curve(num_joints=joints_on_curve)

    def snap_joints_to_curve(self):
        joints_to_snap = self._model.snap_joints_to_curve
        return self._client.snap_joints_to_curve(num_joints=joints_to_snap)

    def toggle_local_rotation_axis(self):
        return self._client.toggle_local_rotation_axis()

    def toggle_all_local_rotation_axis(self):
        return self._client.toggle_all_local_rotation_axis()

    def toggle_selected_local_rotation_axis(self):
        return self._client.toggle_selected_local_rotation_axis()

    def on_all_local_rotation_axis(self):
        return self._client.toggle_all_local_rotation_axis(flag=True)

    def off_all_local_rotation_axis(self):
        return self._client.toggle_all_local_rotation_axis(flag=False)

    def on_selected_local_rotation_axis(self):
        return self._client.toggle_selected_local_rotation_axis(flag=True)

    def off_selected_local_rotation_axis(self):
        return self._client.toggle_selected_local_rotation_axis(flag=False)

    def toggle_joints_xray(self):
        return self._client.toggle_joints_xray()

    def on_joints_xray(self):
        return self._client.set_joints_xray(True)

    def off_joints_xray(self):
        return self._client.set_joints_xray(False)

    def joint_display_size(self):
        joints_display_size = self._model.joints_display_size
        return self._client.set_joints_display_size(joints_display_size)

    def select_hierarchy(self):
        return self._client.select_hierarchy()

    def orient_joints(self):
        return self._client.orient_joints()

    def orient_all_joints(self):
        return self._client.orient_all_joints()

    def orient_selected_joints(self):
        return self._client.orient_selected_joints()

    def add_orient_data(self):
        return self._client.add_orient_data()

    def add_orient_data_all_joints(self):
        return self._client.add_orient_data_all_joints()

    def add_orient_data_selected_joints(self):
        return self._client.add_orient_data_selected_joints()

    def clean_orient_data(self):
        return self._client.clean_orient_data()

    def clean_orient_data_all_joints(self):
        return self._client.clean_orient_data_all_joints()

    def clean_orient_data_selected_joints(self):
        return self._client.clean_orient_data_selected_joints()

    def zero_joint_orient(self):
        return self._client.zero_joint_orient()

    def zero_joint_orient_all_joints(self):
        return self._client.zero_joint_orient_all_joints()

    def zero_joint_orient_selected_joints(self):
        return self._client.zero_joint_orient_selected_joints()

    def orient_tool(self):
        return self._client.orient_tool()

    def mirror_joints(self):
        return self._client.mirror_joints()

    def mirror_all_joints(self):
        return self._client.mirror_all_joints()

    def mirror_selected_joints(self):
        return self._client.mirror_selected_joints()

    def mirror_hierarchy_joints(self):
        return self._client.mirror_hierarchy_joints()
