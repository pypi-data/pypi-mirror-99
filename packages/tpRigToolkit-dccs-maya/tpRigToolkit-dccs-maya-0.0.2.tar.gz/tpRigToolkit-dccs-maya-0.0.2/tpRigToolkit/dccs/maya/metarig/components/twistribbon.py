#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""
Module that contains twist ribbon rig component implementation
Ribbon with rivets attached to it
"""

from __future__ import print_function, division, absolute_import

import logging

import maya.cmds

from tpDcc import dcc
from tpDcc.dccs.maya.meta import metanode
from tpDcc.dccs.maya.core import geometry as geo_utils, rivet as rivet_utils, shape as shape_utils, skin as skin_utils
from tpDcc.dccs.maya.core import ik as ik_utils

from tpRigToolkit.dccs.maya.metarig.core import component, mixin

logger = logging.getLogger('tpRigToolkit-dccs-maya')


class TwistRibbon(component.RigComponent, mixin.JointMixin):
    def __init__(self, *args, **kwargs):
        super(TwistRibbon, self).__init__(*args, **kwargs)

        if self.cached:
            return

        mixin.JointMixin.__init__(self)
        self.set_name('twistRibbon')
        self.set_joint(None)
        self.set_end_transform(None)
        self.set_joint_count(5)
        self.set_offset_axis('Y')
        self.set_ribbon_offset(1)
        self.set_dual_quaternion(False)
        self.set_attach_directly(False)
        self.set_top_parent(None)
        self.set_bottom_parent(None)
        self.set_top_twist_fix(False)
        self.set_bottom_twist_fix(False)
        self.set_top_constraint(None)
        self.set_bottom_constraint(None)

    # =================================================================================================================
    # OVERRIDES
    # =================================================================================================================

    def create(self):
        super(TwistRibbon, self).create()

        if not self.joint:
            logger.warning('Impossible to create TwistRibbon rig setup because no joint is defined!')
            return False

        # create top and bottom twist locators
        top_locator = dcc.create_locator(name=self._get_name('topTwistLocator', node_type='locator'))
        top_locator = metanode.validate_obj_arg(top_locator, 'MetaObject', update_class=True)
        bottom_locator = dcc.create_locator(name=self._get_name('bottomTwistLocator', node_type='locator'))
        bottom_locator = metanode.validate_obj_arg(bottom_locator, 'MetaObject', update_class=True)
        self.add_attribute(attr='top_locator', value=top_locator, attr_type='messageSimple')
        self.add_attribute(attr='bottom_locator', value=bottom_locator, attr_type='messageSimple')

        # If not end transform is given, the first children of the root twist joint hierarchy will be considered the
        # last joint of the twist hierarchy
        if not self.end_transform:
            children = dcc.list_children(self.joint.meta_node, children_type='joint')
            if not children:
                logger.warning('No child found for "{}". Was not possible to create TwistRibbon rig setup.'.format(
                    self.joint))
                return False
            temp_group = metanode.validate_obj_arg(children[0], 'MetaObject', update_class=True)
        else:
            temp_group = self.end_transform

        # create groups where we will store ribbon setup nodes and rivet nodes
        ribbon_group = dcc.create_empty_group(name=self._get_name('twistRibbon', node_type='group'))
        ribbon_group = metanode.validate_obj_arg(ribbon_group, 'MetaObject', update_class=True)
        self.add_attribute(attr='ribbon_group', value=ribbon_group, attr_type='messageSimple')
        rivets_group = dcc.create_empty_group(name=self._get_name('twistRibbonRivets', node_type='group'))
        rivets_group = metanode.validate_obj_arg(rivets_group, 'MetaObject', update_class=True)
        self.add_attribute(attr='rivets_group', value=rivets_group, attr_type='messageSimple')
        rivets_group.set_parent(ribbon_group)

        # create ribbon surface
        self._create_surface(joints=[self.joint.meta_node, temp_group.meta_node])

        # if no joints are defined we created them from the surface
        joints = self.get_joints()
        if not joints:
            joints = geo_utils.nurbs_surface_v_to_transforms(
                self.surface.meta_node, 'ribbonJoint', count=self.joint_count)
            maya.cmds.parent(joints, self.ribbon_group.meta_node)
            joints = [metanode.validate_obj_arg(joint, 'MetaObject', update_class=True) for joint in joints]
            self.add_joints(joints)

        rivets = list()
        for joint in joints:
            # make sure joints are oriented properly and has clean channels
            dcc.delete_node(maya.cmds.orientConstraint(self.joint.meta_node, joint.meta_node))
            maya.cmds.makeIdentity(joint.meta_node, apply=True, r=True)

            # create rivet nodes attached to the ribbon surface
            control_transforms = list()
            rivet = rivet_utils.attach_to_surface(
                joint.meta_node, self.surface.meta_node, constraint=self.attach_directly)
            relatives = dcc.list_relatives(rivet, relative_type='transform')
            if relatives:
                control_transforms.append(relatives[1])
            shapes = shape_utils.get_shapes(rivet)
            dcc.hide_node(shapes)
            rivet = metanode.validate_obj_arg(rivet, 'MetaObject', update_class=True)
            rivet.set_parent(self.rivets_group)
            rivets.append(rivet)
        self.message_list_connect('rivets', rivets)

        # Skin surface to closest joints
        skin_surface = skin_utils.SkinJointSurface(self.surface.meta_node, self.name)
        skin_surface.set_joint_u(True)
        skin_surface.create()
        skin = skin_surface.get_skin()
        joints = skin_surface.get_joints_list()
        if self.dual_quaternion:
            dcc.delete_node(joints[1:-1])
            joints = [joints[0], joints[-1]]
        else:
            dcc.set_attribute_value(skin, 'skinningMethod', 0)

        top_joint = metanode.validate_obj_arg(joints[0], 'MetaObject', update_class=True)
        bottom_joint = metanode.validate_obj_arg(joints[1], 'MetaObject', update_class=True)
        self.add_attribute(attr='top_joint', value=top_joint, attr_type='messageSimple')
        self.add_attribute(attr='bottom_joint', value=bottom_joint, attr_type='messageSimple')

        dcc.match_translation_to_rotate_pivot(top_joint.meta_node, top_locator.meta_node)
        dcc.match_translation_to_rotate_pivot(bottom_joint.meta_node, bottom_locator.meta_node)
        top_joint.set_parent(top_locator)
        bottom_joint.set_parent(bottom_locator)

        maya.cmds.skinPercent(skin, self.surface.meta_node, normalize=True)
        dcc.hide_node(joints)

        if self.top_parent and dcc.node_exists(self.top_parent.meta_node):
            self.top_locator.set_parent(self.top_parent)
        if self.bottom_parent and dcc.node_exists(self.bottom_parent.meta_node):
            self.bottom_locator.set_parent(self.bottom_parent)

        if self.top_constraint and dcc.node_exists(self.top_constraint.meta_node):
            eval('cmds.{}({}, {}, mo=True)'.format(
                self.top_constraint_type, self.top_constraint.meta_node, top_locator.meta_node))
        if self.bottom_constraint and dcc.node_exists(self.bottom_constraint.meta_node):
            eval('cmds.{}({}, {}, mo=True)'.format(
                self.bottom_constraint_type, self.bottom_constraint.meta_node, bottom_locator.meta_node))

        if self.top_twist_fix:
            self._create_top_twister_joint()
        if self.bottom_twist_fix:
            self._create_bottom_twister_joint()

        return True

    # =================================================================================================================
    # BASE
    # =================================================================================================================

    def set_joint(self, joint):
        if not self.has_attr('joint'):
            self.add_attribute(attr='joint', value=joint, attr_type='messageSimple')
        else:
            self.joint = joint

    def set_end_transform(self, end_transform):
        if not self.has_attr('end_transform'):
            self.add_attribute(attr='end_transform', value=end_transform, attr_type='messageSimple')
        else:
            self.end_transform = end_transform

    def set_joint_count(self, joint_count):
        """
        Sets the number of twist joints that will be created
        :param joint_count: int
        """

        if not self.has_attr('joint_count'):
            self.add_attribute(attr='joint_count', value=joint_count, attr_type='int')
        else:
            self.joint_count = joint_count

    def set_offset_axis(self, offset_axis):
        if not self.has_attr('offset_axis'):
            self.add_attribute(attr='offset_axis', value=offset_axis)
        else:
            self.offset_axis = offset_axis

    def set_ribbon_offset(self, ribbon_offset):
        if not self.has_attr('ribbon_offset'):
            self.add_attribute(attr='ribbon_offset', value=ribbon_offset)
        else:
            self.ribbon_offset = ribbon_offset

    def set_dual_quaternion(self, flag):
        if not self.has_attr('dual_quaternion'):
            self.add_attribute(attr='dual_quaternion', value=flag)
        else:
            self.dual_quaternion = flag

        if flag:
            self.set_top_twist_fix(True)
            self.set_bottom_twist_fix(True)

    def set_attach_directly(self, flag):
        if not self.has_attr('attach_directly'):
            self.add_attribute(attr='attach_directly', value=flag)
        else:
            self.attach_directly = flag

    def set_surface(self, surface):
        """
        Set the NURBS surface that the controls should move and the joints should follow when using ribbon
        :param surface: str
        """

        if not self.has_attr('surface'):
            self.add_attribute(attr='surface', value=surface, attr_type='messageSimple')
        else:
            self.surface = surface

    def set_top_parent(self, top_parent):
        if not self.has_attr('top_parent'):
            self.add_attribute(attr='top_parent', value=top_parent, attr_type='messageSimple')
        else:
            self.top_parent = top_parent

    def set_bottom_parent(self, bottom_parent):
        if not self.has_attr('bottom_parent'):
            self.add_attribute(attr='bottom_parent', value=bottom_parent, attr_type='messageSimple')
        else:
            self.bottom_parent = bottom_parent

    def set_top_constraint(self, transform, constraint_type='parentConstraint'):
        if not self.has_attr('top_constraint'):
            self.add_attribute(attr='top_constraint', value=transform, attr_type='messageSimple')
        else:
            self.top_constraint = transform

        if not self.has_attr('top_constraint_type'):
            self.add_attribute(attr='top_constraint_type', value=constraint_type)
        else:
            self.top_constraint_type = constraint_type

    def set_bottom_constraint(self, transform, constraint_type='parentConstraint'):
        if not self.has_attr('bottom_constraint'):
            self.add_attribute(attr='bottom_constraint', value=transform, attr_type='messageSimple')
        else:
            self.bottom_constraint = transform

        if not self.has_attr('bottom_constraint_type'):
            self.add_attribute(attr='bottom_constraint_type', value=constraint_type)
        else:
            self.bottom_constraint_type = constraint_type

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

    # ==============================================================================================
    # INTERNAL
    # ==============================================================================================

    def _create_surface(self, joints):
        """
        Internal function that creates the ribbon surface
        """

        surface_name = self._get_name(self.name, 'twistRibbonSurface', node_type='geometry')
        ribbon_surface = geo_utils.transforms_to_nurbs_surface(
            joints, name=surface_name, offset_amount=self.ribbon_offset, offset_axis=self.offset_axis)

        if self.dual_quaternion:
            maya.cmds.rebuildSurface(
                ribbon_surface, constructionHistory=False, replaceOriginal=True, rebuildType=0, endKnots=1, keepRange=0,
                keepControlPoints=0, keepCorners=0, spansU=1, degreeU=1, spansV=2, degreeV=3, tolerance=0.01,
                fitRebuild=0, direction=2)

        dcc.set_attribute_value(ribbon_surface, 'inheritsTransform', False)
        surface = metanode.validate_obj_arg(ribbon_surface, 'MetaObject', update_class=True)
        self.set_surface(surface)
        self.surface.set_parent(self.ribbon_group)

    def _create_top_twister_joint(self):
        joint1, joint2, ik_handle = ik_utils.create_ik_chain(
            self.bottom_locator.meta_node, self.top_locator.meta_node, 'twistTopFix', ik_utils.IkHandle.SOLVER_RP)
        maya.cmds.hide(joint1, joint2)
        ik_handle = metanode.validate_obj_arg(ik_handle, 'MetaObject', update_class=True)
        self.add_attribute(attr='top_ik_handle', value=ik_handle, attr_type='messageSimple')

        xform = dcc.create_buffer_group(joint1)
        dcc.set_parent(xform, self.top_locator.meta_node)
        dcc.set_parent(ik_handle.meta_node, self.bottom_locator.meta_node)
        maya.cmds.hide(joint1, ik_handle.meta_node)

    def _create_bottom_twister_joint(self):
        ik_chain_name = self._get_name('twistBottomFix', node_type='ikHandle')
        joint1, joint2, ik_handle = ik_utils.create_ik_chain(
            self.bottom_locator.meta_node, self.top_locator.meta_node, ik_chain_name, ik_utils.IkHandle.SOLVER_RP)
        maya.cmds.hide(joint1, joint2)
        ik_handle = metanode.validate_obj_arg(ik_handle, 'MetaObject', update_class=True)
        self.add_attribute(attr='bottom_ik_handle', value=ik_handle, attr_type='messageSimple')
        xform = dcc.create_buffer_group(joint1)
        dcc.set_parent(xform, self.bottom_locator.meta_node)
        dcc.set_parent(ik_handle.meta_node, self.top_locator.meta_node)
        maya.cmds.hide(joint1, ik_handle.meta_node)
