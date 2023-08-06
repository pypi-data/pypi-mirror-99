#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""
Module that contains base class for tpRigToolbox widgets
"""

from __future__ import print_function, division, absolute_import

import time
import inspect
from functools import partial

from Qt.QtCore import Qt, Signal, QPoint, QSize, QEvent
from Qt.QtWidgets import QSizePolicy, QWidget, QFrame, QMenu, QAction, QWhatsThis
from Qt.QtGui import QCursor, QColor, QPainter, QBrush, QPolygon

from tpDcc.managers import resources
from tpDcc.libs.python import python
from tpDcc.libs.qt.core import base
from tpDcc.libs.qt.widgets import layouts, label, buttons, accordion, balloon

from tpRigToolkit.tools.rigtoolbox.widgets import library, info


class BaseRigToolBoxWidget(base.BaseFrame, object):

    emitInfo = Signal(str)
    emitWarning = Signal(str)
    emitError = Signal(str)
    setInfo = Signal(str, str, str)

    def __init__(self, title, parent=None):

        self._title = title

        super(BaseRigToolBoxWidget, self).__init__(parent=parent)

    @property
    def title(self):
        return self._title

    def get_main_layout(self):
        main_layout = layouts.VerticalLayout(spacing=0, margins=(0, 0, 0, 0))
        main_layout.setAlignment(Qt.AlignTop)

        return main_layout

    def ui(self):
        super(BaseRigToolBoxWidget, self).ui()
        self._content_layout = layouts.VerticalLayout(spacing=0, margins=(0, 0, 0, 0))

        self.main_layout.addLayout(self._content_layout)


class CommandRigToolBoxWidget(BaseRigToolBoxWidget, object):
    def __init__(self, title, commands_data, controller, parent=None):

        self._commands_data = commands_data or dict()
        self._widgets = dict()
        self._buttons = list()
        self._current_action = None
        self._controller = controller
        self._controller_functions_mapping = dict()

        super(CommandRigToolBoxWidget, self).__init__(title=title, parent=parent)

        if self._controller:
            predicate = inspect.ismethod if python.is_python2() else inspect.isfunction
            controller_functions = inspect.getmembers(self._controller.__class__, predicate=predicate)
            for controller_fn_data in controller_functions:
                if controller_fn_data[0] in ['__init__']:
                    continue
                controller_fn = getattr(self._controller, controller_fn_data[0])
                if not controller_fn:
                    continue
                self._controller_functions_mapping[controller_fn_data[0]] = controller_fn

        added_categories = list()
        for name, data in self._commands_data.items():
            categories = data.get('categories', list())
            for category in categories:
                if not category or category in added_categories:
                    continue
                category_widget = self._add_category(category)
                if not category_widget:
                    continue
                self._accordion.add_item(category, category_widget)
                added_categories.append(category)

    def ui(self):
        super(CommandRigToolBoxWidget, self).ui()

        self._info_widget = info.InfoMessage(parent=self)
        self._info_frame = base.BaseFrame(parent=self)
        self._info_label = label.BaseLabel(parent=self).strong()
        self._info_frame.setFrameStyle(QFrame.StyledPanel | QFrame.Raised)
        info_frame_layout = layouts.HorizontalLayout(spacing=0, margins=(0, 0, 0, 0))
        info_frame_layout.addStretch()
        info_frame_layout.addWidget(self._info_label)
        info_frame_layout.addStretch()
        self._info_frame.main_layout.addLayout(info_frame_layout)
        self._info_frame.setVisible(False)

        self._accordion = accordion.AccordionWidget(parent=self)
        self._content_layout.addWidget(self._accordion)

        self.main_layout.addWidget(self._info_widget)
        self.main_layout.addWidget(self._info_frame)

    def eventFilter(self, obj, event):

        if isinstance(obj, QMenu):
            if event.type() == QEvent.MouseMove:
                action = obj.actionAt(event.pos())
                if action:
                    if action != self._current_action:
                        self._current_action = action
                        name = action.property('name') or action.text()
                        description = action.property('description') or ''
                        instructions = action.property('instructions') or ''
                        self._set_info(name, description, instructions)

                        self.setInfo.emit(name, description, instructions)
            if event.type() == QEvent.HoverLeave or event.type() == QEvent.Leave:
                self._set_info('', '', '')
                self._current_action = None
        else:
            if event.type() == QEvent.HoverEnter:
                name = obj.property('name') or obj.text()
                description = obj.property('description') or ''
                instructions = obj.property('instructions') or ''
                self._set_info(name, description, instructions)
            elif event.type() == QEvent.HoverLeave:
                self._set_info('', '', '')

        return super(BaseRigToolBoxWidget, self).eventFilter(obj, event)

    def _add_category(self, category_name):
        if not self._controller:
            return False

        commands_to_add = list()

        for command_name, command_data in self._commands_data.items():
            command_function = self._controller_functions_mapping.get(command_name, None)
            if not command_data or command_name not in self._controller_functions_mapping:
                continue
            command_categories = command_data.get('categories', list())
            if category_name not in command_categories:
                continue
            options = list()
            command_actions = command_data.get('options', dict())
            for command_option_name, command_option_data in command_actions.items():
                command_option_function = self._controller_functions_mapping.get(command_option_name, None)
                if not command_option_function:
                    continue
                option_data = command_option_data.copy()
                option_data['fn'] = command_option_function
                options.append(option_data)

            new_command_data = command_data.copy()
            new_command_data.pop('categories')       # categories is not part of the command creation
            new_command_data.pop('options', None)
            new_command = self._create_button(fn=command_function, settings=options, **new_command_data)

            is_available = self._check_command_availability(command_name)
            if not is_available:
                new_command.setToolTip('Command "{}" is not available!'.format(command_name))
                new_command.setEnabled(False)

            commands_to_add.append(new_command)

        if not commands_to_add:
            return False

        category_widget = QWidget()
        category_layout = layouts.FlowLayout()
        category_layout.setAlignment(Qt.AlignLeft)
        category_widget.setLayout(category_layout)

        for command in commands_to_add:
            category_layout.addWidget(command)

        return category_widget

    def _check_command_availability(self, command_name):
        """
        Internal function that returns whether or not given command is available
        Should be override in custom widgets to enable/disable commands
        By default, all commands are available
        :param command_name: str
        :return: bool
        """

        return True

    def _create_button(
            self, name=None, icon=None, fn=None, status=None, tooltip=None, description=None, instructions=None,
            whats_this='', settings=None, settings_fn=None, info_message='', error_message='', widgets=None):
        """
        Internal function to easily create buttons for the box widget
        :param name:
        :param icon:
        :param fn:
        :param status:
        :param tooltip:
        :return:
        """

        name = name or ''
        new_btn = CommandButton(parent=self).small()
        if icon:
            if python.is_string(icon):
                icon = resources.icon(icon)
            new_btn.setIcon(icon)
        else:
            new_btn.setText(name)
        new_btn.setObjectName(name.replace(' ', '').lower() or description)
        new_btn.setStatusTip(status or name)
        new_btn.setToolTip(tooltip or name)
        new_btn.setProperty('name', name)
        new_btn.setProperty('description', description or tooltip or status or '')
        new_btn.setProperty('instructions', instructions or '')
        new_btn.setProperty('tooltip_help', {'title': name, 'description': description})
        new_btn.setStyleSheet('qproperty-iconSize: 20px 20px;')
        new_btn.setIconSize(QSize(20, 20))
        new_btn.setWhatsThis(whats_this or tooltip or name)
        new_btn.setContextMenuPolicy(Qt.CustomContextMenu)
        new_btn.installEventFilter(self)
        if widgets:
            valid_widgets = list()
            for widget in widgets:
                if hasattr(self, widget):
                    valid_widgets.append(getattr(self, widget))
            if valid_widgets:
                self._widgets[new_btn.objectName()] = valid_widgets
                new_btn.has_menu = True

        if fn:
            info_message = info_message or 'Command "{}" executed successfully!'.format(name)
            error_message = error_message or 'Error while executing command "{}"! Check log for more info.'.format(name)
            new_btn.clicked.connect(partial(self._on_execute_command, name, fn, info_message, error_message))
        new_btn.customContextMenuRequested.connect(self._on_show_context_menu)

        if settings:
            settings_icon = 'menu_dots' if settings and len(settings) > 1 else 'settings'
            buttons_widget = QWidget()
            buttons_widget.setStyleSheet('QPushButton::menu-indicator{ image: none; };')
            buttons_layout = layouts.HorizontalLayout(spacing=0, margins=(0, 0, 0, 0))
            buttons_widget.setLayout(buttons_layout)

            if len(settings) > 1:
                options_name = '{} Options'.format(name)
                options_description = 'Show {} Menu'.format(options_name)
                options_btn = self._create_button(
                    icon=settings_icon, fn=settings_fn, name=options_name, description=options_description)
                options_menu = QMenu(self)
                options_menu.installEventFilter(self)
                options_btn.setMenu(options_menu)
                for setting in settings:
                    option_name = setting.get('name', None)
                    if not option_name:
                        continue
                    option_fn = setting.get('fn', None)
                    if not option_fn:
                        continue
                    option_description = setting.get('description', '')
                    option_instructions = setting.get('instructions', '')
                    option_icon = resources.icon(setting.get('icon', 'tpRigToolkit'))
                    option_action = QAction(option_icon, option_name, self)
                    option_action.setProperty('description', option_description or '')
                    option_action.setProperty('instructions', option_instructions or '')
                    option_info_message = info_message or 'Command "{}" executed successfully!'.format(name)
                    option_error_message = error_message or 'Error while executing command "{}"! ' \
                                                            'Check log for more info.'.format(name)
                    option_action.triggered.connect(
                        partial(self._on_execute_command, option_name,
                                option_fn, option_info_message, option_error_message))

                    options_menu.addAction(option_action)
            else:
                setting = settings[0]
                option_description = setting.get('description', '')
                option_name = setting.get('name', None)
                option_fn = setting.get('fn', None)
                options_btn = self._create_button(
                    icon=settings_icon, fn=option_fn, name=option_name, description=option_description)

            new_btn.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Expanding)
            new_btn.setStyleSheet(
                new_btn.styleSheet() + ';border-top-right-radius: 0px; border-bottom-right-radius: 0px; '
                                       'border-right: 0px;')
            new_btn.setMaximumWidth(28)

            options_btn.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Expanding)
            options_btn.setMaximumWidth(18)
            options_btn.setStyleSheet(
                options_btn.styleSheet() + ';border-top-left-radius: 0px; border-bottom-left-radius: 0px; '
                                           'qproperty-iconSize: 12px 12px;')
            buttons_layout.addWidget(new_btn)
            buttons_layout.addWidget(options_btn)

            self._buttons.append(new_btn)

            return buttons_widget

        self._buttons.append(new_btn)

        return new_btn

    def _set_info(self, name, description, instructions):
        self._info_widget.name = name
        self._info_widget.description = description
        self._info_widget.instructions = instructions
        self._info_label.setText(name)

    def _on_show_whats_this(self, whats_this_text):
        pos = QCursor.pos()
        if not whats_this_text:
            return
        QWhatsThis.showText(pos, whats_this_text, self)

    def _on_show_context_menu(self):
        sender = self.sender()
        if not sender:
            return

        sender_name = sender.objectName()
        if sender_name not in self._widgets:
            return

        menu = CommandBalloon(widgets_parent=self, parent=sender)
        widgets = self._widgets[sender_name]
        for widget in widgets:
            menu.add_widget(widget)
        menu.closed.connect(partial(self._on_closed_menu, sender))
        sender.primary()
        menu.show()

        pos = menu.mapToGlobal(QPoint(menu.width() / 2, 0))
        final_pos = sender.mapFromGlobal(pos)
        menu.move(
            menu.pos().x() - final_pos.x() + sender.width() / 2, menu.pos().y() - final_pos.y() + sender.height() - 5)

        return menu

    def _on_closed_menu(self, command_button):
        command_button.default()

    def _on_toggle_info(self, flag):
        self._info_frame.setVisible(not flag)
        self._info_widget.setVisible(flag)

    def _on_execute_command(self, name, fn, info_message=None, error_message=None):
        library.Command.startCommand.emit(name)
        start_time = time.time()
        valid_fn = fn()
        end_time = time.time() - start_time
        if valid_fn and info_message:
            info_message += ' (%0.3f secs)' % end_time
            self.emitInfo.emit(info_message)
        if not valid_fn and error_message:
            self.emitError.emit(error_message)
        library.Command.endCommand.emit(bool(valid_fn))

        return valid_fn


class CommandButton(buttons.BaseButton, object):
    def __init__(self, text='', icon=None, parent=None):
        super(CommandButton, self).__init__(text=text, icon=icon, parent=parent)

        self._has_menu = False

    @property
    def has_menu(self):
        return self._has_menu

    @has_menu.setter
    def has_menu(self, flag):
        self._has_menu = flag

    def paintEvent(self, event):
        super(CommandButton, self).paintEvent(event)
        if self.has_menu:
            painter = QPainter()
            painter.begin(self)
            brush = QBrush(QColor(self.theme().accent_color))
            painter.setRenderHint(painter.Antialiasing)
            painter.setBrush(brush)
            painter.setPen(Qt.NoPen)
            w = self.rect().width() - 1
            h = self.rect().height() - 1
            polygon = QPolygon()
            polygon.append(QPoint(w - 1, h - 8))
            polygon.append(QPoint(w - 8, h - 1))
            polygon.append(QPoint(w - 1, h - 1))
            painter.drawPolygon(polygon)


class CommandBalloon(balloon.BalloonDialog, object):
    def __init__(self, widgets_parent, modal=False, parent=None):
        super(CommandBalloon, self).__init__(modal=modal, parent=parent)

        self._widgets = list()
        self._widgets_parent = widgets_parent

        self.main_layout = layouts.VerticalLayout(spacing=2, margins=(2, 2, 2, 2))
        self.setLayout(self.main_layout)

    def add_widget(self, widget):
        self.main_layout.addWidget(widget)
        widget.setVisible(True)
        self._widgets.append(widget)

    def closeEvent(self, event):
        for widget in self._widgets:
            widget.setVisible(False)
            widget.setParent(self._widgets_parent)
        super(CommandBalloon, self).closeEvent(event)
