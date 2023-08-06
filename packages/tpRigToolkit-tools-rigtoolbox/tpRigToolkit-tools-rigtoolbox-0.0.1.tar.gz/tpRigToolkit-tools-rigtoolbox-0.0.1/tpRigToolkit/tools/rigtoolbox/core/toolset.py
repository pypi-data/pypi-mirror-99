#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Collection of rigging tools
"""

from __future__ import print_function, division, absolute_import

__author__ = "Tomas Poveda"
__license__ = "MIT"
__maintainer__ = "Tomas Poveda"
__email__ = "tpovedatd@gmail.com"

import os
import logging

from Qt.QtCore import Qt
from Qt.QtWidgets import QSizePolicy, QToolButton, QMainWindow

from tpDcc.managers import resources
from tpDcc.libs.python import yamlio
from tpDcc.libs.qt.core import base
from tpDcc.libs.qt.widgets import window, toolset, progressbar, dock, message, buttons

from tpRigToolkit.tools.rigtoolbox.core import consts
from tpRigToolkit.tools.rigtoolbox.widgets import dock, library, base as base_widgets

LOGGER = logging.getLogger(consts.TOOL_ID)


class RigToolboxToolset(toolset.ToolsetWidget, object):
    def __init__(self, *args, **kwargs):
        super(RigToolboxToolset, self).__init__(*args, **kwargs)

    def help_mode(self, flag):
        if not flag:
            return

        help_event = toolset.ToolsetHelpEvent(
            self._rig_toolbox_widget.main_layout, self._toolbox_widgets, self._help_widget)

        return help_event

    def contents(self):
        dcc_name, dcc_version, _ = self.client.get_dcc_info()

        self.client.load_plugins()

        commands_datas = dict()
        if dcc_name:
            commands_path = os.path.join(
                os.path.abspath(os.path.dirname(os.path.dirname(__file__))), 'dccs', dcc_name, 'commands')
            if os.path.isdir(commands_path):
                for command_file in os.listdir(commands_path):
                    if not command_file.endswith('.yaml'):
                        continue
                    commands_category = os.path.splitext(command_file)[0]
                    if commands_category in commands_datas:
                        continue
                    command_file_path = os.path.join(commands_path, command_file)
                    try:
                        commands_data = yamlio.read_file(command_file_path, maintain_order=True)
                    except Exception as exc:
                        LOGGER.error(
                            'Error while reading commands data from "{}" : {}'.format(command_file_path, exc))
                        continue
                    commands_datas[commands_category] = commands_data

        # Load widgets
        self._rig_toolbox_widget = RigToolboxWidget(parent=self)
        self._toolbox_widgets = list()
        if not dcc_name:
            from tpRigToolkit.tools.rigtoolbox.widgets import base
            toolbox_widget = base.BaseRigToolBoxWidget(title='Hello World!', parent=self)
            self._toolbox_widgets.append(toolbox_widget)

        if self.client.is_maya():
            from tpRigToolkit.tools.rigtoolbox.dccs import maya
            self._toolbox_widgets = maya.get_toolbox_widgets(
                client=self.client, commands_data=commands_datas, parent=self)
        self._rig_toolbox_widget.load_widgets(self._toolbox_widgets, parent=self)

        library.Command.startCommand.connect(self._rig_toolbox_widget._on_start_command)
        library.Command.progressCommand.connect(self._rig_toolbox_widget._on_set_progress_command)
        library.Command.endCommand.connect(self._rig_toolbox_widget._on_end_command)
        # self.helpModeChanged.connect(rig_toolbox_widget.set_info_mode)

        return [self._rig_toolbox_widget]

    def reload_theme(self, theme=None):
        super(RigToolboxToolset, self).reload_theme(theme)

        if not theme:
            return
        stylesheet = theme.stylesheet()
        self._rig_toolbox_widget._base_window.setStyleSheet(stylesheet)


class RigToolboxWidget(base.BaseWidget, object):

    WindowName = 'RigToolBoxWidgetsWindow'

    def __init__(self, parent=None):
        super(RigToolboxWidget, self).__init__(parent=parent)

    def ui(self):
        super(RigToolboxWidget, self).ui()

        self._base_window = window.BaseWindow(parent=self)
        self._base_window.centralWidget().hide()
        self._base_window.setDockOptions(
            QMainWindow.AnimatedDocks | QMainWindow.AllowNestedDocks | QMainWindow.AllowTabbedDocks)
        self._base_window.setWindowFlags(Qt.Widget)

        self._progress = progressbar.BaseProgressBar(parent=self)
        self._progress.setMinimum(0)
        self._progress.setMaximum(100)

        self.main_layout.addWidget(self._base_window)
        self.main_layout.addWidget(self._progress)

    def load_widgets(self, widgets, parent=None):
        for w in widgets:
            if isinstance(w, base_widgets.BaseRigToolBoxWidget):
                w.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
                w.emitInfo.connect(self._on_show_success)
                w.emitError.connect(self._on_show_error)
                dock_widget = dock.DockWidget(w.title, parent=parent or self)
                info_button = QToolButton(parent=parent or self)
                info_button.setCheckable(True)
                info_button.setChecked(True)
                info_button.setIcon(resources.icon('info', theme='color'))
                if hasattr(w, '_on_toggle_info'):
                    info_button.toggled.connect(w._on_toggle_info)
                dock_widget.add_button(info_button)
            else:
                dock_widget = dock.DockWidget(w.objectName(), parent=parent or self)

            dock_widget.setWidget(w)
            self._base_window.addDockWidget(Qt.TopDockWidgetArea, dock_widget)

    def _on_start_command(self, command_name):
        library.Command.command = command_name
        self._progress.setFormat('Executing command: "{}"'.format(command_name))
        self._progress.setValue(0)
        self._progress.theme_status = progressbar.BaseProgressBar.NORMAL_STATUS

    def _on_set_progress_command(self, value, msg=None):
        current_command = library.Command.command
        if not current_command:
            return

        self._progress.setValue(value)
        if msg:
            self._progress.setFormat(msg)

    def _on_end_command(self, was_success):
        current_command = library.Command.command
        if not current_command:
            return
        if was_success:
            self._progress.setFormat('Command "{}" executed successfully!'.format(current_command))
            self._progress.theme_status = progressbar.BaseProgressBar.SUCCESS_STATUS
        else:
            self._progress.setFormat('Error while executing command "{}"!'.format(current_command))
            self._progress.theme_status = progressbar.BaseProgressBar.ERROR_STATUS
        self._progress.setValue(100)
        library.Command.command = None

    def _on_show_success(self, success_message):
        message.PopupMessage.success(success_message, self, closable=True)

    def _on_show_error(self, error_message):
        message.PopupMessage.error(error_message, self, closable=True)
