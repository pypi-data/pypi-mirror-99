#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""
Module that contains implementation for info command widget
"""

from __future__ import print_function, division, absolute_import

from Qt.QtCore import Qt, Property
from Qt.QtWidgets import QSizePolicy, QWidget, QFrame, QPlainTextEdit, QTextEdit

from tpDcc.managers import resources
from tpDcc.libs.resources.core import theme
from tpDcc.libs.qt.core import base
from tpDcc.libs.qt.widgets import layouts, message, expandables, dividers


@theme.mixin
class InfoMessage(base.BaseWidget, object):
    def __init__(self, name='', description='', instructions='', parent=None):
        self._name = ''
        self._description = ''
        self._instructions = instructions

        super(InfoMessage, self).__init__(parent)

        self.setAttribute(Qt.WA_StyledBackground)
        self.theme_type = message.MessageTypes.INFO
        self.style().polish(self)
        self.name = name
        self.description = description
        self.instructions = instructions

    # =================================================================================================================
    # PROPERTIES
    # =================================================================================================================

    def _get_name(self):
        return self._name

    def _set_name(self, name):
        self._name = str(name)
        self._expandable_frame.set_title(self._name)

    def _get_description(self):
        return self._description

    def _set_description(self, text):
        self._description = str(text)
        self._description_text.setPlainText(self._description)

    def _get_instructions(self):
        return self._instructions

    def _set_instructions(self, instructions):
        self._instructions = str(instructions)
        self._instructions_text.clear()
        self._instructions_text.insertHtml(instructions)
        self._instructions_widget.setVisible(bool(instructions))

    name = Property(str, _get_name, _set_name)
    description = Property(str, _get_description, _set_description)
    instructions = Property(str, _get_instructions, _set_instructions)

    # =================================================================================================================
    # OVERRIDES
    # =================================================================================================================

    def ui(self):
        super(InfoMessage, self).ui()

        self.setMaximumHeight(150)

        info_icon = resources.icon('info')
        self._expandable_frame = expandables.ExpandableFrame(icon=info_icon, parent=self)
        self._expandable_frame.setFrameStyle(QFrame.StyledPanel | QFrame.Raised)

        expandable_layout = layouts.HorizontalLayout(margins=(2, 2, 2, 2))

        texts_layout = layouts.HorizontalLayout(spacing=0, margins=(0, 0, 0, 0))
        self._description_text = QPlainTextEdit(parent=self)
        self._description_text.setReadOnly(True)
        self._description_text.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Maximum)
        self._description_text.setFocusPolicy(Qt.NoFocus)
        self._description_text.setFrameShape(QFrame.NoFrame)
        self._instructions_widget = QWidget()
        instructions_layout = layouts.VerticalLayout(spacing=2, margins=(0, 0, 0, 0))
        self._instructions_widget.setLayout(instructions_layout)
        self._instructions_text = QTextEdit(parent=self)
        self._instructions_text.setReadOnly(True)
        self._instructions_text.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Maximum)
        self._instructions_text.setFocusPolicy(Qt.NoFocus)
        self._instructions_text.setFrameShape(QFrame.NoFrame)
        self._instructions_widget.setVisible(False)
        # self._instructions_text.insertHtml("<ul><li>text 1</li><li>text 2</li><li>text 3</li></ul> <br />")
        instructions_layout.addWidget(dividers.Divider('Instructions'))
        instructions_layout.addWidget(self._instructions_text)
        texts_layout.addWidget(self._description_text)
        texts_layout.addWidget(self._instructions_widget)

        content_layout = layouts.VerticalLayout()
        content_layout.addLayout(texts_layout)
        expandable_layout.addLayout(content_layout)

        self._expandable_frame.addLayout(expandable_layout)

        self.main_layout.addWidget(self._expandable_frame)
