#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""
Module that contains rig that allows to create buffer chains
"""

from __future__ import print_function, division, absolute_import

from tpDcc import dcc
from tpDcc.dccs.maya.core import transform, joint as joint_utils

from tpRigToolkit.dccs.maya.rigs import attach


class BufferRig(attach.AttachRig):
    def __init__(self, *args, **kwargs):
        super(BufferRig, self).__init__(*args, **kwargs)

        self._buffer_joints = self._joints
        self._create_buffer_joints = kwargs.pop('create_buffer_joints', False)
        self._build_hierarchy = kwargs.pop('build_hierarchy', False)
        self._buffer_replace = kwargs.pop('buffer_replace', ['jnt', 'buffer'])

    # =================================================================================================================
    # PROPERTIES
    # =================================================================================================================

    def create_buffer_joints(self):
        """
        Returns whether or not this joints are attached to a buffer chain
        :return: bool
        """

        return self._create_buffer_joints

    # =================================================================================================================
    # OVERRIDES
    # =================================================================================================================

    def create(self):
        super(BufferRig, self).create()

        self._duplicate_joints()
        self._create_before_attach_joints()

        if self._create_buffer_joints:
            self._attach_joints(self._buffer_joints, self.joints)

    def delete_setup(self):
        if self._create_buffer_joints:
            self.log.warning('Skipping setup group deletion because buffer creation is enabled!')
            return

        super(BufferRig, self).delete_setup()

    # =================================================================================================================
    # INTERNAL
    # =================================================================================================================

    def _create_before_attach_joints(self):
        """
        Internal function that is called before the attach joints process starts
        Override in custom rigs
        """

        pass

    def _duplicate_joints(self):
        """
        Internal function that duplicates current rig hierarchy of joints
        """

        if not self._create_buffer_joints:
            self._buffer_joints = self.joints
            return self._buffer_joints

        if self._build_hierarchy:
            build_hierarchy = joint_utils.BuildJointHierarchy()
            build_hierarchy.set_transforms(self.joints)
            build_hierarchy.set_replace(self._buffer_replace[0], self._buffer_replace[1])
            self._buffer_joints = build_hierarchy.create()
        else:
            duplicate_hierarhcy = transform.DuplicateHierarchy(self.joints[0])
            duplicate_hierarhcy.stop_at(self.joints[-1])
            duplicate_hierarhcy.only_these(self.joints)
            duplicate_hierarhcy.set_replace(self._buffer_replace[0], self._buffer_replace[1])
            self._buffer_joints = duplicate_hierarhcy.create()

        dcc.set_parent(self._buffer_joints[0], self._setup_group)

        return self._buffer_joints
