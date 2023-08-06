#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""
Module that contains joint based twist rig
"""

from __future__ import print_function, division, absolute_import

import maya.cmds

from tpDcc import dcc
from tpDcc.libs.python import mathlib
from tpDcc.dccs.maya.core import constraint, transform as xform_utils, joint as joint_utils, ik as ik_utils

from tpRigToolkit.dccs.maya.core import rig


class OrientTwistJoint(rig.Rig):
    def __init__(self, *args, **kwargs):
        super(OrientTwistJoint, self).__init__(*args, **kwargs)

        self._twist_joints_count = kwargs.pop('twist_joints_count', 4)
        self._twist_driver = kwargs.pop('twist_driver', None)
        self._twist_driven = kwargs.pop('twist_driven', None)
        self._twist_joint = kwargs.pop('twist_joint', None)
        self._reverse_orient = kwargs.pop('reverse_orient', False)

        self._twist_joints = list()
        self._fixed_locator = None
        self._orient_locator = None

    # =================================================================================================================
    # PROPERTIES
    # =================================================================================================================

    @property
    def twist_driver(self):
        """
        Returns the joint that drives the twist rotation. The rotation near this will be maximum and will decrease
        while it arrives into the driven joint
        :return: str
        """

        return self._twist_driver

    @twist_driver.setter
    def twist_driver(self, driver_name):
        """
        Sets the joint that drives the twist rotation.
        :param driver_name: str
        """

        self._twist_driver = driver_name

    @property
    def twist_joint(self):
        """
        Returns joint used as reference to create the twist joints (twist joints will be aligned in rotation to this
        joint during creation).
        If no twist joint is defined, driver joint rotation will be used. Useful in scenarios where the joint driver
        has multiple axis and it is not possible to properly retrieve the twist axis (for example, when setting up
        forearm twist setups
        :return: str
        """

        return self._twist_joint

    @property
    def reverse_orient(self):
        """
        Returns whether or not twist is applied from driven to driven or not
        :return: bool
        """

        return self._reverse_orient

    @property
    def twist_joints(self):
        """
        Returns a list of twist joints created by this rig ordered from driver to driven joints
        :return: list(str)
        """

        return self._twist_joints

    # =================================================================================================================
    # OVERRIDES
    # =================================================================================================================

    def create(self):
        super(OrientTwistJoint, self).create()

        joints = self.joints
        if not self._twist_driver:
            if joints:
                self._twist_driver = joints[0]
        if not self._twist_driver:
            self.log.warning(
                'Impossible to create rig: \n\tname: {}\n\tside: {}\n\twarning: No driver joint defined'.format(
                    self.name, self.side))
            return False

        # If not driven joint is given, the first children of the root twist joint hierarchy will be considered the last
        # joint of the twist hierarchy
        if not self._twist_driven:
            children = dcc.list_relatives(self._twist_driver, children_type='joint')
            if not children:
                self.log.warning(
                    'Impossible to create rig: \n\tname: {}\n\tside: {}\n\twarning: No twist driven defined'.format(
                        self.name, self.side))
                return False
            self._twist_driven = children[0]

        self._create_twist_joints()
        self._connect_twist_joints()
#
        self.delete_setup()

        return True

    # =================================================================================================================
    # INTERNAL
    # =================================================================================================================

    def _get_twist_axis(self, as_letter=False):
        if self._twist_joint:
            twist_joint = self._twist_joint
        else:
            twist_joint = self._twist_driver
            driver_children = dcc.list_children(twist_joint)
            if not driver_children:
                twist_joint = self._twist_driven

        if as_letter:
            return xform_utils.get_axis_letter_aimed_at_child(twist_joint)
        else:
            return xform_utils.get_axis_aimed_at_child(twist_joint)

    def _create_twist_joints(self):
        """
        Internal function that creates twist joints
        """

        distance = dcc.distance_between_nodes(self._twist_driver, self._twist_driven)
        distance_ratio = distance / (self._twist_joints_count - 1)
        twist_axis = self._get_twist_axis()

        root_node = dcc.node_parent(self._twist_driver, full_path=False)
        if root_node == dcc.node_short_name(self._twist_driven):
            twist_axis = (mathlib.Vector(*twist_axis) * -1.0).list()

        for i in range(self._twist_joints_count):
            dcc.clear_selection()
            twist_joint = dcc.create_joint(self._get_name('roll', id=i, node_type='joint'), size=self._scale)
            dcc.match_rotation(self._twist_joint or self._twist_driver, twist_joint)
            dcc.match_translation(self._twist_driver, twist_joint)
            joint_utils.OrientJointAttributes.zero_orient_joint(twist_joint)
            if self._reverse_orient:
                twist_joint = dcc.set_parent(twist_joint, self._twist_driven)
            else:
                twist_joint = dcc.set_parent(twist_joint, self._twist_driver)

            new_distance = mathlib.Vector(*twist_axis) * (distance_ratio * i)
            dcc.translate_node_in_object_space(twist_joint, new_distance.list(), relative=True)
            self._twist_joints.append(twist_joint)

    def _connect_twist_joints(self):
        """
        Internal function that connects twist setup
        """

        # orient locator will be used to retrieve a "clean" orientation value in the twist axis no matter how we
        # rotate the end joint of the twist chain.
        self._orient_locator = dcc.create_locator(name=self._get_name('orient', node_type='locator'))
        self._fixed_locator = dcc.create_locator(name=self._get_name('fixed', node_type='locator'))
        dcc.match_translation_rotation(self._twist_driver, self._orient_locator)
        dcc.match_translation_rotation(self._twist_driver, self._fixed_locator)
        self._fixed_locator = dcc.set_parent(self._fixed_locator, dcc.node_parent(self._twist_driver))
        self._orient_locator = dcc.set_parent(self._orient_locator, self._fixed_locator)

        for axis in 'XYZ':
            dcc.set_attribute_value(self._orient_locator, 'localScale{}'.format(axis), self._scale)
            dcc.set_attribute_value(self._fixed_locator, 'localScale{}'.format(axis), self._scale)

        # as the orient constraint is parented to the local constraint and both locators have the same transforms
        # the orient locator channels are completely clean. We use orient locator to retrieve a clean rotation of
        # the twist driver joint
        orient_constraint = dcc.create_orient_constraint(self._orient_locator, self._twist_driver)

        # we set the constraint interpolation type to average to avoid joint flipping
        dcc.set_attribute_value(orient_constraint, 'interpType', 1)

        axis_letter = self._get_twist_axis(as_letter=True)
        if len(axis_letter) > 1:
            axis_letter = axis_letter[-1]

        twist_value = -1
        loop_joints = self.twist_joints
        if self._reverse_orient:
            loop_joints = list(reversed(loop_joints))
        for i, twist_joint in enumerate(loop_joints):
            multiply_divide_twist = dcc.create_node(
                'multiplyDivide', node_name=self._get_name('twistJoint', id=i, node_type='multiplyDivide'))
            for axis in 'XYZ':
                input_attr = 'input2{}'.format(axis)
                if axis == axis_letter.upper():
                    if self._reverse_orient:
                        dcc.set_attribute_value(multiply_divide_twist, input_attr, 1.0 / len(self.twist_joints) * i)
                    else:
                        dcc.set_attribute_value(multiply_divide_twist, input_attr, twist_value)
                else:
                    dcc.set_attribute_value(multiply_divide_twist, input_attr, 0.0)
            dcc.connect_attribute(
                self._orient_locator, 'rotate', multiply_divide_twist, 'input1')
            dcc.connect_attribute(multiply_divide_twist, 'output', twist_joint, 'rotate')
            twist_value += 1.0 / (self._twist_joints_count - 1)

        # if axis_letter.lower() == 'y':
        #     dcc.set_attribute_value(self._twist_driven, 'rotateOrder', 4)     # yxz

        # twist_axis = self._get_twist_axis()
        # if len(twist_axis) > 1:
        #     twist_axis = twist_axis[-1]
        # axises = ['x', 'y', 'z']
        # axises.pop(axises.index(twist_axis.lower()))
        # orient_constraint = maya.cmds.orientConstraint(
        #     self._twist_driven, self._local_locator, self._orient_locator, skip=axises, mo=True)[0]

#         # orient_constraint = maya.cmds.orientConstraint(
#         #     self._twist_driver, self._orient_locator, w=100.0, skip=axises)[0]
#         #
#         # # # we set the constraint interpolation type to average to avoid joint flipping
#         # # dcc.set_attribute_value(orient_constraint, 'interpType', 1)
#         # #
#         # # twist_value = -1
#         # # rotate_attr = 'rotate{}'.format(twist_axis.upper())
#         # # for i, twist_joint in enumerate(self.twist_joints):
#         # #     multiply_divide_twist = dcc.create_node(
#         # #         'multiplyDivide', node_name=self._get_name('twistJoint', id=i, node_type='multiplyDivide'))
#         # #     # we need to multiply by 2 because the constraint makes the rotation to be divided by the half.
#         We counter
#         # #     # that by multiplying the twist value by 2
#         # #     dcc.set_attribute_value(multiply_divide_twist, 'input1X', twist_value * 2)
#         # #     dcc.connect_attribute(
#         # #         self._orient_locator, rotate_attr, multiply_divide_twist, 'input1X')
#         # #     dcc.connect_attribute(multiply_divide_twist, 'outputX', twist_joint, rotate_attr)
#         # #     twist_value += 1.0 / self._twist_joints_count
#         #
#         #
#         # input_value = -1
#         # for i in range(self._twist_joints_count):
#         #     multiply_divide_twist = dcc.create_node(
#         #         'multiplyDivide', node_name=self._get_name('twistJoint', id=i, node_type='multiplyDivide'))
#         #     dcc.set_attribute_value(multiply_divide_twist, 'input2X', input_value)
#         #     dcc.connect_attribute(self._orient_locator, 'rotate', multiply_divide_twist, 'input1')
#         #     dcc.connect_attribute(multiply_divide_twist, 'output', self.twist_joints[i], 'rotate')
#         #     input_value += 1.0 / self._twist_joints_count
# orient_joint = self._twist_driver
#
# # orient locator will be used to retrieve a "clean" orientation value in the twist axis no matter how we
# # rotate the end joint of the twist chain.
# self._orient_locator = dcc.create_locator(name=self._get_name('orientLocator', node_type='locator'))
# self._orient_buffer = dcc.create_buffer_group(self._orient_locator)
# self._local_locator = dcc.create_locator(name=self._get_name('localLocator', node_type='locator'))
# self._local_buffer = dcc.create_buffer_group(self._local_locator)
# dcc.match_translation_rotation(self._twist_driver, self._orient_buffer)
# dcc.match_translation_rotation(self._twist_driver, self._local_buffer)
# self._local_buffer = dcc.set_parent(self._local_buffer, dcc.node_parent(orient_joint))
# self._orient_buffer = dcc.set_parent(self._orient_buffer, self._local_buffer)
#
# for axis in 'XYZ':
#     dcc.set_attribute_value(self._orient_locator, 'localScale{}'.format(axis), self._scale)
#     dcc.set_attribute_value(self._local_locator, 'localScale{}'.format(axis), self._scale)
#
# twist_axis = xform_utils.get_axis_letter_aimed_at_child(self._twist_driver)
# if len(twist_axis) > 1:
#     twist_axis = twist_axis[-1]
# axises = ['x', 'y', 'z']
# axises.pop(axises.index(twist_axis.lower()))
# # orient_constraint = maya.cmds.orientConstraint(
# #     self._twist_driven, self._local_locator, self._orient_locator, skip=axises, mo=True)[0]
#
# orient_constraint = maya.cmds.orientConstraint(
#     self._twist_driver, self._orient_locator, w=100.0, skip=axises)[0]


class IkTwistJoint(rig.Rig):
    def __init__(self, *args, **kwargs):
        super(IkTwistJoint, self).__init__(*args, **kwargs)

        self._twist_joints_count = kwargs.pop('twist_joints_count', 5)
        self._twist_driver = kwargs.pop('twist_driver', None)
        self._twist_driven = kwargs.pop('twist_driven', None)
        self._twist_joint = kwargs.pop('twist_joint', None)
        self._reverse_orient = kwargs.pop('reverse_orient', False)

        self._twist_joints = list()
        self._ik_handle = None

        self._local_locator = None
        self._orient_locator = None
        self._local_buffer = None
        self._orient_buffer = None

    # =================================================================================================================
    # PROPERTIES
    # =================================================================================================================

    @property
    def twist_driver(self):
        """
        Returns the joint that drives the twist rotation. The rotation near this will be maximum and will decrease
        while it arrives into the driven joint
        :return: str
        """

        return self._twist_driver

    @twist_driver.setter
    def twist_driver(self, driver_name):
        """
        Sets the joint that drives the twist rotation.
        :param driver_name: str
        """

        self._twist_driver = driver_name

    @property
    def twist_joint(self):
        """
        Returns joint used as reference to create the twist joints (twist joints will be aligned in rotation to this
        joint during creation).
        If no twist joint is defined, driver joint rotation will be used. Useful in scenarios where the joint driver
        has multiple axis and it is not possible to properly retrieve the twist axis (for example, when setting up
        forearm twist setups
        :return: str
        """

        return self._twist_joint

    @property
    def reverse_orient(self):
        """
        Returns whether or not twist is applied from driven to driven or not
        :return: bool
        """

        return self._reverse_orient

    @property
    def twist_joints(self):
        """
        Returns a list of twist joints created by this rig ordered from driver to driven joints
        :return: list(str)
        """

        return self._twist_joints

    # =================================================================================================================
    # OVERRIDES
    # =================================================================================================================

    def create(self):
        super(IkTwistJoint, self).create()

        joints = self.joints
        if not self._twist_driver:
            if joints:
                self._twist_driver = joints[0]
        if not self._twist_driver:
            self.log.warning(
                'Impossible to create rig: \n\tname: {}\n\tside: {}\n\twarning: No driver joint defined'.format(
                    self.name, self.side))
            return False

        # If not driven joint is given, the first children of the root twist joint hierarchy will be considered the last
        # joint of the twist hierarchy
        if not self._twist_driven:
            children = dcc.list_relatives(self._twist_driver, children_type='joint')
            if not children:
                self.log.warning(
                    'Impossible to create rig: \n\tname: {}\n\tside: {}\n\twarning: No twist driven defined'.format(
                        self.name, self.side))
                return False
            self._twist_driven = children[0]

        self._create_twist_joints()
        self._create_ik_handle()
        self._connect_twist_joints()

        self.delete_setup()

        return True

    # =================================================================================================================
    # INTERNAL
    # =================================================================================================================

    def _get_twist_axis(self):
        if self._twist_joint:
            twist_joint = self._twist_joint
        else:
            twist_joint = self._twist_driver
            driver_children = dcc.list_children(twist_joint)
            if not driver_children:
                twist_joint = self._twist_driven

        return xform_utils.get_axis_aimed_at_child(twist_joint)

    def _create_twist_joints(self):
        """
        Internal function that creates twist joints
        """

        distance = dcc.distance_between_nodes(self._twist_driver, self._twist_driven)
        distance_ratio = distance / (self._twist_joints_count - 1)
        twist_axis = self._get_twist_axis()

        root_node = dcc.node_parent(self._twist_driver, full_path=False)
        if root_node == self._twist_driven:
            root_node = self._twist_driver
            twist_axis = (mathlib.Vector(*twist_axis) * -1.0).list()

        for i in range(self._twist_joints_count):
            dcc.clear_selection()
            twist_joint = dcc.create_joint(self._get_name('roll', id=i, node_type='joint'), size=self._scale)
            dcc.match_rotation(self._twist_joint or self._twist_driver, twist_joint)
            dcc.match_translation(self._twist_driver, twist_joint)
            joint_utils.OrientJointAttributes.zero_orient_joint(twist_joint)
            if i > 0:
                twist_joint = dcc.set_parent(twist_joint, self._twist_joints[0])
            else:
                if root_node:
                    twist_joint = dcc.set_parent(twist_joint, root_node)

            new_distance = mathlib.Vector(*twist_axis) * (distance_ratio * i)
            dcc.translate_node_in_object_space(twist_joint, new_distance.list(), relative=True)
            self._twist_joints.append(twist_joint)

    def _create_ik_handle(self):
        root_node = dcc.node_parent(self._twist_driver, full_path=False)
        if root_node == dcc.node_short_name(self._twist_driven):
            root_node = self._twist_driver

        ik_handle = ik_utils.IkHandle(self._get_name('roll', node_type='ikHandle'))
        ik_handle.set_solver(ik_handle.SOLVER_SC)
        ik_handle.set_start_joint(self._twist_joints[0])
        ik_handle.set_end_joint(self._twist_joints[-1])
        ik_handle = ik_handle.create()

        if root_node:
            ik_handle = dcc.set_parent(ik_handle, root_node)

        # we make sure that twist joint follows the driven joint
        dcc.create_point_constraint(ik_handle, self._twist_driven)

        self._ik_handle = ik_handle

    def _connect_twist_joints(self):
        """
        Internal function that connects twist setup
        """

        # We make sure that last twist joint has the full rotation from the driver joint
        if self._reverse_orient:
            dcc.create_orient_constraint(self._twist_joints[-1], self._twist_driven, maintain_offset=False)
        else:
            dcc.create_orient_constraint(self._twist_joints[-1], self._twist_driver, maintain_offset=False)

        mid_joint = int((len(self._twist_joints) / 2) - 1)
        distance_ratio = 1.0 / (len(self._twist_joints) - 1)

        loop_joints = self._twist_joints[1:-1]
        if self._reverse_orient:
            loop_joints = list(reversed(loop_joints))

        for i, twist_joint in enumerate(loop_joints):
            point_cns = maya.cmds.pointConstraint(
                self._twist_joints[0], self._twist_joints[-1], twist_joint, mo=False)[0]
            ori_cns = maya.cmds.orientConstraint(
                self._twist_joints[0], self._twist_joints[-1], twist_joint, mo=False)[0]
            weight_names = constraint.Constraint().get_weight_names(point_cns)

            if len(self._twist_joints) % 2 != 0 and i == mid_joint:
                start_weight = 0.5
                end_weight = 0.5
            else:
                if self._reverse_orient:
                    end_weight = 1.0 - ((i + 1) * distance_ratio)
                    start_weight = 1.0 - end_weight
                else:
                    start_weight = 1.0 - ((i + 1) * distance_ratio)
                    end_weight = 1.0 - start_weight

            for cns in [point_cns, ori_cns]:
                dcc.set_attribute_value(cns, weight_names[0], start_weight)
                dcc.set_attribute_value(cns, weight_names[1], end_weight)
