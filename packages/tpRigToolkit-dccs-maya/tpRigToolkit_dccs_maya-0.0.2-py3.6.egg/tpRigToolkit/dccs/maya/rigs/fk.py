#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""
Module that contains Fk rig setup implementation
"""

from __future__ import print_function, division, absolute_import

import maya.cmds

from tpDcc import dcc
from tpRigToolkit.dccs.maya.rigs import buffer


class FkRig(buffer.BufferRig):
    def __init__(self, *args, **kwargs):

        kwargs['buffer_replace'] = kwargs.pop('buffer_replace', None) or ['jnt', 'fk']

        super(FkRig, self).__init__(*args, **kwargs)

        self._skip_controls = kwargs.pop('skip_controls', list())
        self._offset_rotation = kwargs.pop('offset_rotation', list())
        self._match_to_rotation = kwargs.pop('match_to_rotation', True)
        self._skip_match_to_rotation = kwargs.pop('skip_match_to_rotation', list())
        self._increment_offset_rotation = kwargs.pop('increment_offset_rotation', list())

        self._current_increment = 0         # temp index pointing to current Fk control being run in the loop
        self._transforms_list = list()      # temp list of transforms used during the Fk controls loop
        self._control = None
        self._last_control = None

    # =================================================================================================================
    # OVERRIDES
    # =================================================================================================================

    def create(self):
        super(FkRig, self).create()

        self._loop(self._buffer_joints)

    def _create_control(self, name=None, **kwargs):
        new_control = super(FkRig, self)._create_control(name=name or 'fk', **kwargs)

        self._last_control = self._control
        self._control = new_control

        new_control.create_root()
        new_control.create_auto()

        self._set_control_attributes(new_control)

        return new_control

    # =================================================================================================================
    # INTERNAL
    # =================================================================================================================

    def _attach(self, control, target_transform):
        """
        Internal function that constraints the transform (usually a joint) to the given Fk control transform
        :param control: str, name of the Fk control being processed
        :param target_transform: str, name of the transform (usually a joint) Fk control is going to constraint
        """

        if not self._attach_joints:
            return

        if control.has_root_buffer():
            if self._offset_rotation:
                dcc.rotate_node_in_object_space(control.get_top(), self._offset_rotation, relative=True)
            if self._current_increment in self._increment_offset_rotation:
                offset_rotation = self._increment_offset_rotation[self._current_increment]
                dcc.rotate_node_in_object_space(control.get_top(), offset_rotation, relative=True)

        dcc.create_parent_constraint(target_transform, control.get(), maintain_offset=True)

    def _set_control_attributes(self, control):
        """
        Internal function that updates the attributes of the Fk control after the control creation
        :param control: RigControl
        """

        control.hide_scale_attributes()

    def _loop(self, transforms):
        found_to_skip = list()

        if self._skip_controls:
            for increment in self._skip_controls:
                found_transform = None
                try:
                    found_transform = transforms[increment]
                except Exception:
                    pass
                if found_transform:
                    found_to_skip.append(found_transform)

        self._current_increment = 0

        for i in range(len(transforms)):
            if transforms[i] in found_to_skip:
                self._current_increment += 1
                continue
            self._current_increment = i
            new_control = self._create_control(name_data={'id': i})
            self._loop_at_increment(new_control, transforms)

    def _loop_at_increment(self, control, transforms):
        """
        Internal function that is called for each one of the Fk controls. Depending on the position in the Fk
        hierarchy we will handle the control in different ways
        :param control: str, name of the Fk control being processed
        :param transforms: list(str), list of transforms (usually joints) of the Fk hierarchy
        """

        self._transforms_list = transforms
        current_transform = transforms[self._current_increment]

        self._all_increments(control, current_transform)

        if self._current_increment == 0:
            self._first_increment(control, current_transform)
        if self._current_increment > 0:
            self._increment_greater_than_zero(control, current_transform)
        if self._current_increment < len(transforms):
            self._increment_less_than_last(control, current_transform)
        if len(transforms) > self._current_increment > 0:
            self._increment_after_start_before_end(control, current_transform)
        if self._current_increment == len(transforms) - 1 or self._current_increment == 0:
            self._increment_equal_to_start_end(control, current_transform)

    def _all_increments(self, control, transform):
        """
        Internal function that is called for all the Fk controls during the loop
        :param control: str, name of the Fk control being processed
        :param transform: str, name of the transform (usually a joint) Fk control is going to constraint
        """

        match_to_rotation = self._match_to_rotation
        if self._current_increment in self._skip_match_to_rotation:
            match_to_rotation = False

        if match_to_rotation:
            dcc.match_translation_rotation(transform, control.get_top())
        else:
            dcc.match_translation(transform, control.get_top())
        dcc.match_scale(transform, control.get_top())
        dcc.match_translation_to_rotate_pivot(transform, control.get_top())

    def _first_increment(self, control, transform):
        """
        Internal function that is called only for the root Fk control during the loop
        :param control: RigControl, name of the Fk control being processed
        :param transform: str, name of the transform (usually a joint) Fk control is going to constraint
        """

        self._attach(control, transform)

    def _increment_greater_than_zero(self, control, transform):
        """
        Internal function that is called only for Fk controls that are not the root one during the loop
        :param control: RigControl, name of the Fk control being processed
        :param transform: str, name of the transform (usually a joint) Fk control is going to constraint
        """

        self._attach(control, transform)

        if self._last_control:
            control.set_parent(self._last_control.get())
            maya.cmds.controller(control.get(), self._last_control.get(), p=True)

    def _increment_less_than_last(self, control, transform):
        """
        Internal function that is called only for Fk controls that are not the last one during the loop
        :param control: RigControl, name of the Fk control being processed
        :param transform: str, name of the transform (usually a joint) Fk control is going to constraint
        """

        pass

    def _increment_equal_to_start_end(self, control, transform):
        """
        Internal function that is called only for the first and last Fk controls of the hierarchy during the loop
        :param control: RigControl, name of the Fk control being processed
        :param transform: str, name of the transform (usually a joint) Fk control is going to constraint
        """

        pass

    def _increment_after_start_before_end(self, control, transform):
        """
        Internal function that is called only for all Fk controls except the first and last during the loop
        :param control: RigControl, name of the Fk control being processed
        :param transform: str, name of the transform (usually a joint) Fk control is going to constraint
        """

        pass

    def _last_increment(self, control, transform):
        """
        Internal function that is called only for the last Fk control in the hierarchy during the loop
        :param control: RigControl, name of the Fk control being processed
        :param transform: str, name of the transform (usually a joint) Fk control is going to constraint
        """

        pass
