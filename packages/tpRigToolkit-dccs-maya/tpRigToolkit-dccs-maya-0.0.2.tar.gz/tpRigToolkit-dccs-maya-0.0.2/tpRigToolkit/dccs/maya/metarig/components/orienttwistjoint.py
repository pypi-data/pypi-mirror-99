#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""
Module that contains twist ribbon rig component implementation
Ribbon with rivets attached to it
"""

from __future__ import print_function, division, absolute_import

import logging

from tpDcc import dcc
from tpDcc.libs.python import mathlib
from tpDcc.dccs.maya.core import transform as xform_utils, joint as joint_utils
from tpDcc.dccs.maya.meta import metanode

from tpRigToolkit.dccs.maya.metarig.core import component, mixin

logger = logging.getLogger('tpRigToolkit-dccs-maya')


class OrientTwistJoint(component.RigComponent, mixin.JointMixin):
    def __init__(self, *args, **kwargs):
        super(OrientTwistJoint, self).__init__(*args, **kwargs)

        if self.cached:
            return

        mixin.JointMixin.__init__(self)
        self.set_name(kwargs.get('name', 'orientTwistJoint'))
        self.set_twist_joints_count(4)
        self.set_twist_driver(None)
        self.set_twist_driven(None)
        self.set_twist_joint(None)
        self.set_reverse_orient(False)

    # =================================================================================================================
    # OVERRIDES
    # =================================================================================================================

    def create(self):
        super(OrientTwistJoint, self).create()

        joints = self.get_joints()
        if not self.twist_driver:
            if joints:
                self.set_twist_driver(joints[0])
        if not self.twist_driver:
            logger.warning(
                'Impossible to create rig: \n\tname: {}\n\tside: {}\n\twarning: No driver joint defined'.format(
                    self.name, self.side))
            return

        if not self.twist_driver:
            children = dcc.list_relatives(self.twist_driver.meta_node, children_type='joint')
            if not children:
                logger.warning(
                    'Impossible to create rig: \n\tname: {}\n\tside: {}\n\twarning: No twist driven defined'.format(
                        self.name, self.side))
                return

            self.set_twist_driven(metanode.validate_obj_arg(children[0], 'MetaObject', update_class=True))

        self._create_twist_joints()
        self._connect_twist_joints()

    # =================================================================================================================
    # BASE
    # =================================================================================================================

    def get_twist_joints(self, as_meta=True):
        """
        Returns a list of all created twist joints
        :return: list(str or MetaObject)
        """

        return self.message_list_get('twist_joints', as_meta=as_meta)

    def set_twist_joints_count(self, twist_joints_count):
        """
        Sets the total number of twist joints to create
        :param twist_joints_count: int
        """

        if not self.has_attr('twist_joints_count'):
            self.add_attribute(attr='twist_joints_count', value=twist_joints_count)
        else:
            self.twist_joints_count = twist_joints_count

    def set_twist_driver(self, twist_driver):
        """
        Sets the joint that drives the joint rotation.
        The rotation near this joint will be maximum and will decrease while it arrives to the driven joint
        :param twist_driver: MetaObject
        """

        if not self.has_attr('twist_driver'):
            self.add_attribute(attr='twist_driver', value=twist_driver, attr_type='messageSimple')
        else:
            self.twist_driver = twist_driver

    def set_twist_driven(self, twist_driven):
        """
        Sets the driven joint. This joint will have no twist rotation. But all the joints between this joint and the
        driver joint will twist proportionately to the distance
        :param twist_driven: MetaObject
        """

        if not self.has_attr('twist_driven'):
            self.add_attribute(attr='twist_driven', value=twist_driven, attr_type='messageSimple')
        else:
            self.twist_driven = twist_driven

    def set_twist_joint(self, twist_joint):
        """
        Sets the joint used as reference to create the twist joints (twist joints will be aligned in rotation to this
        joint during their creation). If no twist joint is deifned, driver joint will be used.
        Useful in scenarios where the joint driver has multiple children and is not possible to automatically find
        a proper twist axis from it (for example, when setting forearm twist setups).
        :param twist_joint: MetaObject
        """

        if not self.has_attr('twist_joint'):
            self.add_attribute(attr='twist_joint', value=twist_joint, attr_type='messageSimple')
        else:
            self.twist_joint = twist_joint

    def set_reverse_orient(self, flag):
        """
        Sets whether or not twist is applied from driver to driven or viceversa
        :param flag: bool
        """

        if not self.has_attr('reverse_orient'):
            self.add_attribute(attr='reverse_orient', value=flag)
        else:
            self.reverse_orient = flag

    # =================================================================================================================
    # INTERNAL
    # =================================================================================================================

    def _get_twist_axis(self, as_letter=False):
        """
        Internal function that returns twist axis that twist joints will use
        :param as_letter: bool, whether to return the axis as a letter or as a tuple of floats
        :return: str or list(float, float, float)
        """

        if self.twist_joint:
            twist_joint = self.twist_joint
        else:
            twist_joint = self.twist_driver
            driver_children = dcc.list_children(twist_joint.meta_node)
            if not driver_children:
                twist_joint = self.twist_driven

        if as_letter:
            return xform_utils.get_axis_letter_aimed_at_child(twist_joint.meta_node)
        else:
            return xform_utils.get_axis_aimed_at_child(twist_joint.meta_node)

    def _create_twist_joints(self):
        """
        Internal function that creates twist joints
        """

        distance = dcc.distance_between_nodes(self.twist_driver.meta_node, self.twist_driven.meta_node)
        distance_ratio = distance / (self.twist_joints_count - 1)
        twist_axis = self._get_twist_axis()

        root_node = dcc.node_parent(self.twist_driver.meta_node, full_path=False)
        if root_node == dcc.node_short_name(self.twist_driven.meta_node):
            twist_axis = (mathlib.Vector(*twist_axis) * -1.0).list()

        twist_joints = list()
        for i in range(self.twist_joints_count):
            dcc.clear_selection()
            twist_joint = dcc.create_joint(self._get_name('roll', id=i, node_type='joint'), size=self.scale)
            dcc.match_rotation((self.twist_joint or self.twist_driver).meta_node, twist_joint)
            dcc.match_translation(self.twist_driver.meta_node, twist_joint)
            joint_utils.OrientJointAttributes.zero_orient_joint(twist_joint)
            if self.reverse_orient:
                twist_joint = dcc.set_parent(twist_joint, self.twist_driven.meta_node)
            else:
                twist_joint = dcc.set_parent(twist_joint, self.twist_driver.meta_node)

            new_distance = mathlib.Vector(*twist_axis) * (distance_ratio * i)
            dcc.translate_node_in_object_space(twist_joint, new_distance.list(), relative=True)
            twist_joint = metanode.validate_obj_arg(twist_joint, 'MetaObject', update_class=True)
            twist_joints.append(twist_joint)

        self.message_list_connect('twist_joints', twist_joints)

    def _connect_twist_joints(self):
        """
        Internal function that connects twist setup
        """

        # orient locator will be used to retrieve a "clean" orientation value in the twist axis no matter how we
        # rotate the end joint of the twist chain.
        orient_locator = dcc.create_locator(name=self._get_name('orient', node_type='locator', unique_name=True))
        fixed_locator = dcc.create_locator(name=self._get_name('fixed', node_type='locator', unique_name=True))
        dcc.match_translation_rotation(self.twist_driver.meta_node, orient_locator)
        dcc.match_translation_rotation(self.twist_driver.meta_node, fixed_locator)
        fixed_locator = dcc.set_parent(fixed_locator, dcc.node_parent(self.twist_driver.meta_node))
        orient_locator = dcc.set_parent(orient_locator, fixed_locator)
        orient_locator = metanode.validate_obj_arg(orient_locator, 'MetaObject', update_class=True)
        fixed_locator = metanode.validate_obj_arg(fixed_locator, 'MetaObject', update_class=True)
        self.add_attribute(attr='orient_locator', value=orient_locator, attr_type='messageSimple')
        self.add_attribute(attr='fixed_locator', value=fixed_locator, attr_type='messageSimple')

        for axis in 'XYZ':
            dcc.set_attribute_value(self.orient_locator.meta_node, 'localScale{}'.format(axis), self.scale)
            dcc.set_attribute_value(self.fixed_locator.meta_node, 'localScale{}'.format(axis), self.scale)

        # as the orient constraint is parented to the local constraint and both locators have the same transforms
        # the orient locator channels are completely clean. We use orient locator to retrieve a clean rotation of
        # the twist driver joint
        orient_constraint = dcc.create_orient_constraint(self.orient_locator.meta_node, self.twist_driver.meta_node)
        # we set the constraint interpolation type to average to avoid joint flipping
        dcc.set_attribute_value(orient_constraint, 'interpType', 1)

        axis_letter = self._get_twist_axis(as_letter=True)
        if len(axis_letter) > 1:
            axis_letter = axis_letter[-1]

        twist_value = -1
        loop_joints = self.get_twist_joints()
        twist_joints_count = len(loop_joints)
        if self.reverse_orient:
            loop_joints = list(reversed(loop_joints))

        for i, twist_joint in enumerate(loop_joints):
            multiply_divide_twist = dcc.create_node(
                'multiplyDivide', node_name=self._get_name('twistJoint', id=i, node_type='multiplyDivide'))
            for axis in 'XYZ':
                input_attr = 'input2{}'.format(axis)
                if axis == axis_letter.upper():
                    if self.reverse_orient:
                        dcc.set_attribute_value(multiply_divide_twist, input_attr, 1.0 / twist_joints_count * i)
                    else:
                        dcc.set_attribute_value(multiply_divide_twist, input_attr, twist_value)
                else:
                    dcc.set_attribute_value(multiply_divide_twist, input_attr, 0.0)
            dcc.connect_attribute(
                self.orient_locator.meta_node, 'rotate', multiply_divide_twist, 'input1')
            dcc.connect_attribute(multiply_divide_twist, 'output', twist_joint.meta_node, 'rotate')
            twist_value += 1.0 / (self.twist_joints_count - 1)
