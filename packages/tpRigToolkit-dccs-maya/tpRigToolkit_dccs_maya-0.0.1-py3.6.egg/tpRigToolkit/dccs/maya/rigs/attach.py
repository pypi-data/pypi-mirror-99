#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""
Module that contains joint based rigs
"""

from __future__ import print_function, division, absolute_import

import maya.cmds

from tpDcc import dcc
from tpDcc.dccs.maya.core import joint as joint_utils, rig as rig_utils

from tpRigToolkit.dccs.maya.core import rig


class AttachRig(rig.Rig):

    ATTACH_CONSTRAINT = 0
    ATTACH_MATRIX = 1

    def __init__(self, *args, **kwargs):
        super(AttachRig, self).__init__(*args, **kwargs)

        self._enable_attach_joints = kwargs.pop('attach_joints', True)
        self._attach_type = kwargs.pop('attach_type', self.ATTACH_CONSTRAINT)
        self._auto_control_visibility = kwargs.pop('auto_control_visibility', True)
        self._create_switch = kwargs.pop('create_switch', True)
        self._switch_attribute_name = kwargs.pop('switch_attribute_name', 'switch')
        self._switch_node_name = kwargs.pop('switch_node_name', None)

    # =================================================================================================================
    # PROPERTIES
    # =================================================================================================================

    @property
    def attach_joints(self):
        """
        Returns whether or not joints attach functionality should be enabled
        :return: bool
        """

        return self._enable_attach_joints

    @attach_joints.setter
    def attach_joints(self, flag):
        """
        Sets whether or not joints attach functionality should be enabled
        :param flag: bool
        """

        self._enable_attach_joints = flag

    @property
    def switch_attribute_name(self):
        """
        Returns the name of the attribute that handles the switch functionality
        :return: str
        """

        return self._switch_attribute_name

    @switch_attribute_name.setter
    def switch_attribute_name(self, value):
        """
        Returns the name of the attribute that handles the switch functionality
        :return: str
        """

        self._switch_attribute_name = value

    @property
    def switch_node_name(self):
        """
        Returns the node that contains the attribute that manages the switch functionality
        :return: str
        """

        return self._switch_node_name

    @switch_node_name.setter
    def switch_node_name(self, value):
        """
        Returns the node that contains the attribute that manages the switch functionality
        :return: str
        """

        self._switch_node_name = value

    def _post_create(self):
        super(AttachRig, self)._post_create()

        # Create proxy attributes in all controls
        childs = dcc.list_relatives(self._controls_group, all_hierarchy=True, relative_type='transform')
        for child in childs:
            if not dcc.list_shapes(child):
                continue
            title = self._switch_attribute_name if \
                self._switch_attribute_name == 'switch' else '{} switch'.format(self._switch_attribute_name)
            dcc.add_title_attribute(child, title.upper())
            maya.cmds.addAttr(
                child, ln=self._switch_attribute_name,
                proxy='{}.{}'.format(self._switch_node_name, self._switch_attribute_name))

    # =================================================================================================================
    # BASE
    # =================================================================================================================

    def _attach_joints(self, source_chain, target_chain):
        """
        Internal function that attaches source joints chain to given target joints chain
        :param source_chain: list(str), hierarchy list of   joints chain to attach
        :param target_chain: list(str), hierarchy list sof joints chain to attach into
        """

        if not self._enable_attach_joints:
            return

        attach = joint_utils.AttachJoints(
            source_chain, target_chain, create_switch=self._create_switch,
            switch_attribute_name=self._switch_attribute_name)
        attach.set_attach_type(self._attach_type)
        attach.create()

        # TODO: If control name is given, we should add a switch attribute to that control and connect that
        # TODO: attribute to the Attach Joint switch attribute

        if not self._switch_node_name:
            self._switch_node_name = target_chain[0]

        if dcc.attribute_exists(self._switch_node_name, self._switch_attribute_name):
            switch = rig_utils.RigSwitch(target_chain[0])
            weight_count = switch.get_weight_count()
            if weight_count > 0:
                if self._auto_control_visibility:
                    switch.add_groups_to_index(weight_count - 1, self._controls_group)
                switch.create()
            self._switch_node = target_chain[0]
