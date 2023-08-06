#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""
Module that contains widget with geometry functionality
"""

from __future__ import print_function, division, absolute_import

import logging

from Qt.QtCore import QObject

from tpDcc.libs.qt.core import qtutils

from tpRigToolkit.tools.rigtoolbox.widgets import base

LOGGER = logging.getLogger('tpRigToolkit-tools-rigtoolbox')


class GeneralWidget(base.CommandRigToolBoxWidget, object):

    def __init__(self, client, commands_data, parent=None):

        self._model = GeneralWidgetModel()

        super(GeneralWidget, self).__init__(
            title='General', commands_data=commands_data,
            controller=GeneralWidgetController(model=self._model, client=client), parent=parent)


class GeneralWidgetModel(QObject, object):
    def __init__(self):
        super(GeneralWidgetModel, self).__init__()


class GeneralWidgetController(object):

    def __init__(self, model, client):
        super(GeneralWidgetController, self).__init__()

        self._model = model
        self._client = client

    @property
    def model(self):
        return self._model

    @property
    def client(self):
        return self._client

    def delete_history(self):
        return self._client.delete_history()

    def freeze_transforms(self):
        return self._client.freeze_transforms()

    def move_pivot_to_zero(self):
        return self._client.move_pivot_to_zero()

    def lock_all_transforms(self):
        return self._client.lock_all_transforms()

    def lock_translation(self):
        return self._client.lock_translation()

    def lock_rotation(self):
        return self._client.lock_rotation()

    def lock_scale(self):
        return self._client.lock_scale()

    def lock_visibility(self):
        return self._client.lock_visibility()

    def unlock_all_transforms(self):
        return self._client.unlock_all_transforms()

    def unlock_translation(self):
        return self._client.unlock_translation()

    def unlock_rotation(self):
        return self._client.unlock_rotation()

    def unlock_scale(self):
        return self._client.unlock_scale()

    def unlock_visibility(self):
        return self._client.unlock_visibility()

    def clean_student_license(self):
        return self._client.clean_student_license()

    def match_transform(self):
        return self._client.match_transform()

    def match_translation(self):
        return self._client.match_translation()

    def match_rotation(self):
        return self._client.match_rotation()

    def match_scale(self):
        return self._client.match_scale()

    def combine_meshes(self):
        new_mesh_name = None
        if qtutils.is_shift_modifier():
            new_mesh_name = qtutils.get_string_input('Combine Mesh Name', title='Combine Mesh')

        return self._client.combine_meshes(new_mesh_name=new_mesh_name)

    def separate_meshes(self):
        return self._client.separate_meshes()

    def mirror_meshes(self):
        return self._client.mirror_meshes()

    def mirror_meshes_options(self):
        return self._client.mirror_meshes_options()

    def open_symmetry_tool(self):
        return self._client.open_symmetry_tool()

    def detach_components(self):
        return self._client.detach_components()

    def curve_from_edge_loop(self):
        return self._client.curve_from_edge_loop()
