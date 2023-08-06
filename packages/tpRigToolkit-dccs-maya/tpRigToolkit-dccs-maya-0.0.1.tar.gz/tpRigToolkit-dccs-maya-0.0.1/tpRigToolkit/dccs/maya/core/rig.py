#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""
Module that contains base class for rigs
"""

from __future__ import print_function, division, absolute_import

import os
import logging

import maya.cmds

from tpDcc import dcc
from tpDcc.libs.python import python

from tpRigToolkit.core import control
from tpRigToolkit.managers import names

logger = logging.getLogger('tpRigToolkit-dccs-maya')


class RigNotReadyException(Exception):
    pass


class Rig(object):
    def __init__(self, name, **kwargs):
        super(Rig, self).__init__()

        self._name = name
        self._side = kwargs.pop('side', 'center')
        self._log = kwargs.pop('log', logger)
        self._mirror_side = kwargs.pop('mirror_side', 'right')
        self._naming_file = kwargs.pop('naming_file', '')
        self._naming_rule = kwargs.pop('name_rule', '')
        self._name_data = kwargs.pop('name_data', dict())
        self._scale = kwargs.pop('scale', 1.0)

        self._setup_group = None
        self._controls_group = None
        self._setup_group_parent = kwargs.pop('setup_group_parent', None)
        self._controls_group_parent = kwargs.pop('controls_group_parent', None)
        self._delete_setup_group = kwargs.pop('delete_setup_group', False)

        self._joints = self._check_joints(python.force_list(kwargs.pop('joints', list())))

        self._controls = list()
        self._controls_path = kwargs.pop('controls_path', None)
        self._controls_scale = kwargs.pop('controls_scale', 1.0)
        self._controls_data = kwargs.pop('controls_data', dict())
        self._use_control_side_colors = kwargs.pop('use_control_side_colors', True)
        self._side_colors = kwargs.pop('side_colors', dict())

        # default common tokens for rig names
        self._name_data.update(
            {'rig': self.name, 'side': self.side}
        )

        self._create_default_groups()

    def __getattribute__(self, item):
        """
        Override version __getattribute__ that allow us to call specific rig functionality after calling a specific
        rig function. By default, is used to call post_create function in all rig create function implementations
        """

        custom_functions = ['create']
        if item in custom_functions:
            result = object.__getattribute__(self, item)
            if item == 'create':
                ready = self._check()
                if not ready:
                    raise RigNotReadyException(
                        'Rig is not ready to build:\n\tclass: {}\n\tname: {}\n\tside: {}'.format(
                            self.__class__.__name__, self.name, self.side))
            result_values = result()

            def results():
                return result_values
            if item == 'create':
                self._post_create()
            return results
        else:
            return object.__getattribute__(self, item)

    # =================================================================================================================
    # PROPERTIES
    # =================================================================================================================

    @property
    def name(self):
        return self._name

    @property
    def side(self):
        return self._side

    @property
    def mirror_side(self):
        return self._mirror_side

    @property
    def log(self):
        return self._log

    @property
    def naming_file(self):
        return self._naming_file

    @property
    def naming_rule(self):
        return self._naming_rule

    @property
    def controls_path(self):
        return self._controls_path

    @property
    def scale(self):
        return self._scale

    @property
    def joints(self):
        return self._joints

    # =================================================================================================================
    # BASE
    # =================================================================================================================

    def create(self):
        """
        Creates the rig
        """

        self.log.info('Creating new rig:\n\tname: {}\n\tside: {}\n\tclass: {}'.format(
            self.name, self.side, self.__class__.__name__))
        self._parent_default_groups()
        if self._delete_setup_group:
            self.delete_setup()

    def get_controls(self):
        """
        Returns controls linked to this rig
        :return: list(RigControl)
        """

        return self._controls

    def delete_setup(self):
        if not dcc.node_exists(self._setup_group):
            self.log.warning('Impossible to delete setup for rig "{}". Setup group does not exist.'.format(self.name))
            return

        if dcc.node_is_empty(self._setup_group):
            parent = dcc.node_parent(self._setup_group)
            if parent:
                self.log.warning('Setup group for rig "{}" is parented. Skipping deletion.'.format(self.name))
            else:
                dcc.delete_node(self._setup_group)
                return
        if dcc.node_is_empty(self._setup_group) and self._delete_setup_group:
            self.log.warning('Setup group for rig "{}" is not empty. Skipping deletion.'.format(self.name))

        if self._delete_setup_group:
            self.log.warning('Could not delete setup group for rig:\n\tname: {}\n\tside: {}\n\tclass: {}'.format(
                self.name, self.side, self.__class__.__name__))
            return

    # =================================================================================================================
    # INTERNAL
    # =================================================================================================================

    def _check(self):
        """
        Internal function that checks whether or not rig is ready to be build
        :return: bool
        """

        return True

    def _get_name(self, name, *args, **kwargs):
        """
        Internal function that returns a proper name for elements of the rig module
        :param name: str
        :param node_type: str
        :return: str
        """

        return names.solve_name(
            self.name, name, side=self.side, naming_file=self.naming_file, rule_name=self.naming_rule, *args, **kwargs)

    def _create_group(self, name, *args, **kwargs):
        """
        Internal function that creates a new rig group
        :param name: str
        :return: str
        """

        kwargs['node_type'] = 'group'
        group_name = self._get_name(name, *args, **kwargs)
        new_group = dcc.create_empty_group(name=dcc.find_unique_name(group_name))

        return new_group

    def _create_default_groups(self):
        """
        Internal function that creates default rig groups
        """

        self._controls_group = self._create_controls_group()
        self._setup_group = self._create_setup_group()
        # dcc.hide_node(self._setup_group)
        self._parent_default_groups()

    def _parent_default_groups(self):
        """
        Internal function that parents the default groups
        """

        self._parent_group(self._controls_group, self._controls_group_parent)
        self._parent_group(self._setup_group, self._setup_group_parent)

    def _parent_group(self, group, parent_group):
        """
        Internal function that is used to parent groups in  a rig
        :param group: str
        :param parent_group: str
        """

        if not group or not parent_group or not dcc.node_exists(group):
            return
        if not dcc.node_exists(parent_group):
            self.log.warning(
                'Node "{}" cannot be a group parent because it does not exists in current scene!'.format(parent_group))
            return

        group_parent = dcc.node_parent(group)
        if group_parent and group_parent == group_parent:
            return

        try:
            dcc.set_parent(group, parent_group)
        except Exception:
            pass

    def _create_setup_group(self):
        """
        Internal function that creates rig setup group
        :return: str
        """

        setup_group = self._create_group('setup')
        if self._setup_group:
            dcc.set_parent(setup_group, self._setup_group)

        return setup_group

    def _create_controls_group(self):
        """
        Internal function that creates rig controls group
        :return: str
        """

        controls_group = self._create_group('controls')
        if self._controls_group:
            dcc.set_parent(controls_group, self._controls_group)

        return controls_group

    def _check_joints(self, joints):
        """
        Internal function that that returns only valid joints from the list of given nodes
        :param joints: list(str)
        :return: bool
        """

        valid_joints = list()

        for joint in joints:
            if not dcc.node_type(joint) in ('joint', 'transform'):
                self.log.warning('Node "{}" is not a joint or transform. Rig "{}" may not be build correctly!'.format(
                    joint, self.name))
                continue
            joint = dcc.node_short_name(joint)
            valid_joints.append(joint)

        return valid_joints

    def _create_control(self, name=None, **kwargs):
        name = name or 'new'

        # this dict stores all the information needed to solve the control name
        name_data = dict()
        name_data.update(**kwargs.pop('name_data', dict()))     # update name data with custom data from function
        name_data.update(**self._name_data)                     # update name data with specific rig name data
        control_data = {
            'name_data': name_data,
            'controls_path': self._controls_path if self._controls_path and os.path.isdir(self._controls_path) else '',
            'naming_file': self._naming_file,
            'rule_name': self._naming_rule
        }
        control_data.update(self._controls_data)
        control_data.update(**kwargs)

        control_data['control_size'] = control_data.get('control_size', 1.0) * self._controls_scale * self._scale
        control_color = control_data.get('color', None)
        side_color = self._side_colors.get(self._side or '', None) or dcc.get_color_of_side(side=self._side or '')
        if side_color and self._use_control_side_colors or side_color and not control_color:
            control_data['color'] = side_color

        new_control = control.RigControl(name, side=self.side, **control_data)
        new_control.hide_visibility_attribute()
        new_control.set_parent(self._controls_group)

        self._controls.append(new_control)

        return new_control

    def _post_create(self):
        """
        Internal function that is called when a rig creation process is completed
        """

        class_name = str(self.__class__.__name__)

        dcc.add_string_attribute(self._controls_group, 'className', default_value=class_name)
        if dcc.node_exists(self._setup_group):
            if dcc.node_is_empty(self._setup_group):
                parent = dcc.node_parent(self._setup_group)
                if not parent:
                    self.log.warning('Empty setup group found:\n\tclass: "{}"\n\tname: {}\n\tside: {}'.format(
                        class_name, self.name, self.side))

        try:
            self._post_create_rotate_order()
        except Exception:
            self.log.warning(
                'Impossible to add rotate order to channel box:\n\tclass: "{}"\n\tname: {}\n\tside: {}'.format(
                    class_name, self.name, self.side))

    def _post_create_rotate_order(self):
        """
        Internal function that is called during rig post create step.
        Updates all controls of a rig to make sure that their rotate order attributes are visible in the channel box
        """

        for control in self.get_controls():
            count = 0
            for axis in 'XYZ':
                if not dcc.is_attribute_locked(control.get(), 'rotate{}'.format(axis)):
                    count += 1
            if count == 3:
                maya.cmds.setAttr('{}.rotateOrder'.format(control.get()), cb=True)
                maya.cmds.setAttr('{}.rotateOrder'.format(control.get()), k=True)
