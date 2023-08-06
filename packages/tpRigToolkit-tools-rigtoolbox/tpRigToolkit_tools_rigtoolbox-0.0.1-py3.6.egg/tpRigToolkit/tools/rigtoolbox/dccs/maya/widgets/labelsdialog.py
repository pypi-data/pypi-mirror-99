#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""
Module that contains dialog to assign labels to joints
"""

from __future__ import print_function, division, absolute_import

from Qt.QtCore import Qt, Signal, QObject
from Qt.QtWidgets import QDialogButtonBox, QMessageBox

from tpDcc.libs.qt.core import qtutils
from tpDcc.libs.qt.widgets import layouts, dialog, label, lineedit, dividers, message


class JointsLabelDialog(dialog.BaseDialog, object):
    def __init__(self, parent=None):

        self._model = JointsLabelModel()
        self._controller = JointsLabelController(model=self._model)

        super(JointsLabelDialog, self).__init__(
            title='Joints Label Dialog', size=(200, 50), frameless=True, parent=parent
        )

        self._dragger._button_closed.setVisible(False)
        self.refresh()
        self.setFixedHeight(250)
        self.setFixedWidth(300)

    def ui(self):
        super(JointsLabelDialog, self).ui()

        name_label = label.BaseLabel('Specify label sides', parent=self)
        left_side_label = label.BaseLabel('Left Side: ', parent=self)
        self._left_side_line = lineedit.BaseLineEdit(parent=self)
        right_side_label = label.BaseLabel('Right Side: ', parent=self)
        self._right_side_line = lineedit.BaseLineEdit(parent=self)

        info_widget = message.BaseMessage(
            'You can disable auto joint label in tool\n button options (right click on it', parent=self).info()

        grid_layout = layouts.GridLayout()
        grid_layout.addWidget(name_label, 0, 0, 1, 2)
        grid_layout.addWidget(left_side_label, 1, 0, Qt.AlignRight)
        grid_layout.addWidget(self._left_side_line, 1, 1)
        grid_layout.addWidget(right_side_label, 2, 0, Qt.AlignRight)
        grid_layout.addWidget(self._right_side_line, 2, 1)

        self._button_box = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)

        self.main_layout.addLayout(grid_layout)
        self.main_layout.addWidget(dividers.Divider())
        self.main_layout.addWidget(self._button_box)
        self.main_layout.addWidget(dividers.Divider())
        self.main_layout.addWidget(info_widget)

    def setup_signals(self):
        self._left_side_line.textChanged.connect(self._controller.set_left_side)
        self._right_side_line.textChanged.connect(self._controller.set_right_side)
        self._button_box.accepted.connect(self._on_accept)
        self._button_box.rejected.connect(self._on_reject)

        self._model.leftSideChanged.connect(self._left_side_line.setText)
        self._model.rightSideChanged.connect(self._right_side_line.setText)

    def refresh(self):
        self._left_side_line.setText(self._model.left_side)
        self._right_side_line.setText(self._model.right_side)

    def get_sides(self):
        return self._model.left_side, self._model.right_side

    def _on_accept(self):
        valid_verify = self._controller.verify()
        if valid_verify:
            self.accept()
            return True

        res = qtutils.show_warning(
            self, 'Missing side data', 'Please fill both side fields. Do you want to continue with default settings?')
        if res != QMessageBox.Yes:
            return True

        self.reject()

    def _on_reject(self):
        self._controller.set_left_side('')
        self._controller.set_right_side('')
        self.reject()


class JointsLabelModel(QObject, object):

    leftSideChanged = Signal(str)
    rightSideChanged = Signal(str)

    def __init__(self):
        super(JointsLabelModel, self).__init__()

        self._left_side = '*_l_*'
        self._right_side = '*_r_*'

    @property
    def left_side(self):
        return self._left_side

    @left_side.setter
    def left_side(self, value):
        self._left_side = str(value)
        self.leftSideChanged.emit(self._left_side)

    @property
    def right_side(self):
        return self._right_side

    @right_side.setter
    def right_side(self, value):
        self._right_side = str(value)
        self.rightSideChanged.emit(self._right_side)


class JointsLabelController(object):
    def __init__(self, model):
        self._model = model

    @property
    def model(self):
        return self._model

    def set_left_side(self, value):
        self._model.left_side = value

    def set_right_side(self, value):
        self._model.right_side = value

    def verify(self):
        left_side = self._model.left_side
        right_side = self._model.right_side

        if left_side and right_side:
            return True

        return False
