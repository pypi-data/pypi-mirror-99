#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""
Module that contains rig control implementation for Maya
"""

import logging

import maya.cmds

from tpDcc import dcc
from tpDcc.libs.python import python
from tpDcc.dccs.maya.core import decorators, attribute, shape as shape_utils, node as node_utils
from tpDcc.dccs.maya.core import curve as curve_utils, name as name_utils, transform as transform_utils
from tpDcc.dccs.maya.core import attribute as attr_utils, color as color_utils

from tpRigToolkit.core import control
from tpRigToolkit.libs.controlrig.core import controllib

LOGGER = logging.getLogger('tpRigToolkit-dccs-maya')


class MayaRigControl(control.BaseRigControl):
    """
    Creates a curve based control
    """

    def __init__(self, name, **kwargs):

        self._uuid = None
        self._shapes = list()

        super(MayaRigControl, self).__init__(name=name, **kwargs)

    # =================================================================================================================
    # OVERRIDES
    # =================================================================================================================

    @decorators.undo_chunk
    def set_curve_type(self, type_name=None, keep_color=True, **kwargs):
        """
        Updates the curves of the control with the given control type
        :param type_name: str
        :param keep_color: bool
        """

        if not type_name:
            if dcc.attribute_exists(self.get(), 'curveType'):
                type_name = dcc.get_attribute_value(self.get(), 'curveType')

        shapes = shape_utils.get_shapes(self.get())
        color = kwargs.pop('color', None)
        kwargs['color'] = color or (node_utils.get_rgb_color(shapes[0]) if shapes else 0)

        super(MayaRigControl, self).set_curve_type(type_name=type_name, keep_color=keep_color, **kwargs)

        self.update_shapes()
        string_attr = attr_utils.StringAttribute('curveType')
        string_attr.create(self._name)
        string_attr.set_value(type_name)

        return True

    def _create(self, **kwargs):
        """
        Internal function that forces the creation of the control curve
        """

        # whether or not to tag the new control curve
        tag = kwargs.get('tag', None)

        self._name = dcc.create_empty_group(name=self._name)
        self._uuid = dcc.node_handle(self._name)
        super(MayaRigControl, self)._create(**kwargs)
        if tag:
            try:
                maya.cmds.controller(self._name)
            except Exception:
                pass

    # =================================================================================================================
    # OVERRIDES
    # =================================================================================================================

    def update_shapes(self):
        """
        Force the update of the internal control shapes cache
        """

        self._shapes = shape_utils.get_shapes(self._name)

    def get_root(self, suffix=None):
        """
        Returns transform group located above the control
        :return: str
        """

        return transform_utils.get_buffer_group(self.get(), suffix or 'root')

    def get_auto(self, suffix=None):
        """
        Returns transform group located above the control
        :return: str
        """

        return transform_utils.get_buffer_group(self.get(), suffix or 'auto')

    def get_mirror(self, suffix=None):

        return transform_utils.get_buffer_group(self.get(), suffix or 'mirror')

    def get_top(self):
        """
        Returns top control (taking into account root and auto buffer groups)
        :return: str
        """

        mirror_group = self.get_mirror()
        if mirror_group:
            return mirror_group
        root_group = self.get_root()
        if root_group:
            return root_group
        auto_group = self.get_auto()
        if auto_group:
            return auto_group

        return self.get()

    def set_parent(self, parent, **kwargs):
        """
        Overrides set parent to parent proper root/auto nodes if necessary
        :param parent: str, parent transform node name
        :return:
        """

        # Whether to parent ctrl transform or take into account also root/auto groups
        parent_top = kwargs.pop('parent_top', True)
        node_to_parent = self.get()

        root_group = self.get_root()
        auto_group = self.get_auto()

        if parent_top:
            mirror_group = self.get_mirror(suffix=kwargs.pop('mirror_suffix', None))
            if mirror_group:
                node_to_parent = mirror_group
            elif root_group and dcc.node_exists(root_group):
                node_to_parent = root_group
            else:
                if auto_group and dcc.node_exists(auto_group):
                    node_to_parent = auto_group

        dcc.set_parent(node_to_parent, parent)

    def get_rgb_color(self, linear=True):
        """
        Returns the RGB color of the given control, looking in the first shape node
        :param linear: bool, Whether or not the RGB should be in linear space (matches viewport color)
        :return: tuple(float, float, float), new control color in float linear values (between 0.0 and 1.0)
        """

        if not self._shapes:
            return 0.0, 0.0, 0.0

        return node_utils.get_rgb_color(self._shapes[0], linear=linear)

    def match_translation(self, target):
        """
        Matches control translation to given target
        :param target:
        """

        maya.cmds.delete(maya.cmds.pointConstraint(target, self.get_top()))

        if dcc.name_is_right(self.side) and self.get_mirror():
            dcc.set_attribute_value(self.get(), 'rotateY', 0.0)

    def match_rotation(self, target):
        """
        Matches control rotation to given target
        :param target:
        """

        maya.cmds.delete(maya.cmds.orientConstraint(target, self.get_top()))

        if dcc.name_is_right(self.side) and self.get_mirror():
            dcc.set_attribute_value(self.get(), 'rotateY', 0.0)

    def match_translation_rotation(self, target):
        """
        Matches control translation and scale to given target
        :param target:
        """

        maya.cmds.delete(maya.cmds.pointConstraint(target, self.get_top()))
        maya.cmds.delete(maya.cmds.orientConstraint(target, self.get_top()))

        if dcc.name_is_right(self.side) and self.get_mirror():
            dcc.set_attribute_value(self.get(), 'rotateY', 0.0)

    def translate_cvs(self, x, y, z):
        """
        Translates control curve CVs in object space
        :param x: float
        :param y: float
        :param z: float
        """

        components = self._get_components()
        if not components:
            return False

        maya.cmds.move(x, y, z, components, relative=True, os=True, wd=True)

        return True

    def rotate_cvs(self, x, y, z):
        """
        Rotates control curve CVs in object space
        :param x: float
        :param y: float
        :param z: float
        """

        components = self._get_components()
        if not components:
            return False

        maya.cmds.rotate(x, y, z, components, relative=True)

        return True

    def scale_cvs(self, x, y, z, use_pivot=True):
        """
        Scales control curve CVs in object space
        :param x: float
        :param y: float
        :param z: float
        :param use_pivot: bool
        """

        components = self._get_components()
        if not components:
            return False

        if use_pivot:
            pivot = maya.cmds.xform(self.get(), query=True, rp=True, ws=True)
        else:
            shapes = shape_utils.get_shapes_of_type(self.get(), shape_type='nurbsCurve')
            if not shapes:
                return False
            components = shape_utils.get_components_from_shapes(shapes)
            bounding = transform_utils.BoundingBox(components)
            pivot = bounding.get_center()

        if components:
            maya.cmds.scale(x, y, z, components, pivot=pivot, r=True)

        return True

#     def show_translate_attributes(self):
#         """
#         Unlocks and set keyable the control's translate attributes
#         """
#
#         for axis in 'XYZ':
#             maya.cmds.setAttr('{}.translate{}'.format(self.get(), axis), lock=False, keyable=True)
#
#     def show_rotate_attributes(self):
#         """
#         Unlocks and set keyable the control's rotate attributes
#         """
#
#         for axis in 'XYZ':
#             maya.cmds.setAttr('{}.rotate{}'.format(self.get(), axis), lock=False, keyable=True)
#
#     def show_scale_attributes(self):
#         """
#         Unlocks and set keyable the control's scale attributes
#         """
#
#         for axis in 'XYZ':
#             maya.cmds.setAttr('{}.scale{}'.format(self.get(), axis), lock=False, keyable=True)
#
#     def hide_attributes(self, attributes=None):
#         """
#         Locks and hide the given attributes on the control. If no attributes given, hide translate, rotate, scale and
#         visibility
#         :param attributes:
#         :return:
#         """
#
#         if attributes:
#             attr_utils.hide_attributes(self.get(), attributes)
#         else:
#             self.hide_translate_attributes()
#             self.hide_rotate_attributes()
#             self.hide_scale_and_visibility_attributes()
#

    def has_root_buffer(self):
        """
        Returns whether or not control has a a root buffer
        :return: bool
        """

        root_group = self.get_root()
        if not root_group or root_group == self.get():
            return False

        return True

    def has_auto_buffer(self):
        """
        Returns whether or not control has a a root buffer
        :return: bool
        """

        auto_group = self.get_auto()
        if not auto_group or auto_group == self.get():
            return False

        return True

    def create_root(self, name=None, *args, **kwargs):
        """
        Creates a root buffer group above the control
        :return: str
        """

        suffix = kwargs.pop('suffix', 'root')
        name = name or 'root'

        if self.get_root(suffix=suffix):
            return self.get_root(suffix=suffix)

        top_parent = dcc.node_parent(self.get_top())

        new_group = self._create_group(suffix, name=name, *args, **kwargs)

        # MIRROR BEHAVIOUR
        # TODO: This should be optional
        mirror_group = None
        if self.side and dcc.name_is_right(self.side):
            mirror_group = self._create_group('mirror', name='mirror', *args, **kwargs)
            # dcc.match_translation_rotation(self.get(), mirror_group)
            dcc.set_attribute_value(mirror_group, 'scaleX', -1)
            if top_parent:
                dcc.set_parent(mirror_group, top_parent)

        auto_group = self.get_auto()
        if not auto_group:
            if mirror_group:
                dcc.set_parent(new_group, mirror_group)
                self.set_parent(new_group, parent_top=False)
                for xform in 'trs':
                    for axis in 'xyz':
                        attr_value = 1.0 if xform == 's' else 0.0
                        dcc.set_attribute_value(new_group, '{}{}'.format(xform, axis), attr_value)
            else:
                node_parent = dcc.node_parent(self.get())
                if node_parent:
                    dcc.set_parent(new_group, node_parent)
                self.set_parent(new_group, parent_top=False)
        else:
            if mirror_group:
                dcc.set_parent(new_group, mirror_group)
            else:
                auto_group_parent = dcc.node_parent(auto_group)
                if auto_group_parent:
                    new_group = dcc.set_parent(new_group, auto_group_parent)
            dcc.set_parent(auto_group, new_group)

        return new_group

    def create_auto(self, name=None, *args, **kwargs):
        """
        Creates an auto buffer group above the control
        :return: str
        """

        suffix = kwargs.pop('suffix', 'auto')
        name = name or 'auto'

        if self.get_auto(suffix=suffix):
            return self.get_auto(suffix=suffix)

        new_group = self._create_group(suffix, name=name, *args, **kwargs)
        node_parent = dcc.node_parent(self.get())
        if node_parent:
            new_group = dcc.set_parent(new_group, node_parent)

        root_group = self.get_root(suffix=kwargs.pop('auto_suffix', None))
        if root_group:
            if not dcc.node_short_name(dcc.node_parent(new_group)) == dcc.node_short_name(root_group):
                dcc.set_parent(new_group, root_group)
            for xform in 'trs':
                for axis in 'xyz':
                    attr_value = 1.0 if xform == 's' else 0.0
                    dcc.set_attribute_value(new_group, '{}{}'.format(xform, axis), attr_value)

        self.set_parent(new_group, parent_top=False)

        return new_group

    # def create_buffer(self, suffix='root', name=None):
    #     """
    #     Creates a buffer group above the control
    #     :return: str
    #     """
    #
    #     if not name and self._naming_file:
    #         parsed_name = self.parse_name(self.get())
    #         if 'node_type' in parsed_name:
    #             parsed_name['node_type'] = suffix
    #             name = self.solve_name(**parsed_name)
    #         else:
    #             name = self.solve_name(**parsed_name)
    #             name = '{}_{}'.format(name, suffix)
    #
    #     return transform_utils.create_buffer_group(self.get(), buffer_name=name, suffix=suffix)

#     def set_controls_file(self, controls_file):
#         """
#         Sets the file used to load controls curve data from
#         :param controls_file: str
#         """
#
#         self._controls_file = controls_file

    @decorators.undo_chunk
    def set_color(self, value):
        """
        Sets the color of the control shapes
        :param value: int or list, color defined by its RGB color or by its index
        """

        self.update_shapes()
        if not self._shapes:
            return

        node_utils.set_color(self._shapes, value)

#     @decorators.undo_chunk
#     def set_rotate_order(self, xyz_order):
#         """
#         Sets the rotate order of the control
#         :param xyz_order: str ('xyz', 'yzx', 'zxy', 'xzy', 'yxz', 'zyx')
#         """
#
#         xyz_orders = ['xyz', 'yzx', 'zxy', 'xzy', 'yxz', 'zyx']
#
#         if type(xyz_order) == int:
#             value = xyz_order
#         else:
#             value = 0
#             if xyz_order in xyz_orders:
#                 value = xyz_orders.index(xyz_order)
#
#         return maya.cmds.setAttr('{}.rotateOrder'.format(self._name, value))
#
#     def delete_shapes(self):
#         """
#         Delete all shapes beneath the control
#         """
#
#         shapes = shape_utils.get_shapes(self.get())
#         maya.cmds.delete(shapes)
#
#     @decorators.undo_chunk
#     def set_shape(self, shapes):
#         self.delete_shapes()
#         shapes = python.force_list(shapes)
#         if not shapes:
#             return
#         valid_shapes = list()
#         for shape in shapes:
#             if not shape_utils.is_shape(shape):
#                 shapes = dcc.list_shapes(shape) or list()
#                 valid_shapes.extend(shapes)
#             else:
#                 valid_shapes.append(shape)
#         valid_shapes = list(set(valid_shapes))
#         if not valid_shapes:
#             return
#
#         for shape in valid_shapes:
#             maya.cmds.parent(shape, self.get(), add=True, shape=True)
#
#         self.update_shapes()

#     @decorators.undo_chunk
#     def set_curve_as_text(self, text):
#         """
#         Updates the curves of the control with the given text (as curves)
#         :param text: str
#         """
#
#         if not self._shapes:
#             return False
#
#         color = node_utils.get_rgb_color(self._shapes[0])
#         curve_utils.set_shapes_as_text_curve(self.get(), text)
#         self.update_shapes()
#         node_utils.set_color(self._shapes, color)
#         maya.cmds.select(clear=True)
#
#         return True
#
#     @decorators.undo_chunk
#     def set_to_joint(self, joint=None, scale_compensate=False):
#         """
#         Updates the control to have a joint as its main transform type
#         :param joint: str, name of a joint to use. If not given, the joint will be created automatically
#         :param scale_compensate: bool, Whether to connect scale of parent to inverseScale of joint. This causes
#             the group above the joint to be able to change scale value without affect the control's look
#         """
#
#         maya.cmds.select(clear=True)
#
#         self.update_shapes()
#
#         name = self._name
#         joint_given = True
#         temp_parent = None
#         curve_type_value = ''
#
#         if not joint:
#             joint = maya.cmds.joint()
#             maya.cmds.delete(maya.cmds.parentConstraint(name, joint))
#             maya.cmds.delete(maya.cmds.parentConstraint(name, joint))
#             buffer_group = maya.cmds.group(empty=True, n=name_utils.find_unique_name('temp_{}'.format(joint)))
#             maya.cmds.parent(buffer_group, self._name)
#             maya.cmds.parent(joint, buffer_group)
#             maya.cmds.makeIdentity(buffer_group, t=True, r=True, s=True, jo=True, apply=True)
#             maya.cmds.parent(joint, w=True)
#             temp_parent = maya.cmds.listRelatives(joint, p=True)
#             maya.cmds.delete(buffer_group)
#             joint_given = False
#
#         if self._shapes:
#             for shape in self._shapes:
#                 maya.cmds.parent(shape, joint, r=True, s=True)
#
#         if joint_given:
#             transform_utils.transfer_relatives(name, joint, reparent=False)
#         else:
#             parent = maya.cmds.listRelatives(name, p=True)
#             if parent:
#                 maya.cmds.parent(joint, parent)
#                 if temp_parent:
#                     maya.cmds.delete(temp_parent)
#                 maya.cmds.makeIdentity(joint, r=True, s=True, apply=True)
#             transform_utils.transfer_relatives(name, joint)
#             if scale_compensate:
#                 parent = maya.cmds.listRelatives(joint, p=True)
#                 if parent:
#                     maya.cmds.connectAttr('{}.scale'.format(parent[0]), '{}.inverseScale'.format(joint))
#
#         transfer = attr_utils.TransferAttributes()
#         transfer.transfer_control(name, joint)
#         attr_utils.transfer_output_connections(name, joint)
#
#         maya.cmds.setAttr('{}.radius'.format(joint), lock=True, keyable=False, cb=False)
#         maya.cmds.setAttr('{}.drawStyle'.format(joint), 2)
#
#         if maya.cmds.objExists('{}.curveType'.format(name)):
#             curve_type_value = maya.cmds.getAttr('{}.curveType'.format(name))
#
#         maya.cmds.delete(name)
#
#         if not joint_given:
#             joint = maya.cmds.rename(joint, name)
#
#         self._name = joint
#
#         if joint_given:
#             shape_utils.rename_shapes(self._name)
#
#         string_attr = attr_utils.StringAttribute('curveType')
#         string_attr.create(joint)
#         string_attr.set_value(curve_type_value)
#
#         return True
#
#     @decorators.undo_chunk
#     def rename(self, new_name):
#         """
#         Gives a new name to the control
#         :param new_name: str
#         :return: str
#         """
#
#         new_name = name_utils.find_unique_name(new_name)
#         self._rename_message_groups(self._name, new_name)
#         new_name = maya.cmds.rename(self._name, new_name)
#         constraints = maya.cmds.listRelatives(new_name, type='constraint')
#         if constraints:
#             for constraint in constraints:
#                 new_constraint = constraint.replace(self.get(), new_name)
#                 maya.cmds.rename(constraint, new_constraint)
#         self._name = new_name
#         shape_utils.rename_shapes(self._name)
#         self.update_shapes()
#
#         return self._name
#
#     @decorators.undo_chunk
#     def delete_shapes(self):
#         """
#         Deletes all control shapes
#         """
#
#         self.update_shapes()
#         maya.cmds.delete(self._shapes)
#         self._shapes = list()
#
#     @decorators.undo_chunk
#     def copy_shapes(self, transform):
#         """
#         Copies all shapes from the given transform to the control transform
#         :param transform: str
#         """
#
#         if not shape_utils.has_shape_of_type(transform, 'nurbsCurve'):
#             return
#
#         orig_shapes = shape_utils.get_shapes_of_type(self._name, shape_type='nurbsCurve')
#
#         temp = maya.cmds.duplicate(transform)[0]
#         maya.cmds.parent(temp, self._name)
#         maya.cmds.makeIdentity(temp, apply=True, t=True, r=True, s=True)
#
#         shapes = shape_utils.get_shapes_of_type(temp, shape_type='nurbsCurve')
#         color = None
#         colors = dict()
#         if shapes:
#             index = 0
#             for shape in shapes:
#                 if index < len(orig_shapes) and index < len(shapes):
#                     color = node_utils.get_rgb_color(orig_shapes[index])
#                 colors[shape] = color
#                 if color:
#                     if type(color) != list:
#                         node_utils.set_color(shape, color)
#                     else:
#                         node_utils.set_rgb_color(shape, [color[0], color[1], color[2]])
#                 maya.cmds.parent(shape, self._name, r=True, shape=True)
#                 index += 1
#
#         maya.cmds.delete(orig_shapes)
#         maya.cmds.delete(temp)
#
#         shape_utils.rename_shapes(self._name)
#         self.update_shapes()
#
#     @decorators.undo_chunk
#     def update_color_respect_side(self, sub=False, center_tolerance=0.001):
#         """
#         Updates control shapes color taking into account the position of the control (left, right or center)
#         :param sub: bool, Whether to set the color to sub colors
#         :param center_tolerance: float, distance the control can be from center before it is considered left or right
#         :return:str, side of the control as letter ('L', 'R' or 'C')
#         """
#
#         color_value = None
#         side = 'C'
#         position = maya.cmds.xform(self.get(), query=True, ws=True, t=True)
#         if position[0] > 0:
#             color_value = dcc.get_color_of_side('L', sub)
#             side = 'L'
#         elif position[0] < 0:
#             color_value = dcc.get_color_of_side('R', sub)
#             side = 'R'
#         elif center_tolerance > position[0] > center_tolerance * -1:
#             color_value = dcc.get_color_of_side('C', sub)
#             side = 'C'
#
#         if type(color_value) == int or type(color_value) == float:
#             self.set_color(int(color_value))
#         else:
#             self.set_color_rgb(color_value[0], color_value[1], color_value[2])
#
#         return side
#
#     @dcc.undo_decorator()
#     def duplicate(self, delete_shapes=False, copy_scale_tracker=True):
#         """
#         Duplicates the control generating a new transform parented to the world
#         :param delete_shapes: bool, Whether or not delete the shape nodes of the original transform node
#         :param copy_scale_tracker: bool, Whether or not scale tracker attribute should be copied
#         :return:
#         """
#
#         scale_track = list()
#         scale_default = [1.0, 1.0, 1.0]
#
#         duplicated_control = transform_utils.duplicate_transform_without_children(
#             self._name, node_name='temp_control', delete_shapes=delete_shapes)
#         if delete_shapes:
#             self.update_shapes()
#
#         if maya.cmds.listRelatives(duplicated_control, parent=True, fullPath=True):
#             duplicated_control = maya.cmds.parent(duplicated_control, world=True, absolute=True)[0]
#
#         if maya.cmds.nodeType(duplicated_control) == 'joint':
#             dup_group = maya.cmds.group(empty=True, name='tempMirror_grp')
#             maya.cmds.matchTransform([dup_group, self._name], pos=True, rot=True, scl=False, piv=False)
#             duplicated_control = transform_utils.parent_transforms_shapes(
#                 dup_group, duplicated_control, delete_original=True)
#
#         if copy_scale_tracker:
#             None

    def _get_group_name(self, name, *args, **kwargs):
        if kwargs.get('force_suffix', True):
            kwargs['node_type'] = 'group'

        parsed_name = self.parse_name(self.get())

        if parsed_name:
            kwargs['force_suffix'] = False

        if name and self._naming_file:
            if 'node_type' in parsed_name:
                parsed_name['node_type'] = name
                name = self._get_name(*args, **parsed_name)
        else:
            base_name = self._get_name(*args, **parsed_name)
            name = '{}_{}'.format(base_name, name)

        return name

    # def _create_buffer(self, suffix, name=None, *args, **kwargs):
    #     """
    #     Internal function that creates new groups for the rig control
    #     :param group_name: str, name of the group
    #     :return:
    #     """
    #
    #     name = self._get_group_name(name, *args, **kwargs)
    #     new_group = transform_utils.create_buffer_group(self.get(), buffer_name=name, suffix=suffix)
    #
    #     return new_group

    def _create_group(self, suffix, name=None, *args, **kwargs):
        """
        Internal function that creates new groups for the rig control
        :param group_name: str, name of the group
        :return:
        """

        group_name = self._get_group_name(name, *args, **kwargs)
        new_group = dcc.create_empty_group(name=group_name)

        node_name_split = self.get().split('|')
        if len(node_name_split) == 1:
            attribute.connect_group_with_message(new_group, self.get(), suffix)
        else:
            node_root_name = '|'.join(node_name_split[:-1])
            buffer_node_name = '{}|{}|{}'.format(node_root_name, new_group, node_name_split[-1])
            attribute.connect_group_with_message(new_group, buffer_node_name, suffix)

        return new_group

    def _get_components(self):
        """
        Internal function that returns the geometry components of the control curve
        :return: list(str)
        """

        self.update_shapes()
        if not self._shapes:
            return
        return shape_utils.get_components_from_shapes(self._shapes)

#     def _rename_message_groups(self, search_name, replace_name):
#         """
#         Internal function that renames the message groups of the control
#         :param search_name: str
#         :param replace_name: str
#         """
#
#         message_attrs = attr_utils.get_message_attributes(search_name)
#         if message_attrs:
#             for attr_name in message_attrs:
#                 attr_node = '{}.{}'.format(search_name, attr_name)
#                 if attr_name.startswith('group'):
#                     node = attr_utils.get_attribute_input(attr_node, True)
#                     if node.find(search_name) > -1:
#                         new_node = node.replace(search_name, replace_name)
#                         self._rename_message_groups(node, new_node)
#                         constraints = maya.cmds.listRelatives(node, type='constraint')
#                         if constraints:
#                             for constraint in constraints:
#                                 new_constraint = constraint.replace(node, new_node)
#                                 maya.cmds.rename(constraint, new_constraint)
#                         maya.cmds.rename(node, new_node)
#
#
# def get_control_rgb_color(control_name, linear=True):
#     """
#     Returns the RGB color of the given control, looking in the first shape node
#     :param control_name: str, control transform node
#     :param linear: bool, Whether or not the RGB should be in linear space (matches viewport color)
#     :return: tuple(float, float, float), new control color in float linear values (between 0.0 and 1.0)
#     """
#
#     return MayaRigControl(control_name).get_rgb_color(linear=linear)
#
#
# def add_control_tracker_attributes(
#         control_name, translate=(1.0, 1.0, 1.0), rotate=(1.0, 1.0, 1.0), scale=(1.0, 1.0, 1.0),
#         rgb_color=None, control_type='circle'):
#     """
#     Adds tracker attributes to the given control transform node
#     :param control_name: str, name of the control transform node
#     :param translate: tuple(float, float, float), initial translation values
#     :param rotate: tuple(float, float, float), initial rotation values
#     :param scale: tuple(float, float, float), initial scale values
#     :param rgb_color: tuple(float, float, float), initial RGB color as linear float
#     :param control_type: str, initial control library type
#     """
#
#     transform_utils.add_transform_tracker_attributes(control_name, translate=translate, rotate=rotate, scale=scale)
#     color_utils.add_color_tracker_attributes(control_name, rgb_color=rgb_color)
#
#
# def rename_control(old_name, new_name):
#     """
#     Renames given control name with the new one
#     :param old_name: str
#     :param new_name: str
#     :return: str
#     """
#
#     return MayaRigControl(old_name).rename(new_name)
