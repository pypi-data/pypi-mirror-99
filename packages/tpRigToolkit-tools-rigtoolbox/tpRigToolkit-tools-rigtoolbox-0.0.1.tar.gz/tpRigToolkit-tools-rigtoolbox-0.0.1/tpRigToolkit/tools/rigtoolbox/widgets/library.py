#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""
Module that contains basic library implementation
"""

from __future__ import print_function, division, absolute_import

from Qt.QtCore import QObject, Signal


class _CommandSignals(QObject, object):

    command = None

    startCommand = Signal(str)
    progressCommand = Signal(int, str)
    endCommand = Signal(bool)


Command = _CommandSignals()
