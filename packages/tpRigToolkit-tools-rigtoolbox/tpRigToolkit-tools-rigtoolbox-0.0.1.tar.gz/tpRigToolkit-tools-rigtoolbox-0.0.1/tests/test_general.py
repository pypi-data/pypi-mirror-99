#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""
Module that contains general tests for tpRigToolkit-tools-rigtoolbox
"""

import pytest

from tpRigToolkit.tools.rigtoolbox import __version__


def test_version():
    assert __version__.get_version()
