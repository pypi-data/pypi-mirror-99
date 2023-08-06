#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""
Module that contains Ik rig setup implementation
Useful for creating ik setup for arms and legs
"""

from __future__ import print_function, division, absolute_import

from tpDcc import dcc
from tpDcc.dccs.maya.core import ik as ik_utils, rig as rig_utils, joint as joint_utils

from tpRigToolkit.dccs.maya.rigs import buffer


class IkRig(buffer.BufferRig):
    def __init__(self, *args, **kwargs):

        kwargs['buffer_replace'] = kwargs.pop('buffer_replace', None) or ['jnt', 'ik']

        super(IkRig, self).__init__(*args, **kwargs)

        self._ik_buffer_joint = kwargs.pop('ik_buffer_joint', True)
        self._build_pole_vector_control = kwargs.pop('_build_pole_vector_control', True)
        self._pole_vector_control_data = kwargs.pop('pole_vector_control_data', dict())
        self._bottom_control_data = kwargs.pop('bottom_control_data', dict())
        self._match_bottom_to_joint = kwargs.pop('match_bottom_control_to_joint', True)
        self._pole_angle_joints = kwargs.pop('pole_angle_joints', list())
        self._pole_vector_offset = kwargs.pop('pole_vector_offset', 1)
        self._orient_constraint = kwargs.pop('orient_constraint', True)
        self._start_joint = kwargs.pop('start_joint', None)
        self._end_joint = kwargs.pop('end_joint', None)

        self._ik_chain = None
        self._pole_vector_control = None
        self._pole_vector_constraint = None
        self._bottom_control = None
        self._ik_handle = None

    # =================================================================================================================
    # PROPERTIES
    # =================================================================================================================

    @property
    def ik_handle(self):
        """
        Returns Ik Handle
        :return: str
        """

        return self._ik_handle

    @property
    def ik_chain(self):
        """
        Returns Ik chain
        :return: list(str)
        """

        return self._ik_chain

    @property
    def start_ik_joint(self):
        """
        Returns start joint of the Ik handle
        :return: str
        """

        return self._ik_chain[self._start_index]

    @property
    def end_ik_joint(self):
        """
        Returns end joint of the Ik handle
        :return: str
        """

        return self._ik_chain[self._end_index]

    @property
    def bottom_control(self):
        """
        Returns Ik bottom control
        :return: RigControl
        """

        return self._bottom_control

    # =================================================================================================================
    # BASE
    # =================================================================================================================

    def get_pole_vector_control(self):
        """
        Returns Ik pole vector control
        :return: RigControl or None
        """

        return self._pole_vector_control

    # =================================================================================================================
    # OVERRIDES
    # =================================================================================================================

    def create(self):
        self._start_joint = dcc.node_short_name(self._start_joint or self.joints[0])
        self._end_joint = dcc.node_short_name(self._end_joint or self.joints[-1])
        self._start_index = self.joints.index(dcc.node_short_name(self._start_joint))
        self._end_index = self.joints.index(dcc.node_short_name(self._end_joint))

        super(IkRig, self).create()

        self._create_pole_vector_control()
        self._create_bottom_control()
        self._setup_bottom_control()

        if self._build_pole_vector_control:
            self._create_pole_vector()

    def _create_before_attach_joints(self):
        super(IkRig, self)._create_before_attach_joints()

        self._create_ik_handle()

    def _duplicate_joints(self):
        super(IkRig, self)._duplicate_joints()

        self._ik_chain = self._buffer_joints

        if not self._create_buffer_joints:
            return

        ik_group = self._create_group('ik')
        dcc.set_parent(self._ik_chain[0], ik_group)
        dcc.set_parent(ik_group, self._setup_group)

    # =================================================================================================================
    # INTERNAL
    # =================================================================================================================

    def _create_ik_handle(self):
        """
        Internal function that creates Ik handle
        """

        if self._ik_buffer_joint:
            buffer_joint = self._create_ik_buffer_joint()
        else:
            buffer_joint = self._ik_chain[self._end_index]

        ik_handle = ik_utils.IkHandle(self._get_name('ik', node_type='ikHandle'))
        ik_handle.set_start_joint(self._ik_chain[self._start_index])
        ik_handle.set_end_joint(buffer_joint)
        ik_handle.set_solver(ik_handle.SOLVER_RP)
        self._ik_handle = ik_handle.create()
        dcc.hide_node(self._ik_handle)

        ik_handle_buffer = dcc.create_buffer_group(self._ik_handle)
        dcc.set_parent(ik_handle_buffer, self._setup_group)

    def _create_ik_buffer_joint(self):
        """
        Internal function that creates Ik buffer joint
        This buffer is useful when multiple rigs are attached to the same target Ik handle joint to avoid transform
        cycles and also to have clean transforms channels in the target node which helps the Ik handle to behave in
        a more solid manner
        :return: str
        """

        end_joint = self._ik_chain[self._end_index]
        buffer_name = dcc.find_unique_name('{}_ikBuffer'.format(end_joint))
        buffer_joint = dcc.duplicate_node(end_joint, new_node_name=buffer_name, only_parent=True)
        end_joint = dcc.set_parent(end_joint, buffer_joint)
        if not dcc.is_attribute_connected_to_attribute(buffer_joint, 'scale', end_joint, 'inverseScale'):
            dcc.connect_attribute(buffer_joint, 'scale', end_joint, 'inverseScale')

        attributes = list()
        for axis in 'XYZ':
            for attr_name in ['rotate', 'jointOrient']:
                attributes.append('{}{}'.format(attr_name, axis))
        for attribute in attributes:
            dcc.set_attribute_value(end_joint, attribute, 0)

        return buffer_joint

    def _create_pole_vector_control(self):
        """
        Internal function that creates the control that manages the pole vector of the Ik
        """

        if not self._build_pole_vector_control:
            return

        pole_vector_data = self._pole_vector_control_data.copy()
        if 'control_type' not in pole_vector_data:
            pole_vector_data['control_type'] = 'cube'

        pole_vector_control = self._create_control('pole', **pole_vector_data)
        pole_vector_control.hide_scale_and_visibility_attributes()
        self._pole_vector_control = pole_vector_control

    def _create_bottom_control(self):
        """
        Internal function that creates bottom Ik control
        """

        bottom_control_data = self._bottom_control_data.copy()
        bottom_control = self._create_control('bottom', **bottom_control_data)
        bottom_control.hide_scale_and_visibility_attributes()
        bottom_control.create_root()
        bottom_control.create_auto()

        joints = self._ik_chain

        if self._match_bottom_to_joint:
            bottom_control.match_translation_rotation(joints[self._end_index])
        else:
            bottom_control.match_translation(joints[self._end_index])

        self._bottom_control = bottom_control

        return self._bottom_control

    def _setup_bottom_control(self):
        """
        Internal function that setup bottom control after its creation
        :return:
        """

        joints = self._ik_chain

        ik_handle_parent = dcc.node_parent(self._ik_handle)

        dcc.set_parent(ik_handle_parent, self._bottom_control.get())

        if self._orient_constraint:
            dcc.create_orient_constraint(joints[self._end_index], self._bottom_control.get(), maintain_offset=True)

    def _create_pole_vector(self):
        """
        Internal function that creates the Ik pole vector setup
        :return:
        """

        bottom_control = self._bottom_control.get()

        pole_vector_control = self._pole_vector_control
        pole_vector_control_buffer = pole_vector_control.create_root()

        dcc.add_title_attribute(bottom_control, 'POLE_VECTOR')
        dcc.add_bool_attribute(bottom_control, 'poleVisibility', default_value=True)
        dcc.add_float_attribute(bottom_control, 'twist')

        if self.side == self.mirror_side:
            dcc.connect_multiply(bottom_control, 'twist', self._ik_handle, 'twist', -1)
        else:
            dcc.connect_attribute(bottom_control, 'twist', self._ik_handle, 'twist')

        pole_joints = self._get_pole_joints()
        position = dcc.get_pole_vector_position(
            pole_joints[0], pole_joints[1], pole_joints[2], offset=self._pole_vector_offset * self.scale)
        dcc.move_node(pole_vector_control.get(), position[0], position[1], position[2])

        self._create_pole_vector_constraint(pole_vector_control.get(), self._ik_handle)

        rig_line_name = self._get_name('pvLine', node_type='rigLine')
        rig_line = rig_utils.RiggedLine(pole_joints[1], pole_vector_control.get(), rig_line_name).create()
        dcc.set_parent(rig_line, self._controls_group)

        dcc.connect_attribute(bottom_control, 'poleVisibility', pole_vector_control_buffer, 'visibility')
        dcc.connect_attribute(bottom_control, 'poleVisibility', rig_line, 'visibility')

        self._pole_vector_buffer = pole_vector_control_buffer

    def _create_pole_vector_constraint(self, pole_vector_control, ik_handle):
        """
        Internal function that creates the constraint used for pole vector
        :param pole_vector_control: str, name of the pole vector control
        :param ik_handle: str, name of the Ik handle, pole vector is applied into
        """

        self._pole_vector_constraint = dcc.create_pole_vector_constraint(pole_vector_control, ik_handle)

    def _get_pole_joints(self):
        """
        Internal function that returns joints that define the pole vector angle plane
        If not default pole angle joints are given, the first, mid and last Ik chain joints will be used to define
        the pole vector angle plane
        """

        if not self._pole_angle_joints:

            hierarchy = joint_utils.get_joint_list(self._ik_chain[self._start_index], self._ik_chain[self._end_index])
            mid_joint_index = int(len(hierarchy) / 2)
            if self._ik_buffer_joint:
                mid_joint = hierarchy[mid_joint_index - 1]
            else:
                mid_joint = hierarchy[mid_joint_index]
            joints = [self._ik_chain[self._start_index], mid_joint, self._ik_chain[self._end_index]]
            return joints

        return self._pole_angle_joints
