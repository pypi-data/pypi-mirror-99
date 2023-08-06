#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""
Module that contains Control CV position data implementation for Maya
"""

from __future__ import print_function, division, absolute_import

from tpDcc import dcc

from tpRigToolkit.data import controlcv


class ControlCVsLibMaya(controlcv.BaseControlCVsLib):
    def __init__(self):
        super(ControlCVsLibMaya, self).__init__()

    # ==============================================================================================
    # OVERRIDES
    # ==============================================================================================

    def _get_curve_transform(self, curve):
        parent = curve
        if dcc.node_exists(curve):
            if dcc.node_type(curve) == 'nurbsCurve':
                parent = dcc.node_parent(curve)
            else:
                parent = curve

        return parent
