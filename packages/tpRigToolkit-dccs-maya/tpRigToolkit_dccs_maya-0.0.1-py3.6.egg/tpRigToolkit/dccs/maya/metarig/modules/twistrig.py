#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""
Module that contains twist rig implementation for metarig in Maya
"""

from __future__ import print_function, division, absolute_import

import logging

from tpDcc import dcc
from tpDcc.dccs.maya.core import transform as xform_utils

from tpRigToolkit.dccs.maya.metarig.core import module, mixin
from tpRigToolkit.dccs.maya.metarig.components import twistribbon

logger = logging.getLogger('tpRigToolkit-dccs-maya')


class TwistRig(module.RigModule, mixin.JointMixin):
    def __init__(self, *args, **kwargs):
        super(TwistRig, self).__init__(*args, **kwargs)

        if self.cached:
            return

        mixin.JointMixin.__init__(self)
        self.set_name(kwargs.get('name', 'twistRig'))
        self.set_control_count(5)
        self.set_offset_axis('Y')
        self.set_attach_directly(True)
        self.set_top_twist_fix(True)
        self.set_bottom_twist_fix(True)
        self.set_orient_example(None)

    # ==============================================================================================
    # OVERRIDES
    # ==============================================================================================

    def create(self, *args, **kwargs):
        super(TwistRig, self).create(*args, **kwargs)

        joints = self.get_joints()
        if not joints:
            logger.warning('No joint defined to create twist rig for')
            return False

        for joint in joints:
            next_joint = dcc.list_relatives(joint.meta_node, relative_type='joint')
            next_joint = next_joint[0] if next_joint else None
            if not next_joint:
                continue

            length = dcc.distance_between_transforms(joint.meta_node, next_joint)

            self.orient_example = self.orient_example or joint

            twist_component = twistribbon.TwistRibbon(name='twistRibbon')
            self.add_component(twist_component)
            twist_component.set_joint(joint)
            twist_component.set_joint_count(self.control_count)
            twist_component.set_offset_axis(self.offset_axis)
            twist_component.set_attach_directly(self.attach_directly)
            twist_component.set_top_twist_fix(self.top_twist_fix)
            twist_component.set_bottom_twist_fix(self.bottom_twist_fix)
            twist_component.set_ribbon_offset(length / 4.0)
            twist_component.set_dual_quaternion(False)
            bad_axis = xform_utils.get_axis_letter_aimed_at_child(joint.meta_node)
            if bad_axis in ('X', '-X'):
                twist_component.set_offset_axis('Z')
            elif bad_axis in ('Y', '-Y'):
                twist_component.set_offset_axis('X')
            elif bad_axis in ('Z', '-Z'):
                twist_component.set_offset_axis('X')
            else:
                logger.warning('Was not possible to retrieve offset axis from joint "{}"'.format(joint))
            twist_component.create()
            # dcc.set_attribute_value(twist_component.surface.meta_node, 'inheritsTransform', False)

        return True

    # ==============================================================================================
    # BASE
    # ==============================================================================================

    def set_control_count(self, control_count):
        if not self.has_attr('control_count'):
            self.add_attribute(attr='control_count', value=control_count - 1)
        else:
            self.control_count = control_count - 1

    def set_orient_example(self, orient_example):
        if not self.has_attr('orient_example'):
            self.add_attribute(attr='orient_example', value=orient_example, attr_type='messageSimple')
        else:
            self.orient_example = orient_example

    def set_offset_axis(self, offset_axis):
        if not self.has_attr('offset_axis'):
            self.add_attribute(attr='offset_axis', value=offset_axis)
        else:
            self.offset_axis = offset_axis

    def set_attach_directly(self, flag):
        if not self.has_attr('attach_directly'):
            self.add_attribute(attr='attach_directly', value=flag)
        else:
            self.attach_directly = flag

    def set_top_twist_fix(self, flag):
        if not self.has_attr('top_twist_fix'):
            self.add_attribute(attr='top_twist_fix', value=flag)
        else:
            self.top_twist_fix = flag

    def set_bottom_twist_fix(self, flag):
        if not self.has_attr('bottom_twist_fix'):
            self.add_attribute(attr='bottom_twist_fix', value=flag)
        else:
            self.bottom_twist_fix = flag
