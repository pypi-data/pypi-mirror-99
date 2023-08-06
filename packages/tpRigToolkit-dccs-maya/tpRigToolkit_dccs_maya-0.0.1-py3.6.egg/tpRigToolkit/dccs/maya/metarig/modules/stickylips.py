#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""
Module that contains sticky meta rig implemetnations
"""

from __future__ import print_function, division, absolute_import

from tpDcc import dcc
from tpDcc.dccs.maya.meta import metanode
from tpDcc.dccs.maya.core import constraint

from tpRigToolkit.managers import names
from tpRigToolkit.dccs.maya.metarig.core import module, mixin


class StickyLips(module.RigModule, mixin.JointMixin):

    UPPER_PART = 'Upper'
    LOWER_PART = 'Lower'

    def __init__(self, *args, **kwargs):
        super(StickyLips, self).__init__(*args, **kwargs)

        if self.cached:
            return

        mixin.JointMixin.__init__(self)
        self.set_name(kwargs.get('name', 'stickyLips'))
        self.set_locators([])
        self.set_count(5)
        self.set_degree(1.3)
        self.set_follow_y(1)
        self.set_follow_z(1.5)

    # ==============================================================================================
    # STATIC METHODS
    # ==============================================================================================

    @classmethod
    def create_guides(cls, naming_file, count=5, rule_name=None, center_side=None, left_side=None, right_side=None):
        def _name(*args, **kwargs):
            side = kwargs.pop('side', center_side)
            return names.solve_name(side=side, rule_name=rule_name, naming_file=naming_file, *args, **kwargs)

        rule_name = rule_name or 'node'
        center_side = center_side or 'center'
        left_side = left_side or 'left'
        right_side = right_side or 'right'
        sides = [left_side, right_side]

        for part in [cls.UPPER_PART, cls.LOWER_PART]:
            part_factor = 1 if part == cls.UPPER_PART else -1
            mid_loc = dcc.create_locator(_name('jaw{}'.format(part), 'lip', node_type='guide'))
            dcc.set_attribute_value(mid_loc, 'translate', (0, part_factor, 0))

            for side in sides:
                for i in range(count):
                    factor = i + 1 if side == left_side else -(i + 1)
                    loc_data = (factor, part_factor, 0)
                    loc = dcc.create_locator(
                        _name('jaw{}'.format(part), 'lip', id=i, side=side, node_type='guide'))
                    dcc.set_attribute_value(loc, 'translate', loc_data)

        left_corner_loc = dcc.create_locator(_name('jawCorner', 'lip', side=left_side, node_type='guide'))
        right_corner_loc = dcc.create_locator(_name('jawCorner', 'lip', side=right_side, node_type='guide'))
        dcc.set_attribute_value(left_corner_loc, 'translate', (count + 1, 0, 0))
        dcc.set_attribute_value(right_corner_loc, 'translate', (-(count + 1), 0, 0))

        jaw_guide = dcc.create_locator(_name('jaw', node_type='guide'))
        jaw_inverse_guide = dcc.create_locator(_name('jawInverse', node_type='guide'))
        dcc.set_attribute_value(jaw_guide, 'translate', (0, -1, -count))
        dcc.set_attribute_value(jaw_inverse_guide, 'translate', (0, 1, -count))

        dcc.clear_selection()

    # ==============================================================================================
    # OVERRIDES
    # ==============================================================================================

    def create(self, *args, **kwargs):
        super(StickyLips, self).create(*args, **kwargs)

        center_side = self.center_side if self.has_attr('center_side') else 'center'
        left_side = self.left_side if self.has_attr('left_side') else 'left'
        right_side = self.left_side if self.has_attr('right_side') else 'right'
        if not self.has_attr('center_side'):
            self.add_attribute('center_side', center_side)
        if not self.has_attr('left_side'):
            self.add_attribute('left_side', left_side)
        if not self.has_attr('right_side'):
            self.add_attribute('right_side', right_side)
        sides = [left_side, right_side]

        guides_lookup = self._check_guides(sides=sides)
        if not guides_lookup:
            raise Exception('Not all locators are valid!')

        self._create_groups()
        self._parent_locators(sides=sides)
        self._create_jaw_base_joints()
        self._create_minor_joints()
        self._create_broad_joints()
        self._constraint_broad_joints()
        for part in [self.UPPER_PART, self.LOWER_PART]:
            self._create_seal(part)
        self._create_jaw_attributes()
        self._create_constraints()
        for part in [self.UPPER_PART, self.LOWER_PART]:
            self._create_initial_values(part)
        self._create_offset_follow()
        for part in [self.UPPER_PART, self.LOWER_PART]:
            self._create_seal_setup(part)
        self._create_jaw_pin()

    # ==============================================================================================
    # BASE
    # ==============================================================================================

    def get_locators(self, as_meta=True):
        return self.message_list_get('locators', as_meta=as_meta)

    def get_jaw_guides(self, as_meta=True):
        return self.message_list_get('jaw_guides', as_meta=as_meta)

    def get_lip_guides(self, as_meta=True):
        return self.message_list_get('lip_guides', as_meta=as_meta)

    def get_minor_joints(self, as_meta=True):
        return self.message_list_get('minor_joints', as_meta=as_meta)

    def set_count(self, joints_count):
        """
        Sets the total amount of joints in each side of the lips
        :param joints_count: int
        """

        if not self.has_attr('joints_count'):
            self.add_attribute(attr='joints_count', value=joints_count)
        else:
            self.joints_count = joints_count

    def set_degree(self, degree):
        """
        Sets the degree amount used by the lips joints
        :param degree: float
        """

        if not self.has_attr('degree'):
            self.add_attribute(attr='degree', value=degree)
        else:
            self.degree = degree

    def set_follow_y(self, follow_y):
        """
        Sets the follow amount in Y global axis used by the jaw joint
        :param follow_y: float
        """

        if not self.has_attr('follow_y'):
            self.add_attribute(attr='follow_y', value=follow_y)
        else:
            self.follow_y = follow_y

    def set_follow_z(self, follow_z):
        """
        Sets the follow amount in Z global axis used by the jaw joint
        :param follow_z: float
        """

        if not self.has_attr('follow_z'):
            self.add_attribute(attr='follow_z', value=follow_z)
        else:
            self.follow_z = follow_z

    def set_locators(self, locators):
        """
        Sets the locators used by the sticky lips rig
        :param locators: list(MetaObject)
        :return:
        """

        if not self.message_list_get('locators', as_meta=False):
            self.message_list_connect('locators', locators)
        else:
            self.message_list_purge('locators')
            for loc in locators:
                self.message_list_append('locators', loc)

    # ==============================================================================================
    # INTERNAL
    # ==============================================================================================

    def _check_guides(self, sides):
        """
        Checks whether or not setup guides are available and store them in proper variables
        """

        current_locators = dict()
        for loc in self.get_locators():
            current_locators[dcc.node_short_name(loc.meta_node)] = loc

        lip_guides = list()

        lookup = {
            self.center_side: dict(),
            self.left_side: dict(),
            self.right_side: dict()
        }

        for part in [self.UPPER_PART, self.LOWER_PART]:
            mid_loc = self._get_name('jaw{}'.format(part), node_type='guide', unique_name=False)
            if mid_loc not in current_locators:
                return None
            self.add_attribute('mid_{}_guide'.format(part), current_locators[mid_loc], attr_type='messageSimple')
            lookup[self.center_side].setdefault(part, list())
            lookup[self.center_side][part].append(current_locators[mid_loc])
            lip_guides.append(current_locators[mid_loc])

            for side in sides:
                lookup[side].setdefault(part, list())
                for i in range(self.joints_count):
                    loc = self._get_name(
                        'jaw{}'.format(part), id=i, side=side, node_type='guide', unique_name=False)
                    if loc not in current_locators:
                        return False
                    self.add_attribute(
                        'lip_{}_{}_{}_guide'.format(part, side, i), current_locators[loc], attr_type='messageSimple')
                    lip_guides.append(current_locators[loc])
                    lookup[side][part].append(current_locators[loc])

        for side in sides:
            corner_loc = self._get_name('jawCorner', side=side, node_type='guide', unique_name=False)
            if corner_loc not in current_locators:
                return None
            self.add_attribute(
                'jawCorner_{}_guide'.format(side), current_locators[corner_loc], attr_type='messageSimple')
            lip_guides.append(current_locators[corner_loc])
            lookup[side].setdefault('corner', current_locators[corner_loc])

        jaw_loc = self._get_name('jaw', node_type='guide', unique_name=False)
        jaw_inverse_loc = self._get_name('jawInverse', node_type='guide', unique_name=False)
        if jaw_loc not in current_locators or jaw_inverse_loc not in current_locators:
            return None
        self.add_attribute('jaw_guide', current_locators[jaw_loc], attr_type='messageSimple')
        self.add_attribute('jawInverse_guide', current_locators[jaw_inverse_loc], attr_type='messageSimple')

        self.message_list_connect('lip_guides', lip_guides)
        self.message_list_connect('jaw_guides', [current_locators[jaw_loc], current_locators[jaw_inverse_loc]])

        return lookup

    def _create_groups(self):
        """
        Internal function that creates base group used by the rig
        """

        jaw_guide_grp = dcc.create_empty_group(self._get_name('jaw', node_type='group'))
        locs_grp = dcc.create_empty_group(self._get_name('jawLip', node_type='group'))
        lip_locs_grp = dcc.create_empty_group(self._get_name('jawLipMinor', node_type='group'))
        jaw_base_guide_grp = dcc.create_empty_group(self._get_name('base', node_type='group'))
        lip_minor_grp = dcc.create_empty_group(self._get_name('lipMinor', node_type='group'))
        lip_broad_grp = dcc.create_empty_group(self._get_name('lipBroad', node_type='group'))
        seal_grp = dcc.create_empty_group(self._get_name('seal', node_type='group'))
        jaw_attribute_grp = dcc.create_empty_group(self._get_name('jawAttributes', node_type='group'))

        jaw_guide_grp = metanode.validate_obj_arg(jaw_guide_grp, 'MetaObject', update_class=True)
        locs_grp = metanode.validate_obj_arg(locs_grp, 'MetaObject', update_class=True)
        lip_locs_grp = metanode.validate_obj_arg(lip_locs_grp, 'MetaObject', update_class=True)
        jaw_base_guide_grp = metanode.validate_obj_arg(jaw_base_guide_grp, 'MetaObject', update_class=True)
        lip_minor_grp = metanode.validate_obj_arg(lip_minor_grp, 'MetaObject', update_class=True)
        lip_broad_grp = metanode.validate_obj_arg(lip_broad_grp, 'MetaObject', update_class=True)
        seal_grp = metanode.validate_obj_arg(seal_grp, 'MetaObject', update_class=True)
        jaw_attribute_grp = metanode.validate_obj_arg(jaw_attribute_grp, 'MetaObject', update_class=True)

        self.add_attribute('jaw_guide_group', jaw_guide_grp, attr_type='messageSimple')
        self.add_attribute('locators_group', locs_grp, attr_type='messageSimple')
        self.add_attribute('lip_locators_group', lip_locs_grp, attr_type='messageSimple')
        self.add_attribute('jaw_base_guide_group', jaw_base_guide_grp, attr_type='messageSimple')
        self.add_attribute('lip_minor_group', lip_minor_grp, attr_type='messageSimple')
        self.add_attribute('lip_broad_group', lip_broad_grp, attr_type='messageSimple')
        self.add_attribute('seal_group', seal_grp, attr_type='messageSimple')
        self.add_attribute('jaw_attributes', jaw_attribute_grp, attr_type='messageSimple')

        jaw_guide_grp.set_parent(self.setup_group)
        locs_grp.set_parent(jaw_guide_grp)
        lip_locs_grp.set_parent(locs_grp)
        lip_minor_grp.set_parent(locs_grp)
        lip_broad_grp.set_parent(locs_grp)
        jaw_base_guide_grp.set_parent(jaw_guide_grp)
        seal_grp.set_parent(jaw_guide_grp)
        jaw_attribute_grp.set_parent(jaw_guide_grp)

    def _parent_locators(self, sides):
        for part in [self.UPPER_PART, self.LOWER_PART]:
            self.get_attr('mid_{}_guide'.format(part), as_attr=False).set_parent(self.lip_locators_group)
            for side in sides:
                for i in range(self.joints_count):
                    self.get_attr(
                        'lip_{}_{}_{}_guide'.format(part, side, i), as_attr=False).set_parent(self.lip_locators_group)

        for side in sides:
            self.get_attr('jawCorner_{}_guide'.format(side), as_attr=False).set_parent(self.lip_locators_group)

        self.get_attr('jaw_guide', as_attr=False).set_parent(self.jaw_base_guide_group)
        self.get_attr('jawInverse_guide', as_attr=False).set_parent(self.jaw_base_guide_group)

    def _create_jaw_base_joints(self):

        jaw_pos = dcc.node_world_matrix(self.get_attr('jaw_guide', as_attr=False).meta_node)
        jaw_inverse_pos = dcc.node_world_matrix(self.get_attr('jawInverse_guide', as_attr=False).meta_node)

        jaw_joint = dcc.create_joint(self._get_name('jaw', node_type='joint'))
        dcc.set_node_world_matrix(jaw_joint, jaw_pos)
        dcc.clear_selection()
        inverse_jaw_joint = dcc.create_joint(self._get_name('jawInverse', node_type='joint'))
        dcc.set_node_world_matrix(inverse_jaw_joint, jaw_inverse_pos)
        dcc.clear_selection()

        jaw_joint = metanode.validate_obj_arg(jaw_joint, 'MetaObject', update_class=True)
        inverse_jaw_joint = metanode.validate_obj_arg(inverse_jaw_joint, 'MetaObject', update_class=True)

        self.add_attribute('jaw_joint', jaw_joint, attr_type='messageSimple')
        self.add_attribute('inverse_jaw_joint', inverse_jaw_joint, attr_type='messageSimple')

        jaw_joint.set_parent(self.jaw_base_guide_group)
        dcc.set_attribute_value(jaw_joint.meta_node, 'radius', 0.5 * self.scale)
        jaw_buffer = dcc.create_buffer_group(jaw_joint.meta_node)
        jaw_buffer = metanode.validate_obj_arg(jaw_buffer, 'MetaObject', update_class=True)
        self.add_attribute('jaw_joint_buffer', jaw_buffer, attr_type='messageSimple')

        inverse_jaw_joint.set_parent(self.jaw_base_guide_group)
        dcc.set_attribute_value(inverse_jaw_joint.meta_node, 'radius', 0.5 * self.scale)
        jaw_inverse_buffer = dcc.create_buffer_group(inverse_jaw_joint.meta_node)
        jaw_inverse_buffer = metanode.validate_obj_arg(jaw_inverse_buffer, 'MetaObject', update_class=True)
        self.add_attribute('jaw_inverse_joint_buffer', jaw_inverse_buffer, attr_type='messageSimple')

        self.add_joints([jaw_joint, inverse_jaw_joint])

        dcc.clear_selection()

    def _create_minor_joints(self):

        minor_joints = list()

        for guide in self.get_lip_guides():
            dcc.clear_selection()
            xform_matrix = dcc.node_world_matrix(guide.meta_node)
            joint_name = dcc.node_short_name(guide.meta_node).replace('guide', 'jnt')
            guide_joint = dcc.create_joint(joint_name)
            dcc.set_attribute_value(guide_joint, 'radius', 0.25 * self.scale)
            dcc.set_node_world_matrix(guide_joint, xform_matrix)
            guide_joint = metanode.validate_obj_arg(guide_joint, 'MetaObject', update_class=True)
            guide_joint.set_parent(self.lip_minor_group)
            minor_joints.append(guide_joint)

        self.message_list_connect('minor_joints', minor_joints)
        self.add_joints(minor_joints)

        dcc.clear_selection()

    def _create_broad_joints(self):

        dcc.clear_selection()

        upper_pos = dcc.node_world_matrix(
            self.get_attr('mid_{}_guide'.format(self.UPPER_PART), as_attr=False).meta_node)
        lower_pos = dcc.node_world_matrix(
            self.get_attr('mid_{}_guide'.format(self.LOWER_PART), as_attr=False).meta_node)
        left_pos = dcc.node_world_matrix(self.get_attr('jawCorner_left_guide', as_attr=False).meta_node)
        right_pos = dcc.node_world_matrix(self.get_attr('jawCorner_right_guide', as_attr=False).meta_node)

        upper_joint = dcc.create_joint(self._get_name('broadUpper', node_type='joint'))
        dcc.set_node_world_matrix(upper_joint, upper_pos)
        dcc.clear_selection()
        lower_joint = dcc.create_joint(self._get_name('broadLower', node_type='joint'))
        dcc.set_node_world_matrix(lower_joint, lower_pos)
        dcc.clear_selection()
        left_joint = dcc.create_joint(self._get_name('broadCorner', side='left', node_type='joint'))
        dcc.set_node_world_matrix(left_joint, left_pos)
        dcc.clear_selection()
        right_joint = dcc.create_joint(self._get_name('broadCorner', side='right', node_type='joint'))
        dcc.set_node_world_matrix(right_joint, right_pos)
        dcc.clear_selection()

        upper_joint = metanode.validate_obj_arg(upper_joint, 'MetaObject', update_class=True)
        lower_joint = metanode.validate_obj_arg(lower_joint, 'MetaObject', update_class=True)
        left_joint = metanode.validate_obj_arg(left_joint, 'MetaObject', update_class=True)
        right_joint = metanode.validate_obj_arg(right_joint, 'MetaObject', update_class=True)

        self.add_attribute('broad_upper_joint', upper_joint, attr_type='messageSimple')
        self.add_attribute('broad_lower_joint', lower_joint, attr_type='messageSimple')
        self.add_attribute('broad_left_joint', left_joint, attr_type='messageSimple')
        self.add_attribute('broad_right_joint', right_joint, attr_type='messageSimple')

        joints = [upper_joint, lower_joint, left_joint, right_joint]
        for joint in joints:
            joint.set_parent(self.lip_broad_group)
            dcc.set_attribute_value(joint.meta_node, 'radius', 0.5 * self.scale)
        self.add_joints(joints)

        dcc.clear_selection()

    def _get_lip_parts(self, cache=True):

        if self.has_attr('lookup_lip_parts') and cache:
            return self.lookup_lip_parts

        lip_joints = [dcc.node_short_name(lip_joint.meta_node) for lip_joint in self.get_minor_joints()]

        broad_upper = self.broad_upper_joint
        broad_lower = self.broad_lower_joint
        broad_left = self.broad_left_joint
        broad_right = self.broad_right_joint

        lookup = {
            self.center_side: {self.UPPER_PART: dict(), self.LOWER_PART: dict()},
            self.left_side: {self.UPPER_PART: dict(), self.LOWER_PART: dict(), 'corner': dict()},
            self.right_side: {self.UPPER_PART: dict(), self.LOWER_PART: dict(), 'corner': dict()},
        }

        for joint in lip_joints:
            parse_joint = names.parse_name(joint)
            side = parse_joint['side']
            if side == self.center_side or side == self.center_side[0]:
                if self.UPPER_PART in parse_joint['description']:
                    lookup[self.center_side][self.UPPER_PART][joint] = [broad_upper.meta_node]
                elif self.LOWER_PART in parse_joint['description']:
                    lookup[self.center_side][self.LOWER_PART][joint] = [broad_lower.meta_node]
            elif side == self.left_side or side == self.left_side[0]:
                if parse_joint['description'] == 'jawCorner':
                    lookup[self.left_side]['corner'][joint] = [broad_left.meta_node]
                elif self.UPPER_PART in parse_joint['description']:
                    lookup[self.left_side][self.UPPER_PART][joint] = [broad_upper.meta_node, broad_left.meta_node]
                elif self.LOWER_PART in parse_joint['description']:
                    lookup[self.left_side][self.LOWER_PART][joint] = [broad_lower.meta_node, broad_left.meta_node]
            elif side == self.right_side or side == self.right_side[0]:
                if parse_joint['description'] == 'jawCorner':
                    lookup[self.right_side]['corner'][joint] = [broad_right.meta_node]
                elif self.UPPER_PART in parse_joint['description']:
                    lookup[self.right_side][self.UPPER_PART][joint] = [broad_upper.meta_node, broad_right.meta_node]
                elif self.LOWER_PART in parse_joint['description']:
                    lookup[self.right_side][self.LOWER_PART][joint] = [broad_lower.meta_node, broad_right.meta_node]

        if self.has_attr('lookup_lip_parts'):
            self.lookup_lip_parts = lookup
        else:
            self.add_attribute('lookup_lip_parts', lookup, attr_type='complex')

        return lookup

    def _get_lip_part(self, part):
        lip_parts_dict = self._get_lip_parts()
        lip_parts = [
            reversed(sorted(list(lip_parts_dict[self.left_side][part].keys()))),
            list(lip_parts_dict[self.center_side][part].keys()),
            sorted(list(lip_parts_dict[self.right_side][part].keys())),
        ]

        return [joint for joint in lip_parts for joint in joint]

    def _constraint_broad_joints(self):

        # create offset to broad joints
        upper_offset = dcc.create_buffer_group(self.broad_upper_joint.meta_node)
        lower_offset = dcc.create_buffer_group(self.broad_lower_joint.meta_node)
        left_offset = dcc.create_buffer_group(self.broad_left_joint.meta_node)
        right_offset = dcc.create_buffer_group(self.broad_right_joint.meta_node)

        # create constraints to broad joints
        dcc.create_parent_constraint(upper_offset, self.inverse_jaw_joint.meta_node, maintain_offset=True)
        dcc.create_parent_constraint(lower_offset, self.jaw_joint.meta_node, maintain_offset=True)
        dcc.create_parent_constraint(left_offset, [upper_offset, lower_offset], maintain_offset=True)
        dcc.create_parent_constraint(right_offset, [upper_offset, lower_offset], maintain_offset=True)

        upper_offset = metanode.validate_obj_arg(upper_offset, 'MetaObject', update_class=True)
        lower_offset = metanode.validate_obj_arg(lower_offset, 'MetaObject', update_class=True)
        left_offset = metanode.validate_obj_arg(left_offset, 'MetaObject', update_class=True)
        right_offset = metanode.validate_obj_arg(right_offset, 'MetaObject', update_class=True)

        self.add_attribute('upper_broad_offset', upper_offset, attr_type='messageSimple')
        self.add_attribute('lower_broad_offset', lower_offset, attr_type='messageSimple')
        self.add_attribute('left_broad_offset', left_offset, attr_type='messageSimple')
        self.add_attribute('right_broad_offset', right_offset, attr_type='messageSimple')

        dcc.clear_selection()

    def _create_seal(self, part):
        seal_nodes = list()
        lip_part_joints = self._get_lip_part(part)
        value = len(lip_part_joints)
        for index, joint_name in enumerate(lip_part_joints):
            seal_group_name = dcc.node_short_name(joint_name).replace('jnt', 'seal')
            seal_node = dcc.create_empty_group(seal_group_name)
            joint_matrix = dcc.node_world_matrix(joint_name)
            dcc.set_node_world_matrix(seal_node, joint_matrix)
            seal_constraint = dcc.create_parent_constraint(
                seal_node, [self.broad_left_joint.meta_node, self.broad_right_joint.meta_node], maintain_offset=True)
            dcc.set_attribute_value(seal_constraint, 'interpType', 2)       # shortest interpolation to avoid flips
            seal_node = metanode.validate_obj_arg(seal_node, 'MetaObject', update_class=True)
            seal_node.set_parent(self.seal_group)
            seal_nodes.append(seal_node)

            right_corner_value = float(index) / float(value - 1)
            left_corner_value = 1 - right_corner_value
            weight_names = constraint.Constraint().get_weight_names(seal_constraint)
            left_corner_attr = weight_names[0]
            right_corner_attr = weight_names[1]
            dcc.set_attribute_value(seal_constraint, left_corner_attr, left_corner_value)
            dcc.set_attribute_value(seal_constraint, right_corner_attr, right_corner_value)

        self.message_list_connect('seal{}_groups'.format(part), seal_nodes)

    def _create_jaw_attributes(self):
        lip_parts = self._get_lip_parts()
        jaw_attributes = self.jaw_attributes.meta_node

        # center upper attributes
        joints = sorted(list(lip_parts[self.center_side][self.UPPER_PART].keys()))
        for joint in joints:
            joint_name = dcc.node_short_name(joint)
            dcc.add_float_attribute(jaw_attributes, joint_name, min_value=0, max_value=1, default_value=0)
            dcc.lock_attribute(jaw_attributes, joint_name)

        # left upper attributes
        joints = sorted(list(lip_parts[self.left_side][self.UPPER_PART].keys()))
        for joint in joints:
            joint_name = dcc.node_short_name(joint)
            dcc.add_float_attribute(jaw_attributes, joint_name, min_value=0, max_value=1, default_value=0)

        # left corner attributes
        left_corner_joint = dcc.node_short_name(list(lip_parts[self.left_side]['corner'].keys())[0])
        dcc.add_float_attribute(jaw_attributes, left_corner_joint, min_value=0, max_value=1, default_value=1)
        dcc.lock_attribute(jaw_attributes, left_corner_joint)

        # left lower attributes
        joints = sorted(list(lip_parts[self.left_side][self.LOWER_PART].keys()))[::-1]
        for joint in joints:
            joint_name = dcc.node_short_name(joint)
            dcc.add_float_attribute(jaw_attributes, joint_name, min_value=0, max_value=1, default_value=0)

        # center lower attributes
        joints = sorted(list(lip_parts[self.center_side][self.LOWER_PART].keys()))
        for joint in joints:
            joint_name = dcc.node_short_name(joint)
            dcc.add_float_attribute(jaw_attributes, joint_name, min_value=0, max_value=1, default_value=0)
            dcc.lock_attribute(jaw_attributes, joint_name)

        # follow attributes
        dcc.add_float_attribute(jaw_attributes, 'follow_ty', min_value=-10, max_value=10, default_value=0)
        dcc.add_float_attribute(jaw_attributes, 'follow_tz', min_value=-10, max_value=10, default_value=0)

        # seal attributes
        dcc.add_double_attribute(
            jaw_attributes, 'seal_{}'.format(self.left_side), min_value=0, max_value=10, default_value=0)
        dcc.add_double_attribute(
            jaw_attributes, 'seal_{}'.format(self.right_side), min_value=0, max_value=10, default_value=0)
        dcc.add_double_attribute(
            jaw_attributes, 'seal_delay_{}'.format(self.left_side), min_value=0.1, max_value=10, default_value=4)
        dcc.add_double_attribute(
            jaw_attributes, 'seal_delay_{}'.format(self.right_side), min_value=0.1, max_value=10, default_value=4)

    def _create_constraints(self):

        lip_parts = self._get_lip_parts()
        jaw_attrs = self.jaw_attributes.meta_node

        for side, parts_data in lip_parts.items():
            for part, joints_data in parts_data.items():
                for lip_joint, broad_joints in joints_data.items():
                    parse_joint = names.parse_name(lip_joint)
                    joint_side = parse_joint['side']
                    seal_name = lip_joint.replace('jnt', 'seal')
                    if not dcc.node_exists(seal_name):
                        seal_constraint = dcc.create_parent_constraint(lip_joint, broad_joints)
                        dcc.set_attribute_value(seal_constraint, 'interpType', 2)
                        continue

                    seal_constraint = dcc.create_parent_constraint(
                        lip_joint, broad_joints + [seal_name], maintain_offset=True)
                    dcc.set_attribute_value(seal_constraint, 'interpType', 2)
                    weight_names = constraint.Constraint().get_weight_names(seal_constraint)
                    if len(broad_joints) == 1:
                        seal_weight_attr = weight_names[1]
                        rev_node = dcc.create_node('reverse', node_name=lip_joint.replace('jnt', 'rev'))
                        dcc.connect_attribute(seal_constraint, seal_weight_attr, rev_node, 'inputX')
                        dcc.connect_attribute(rev_node, 'outputX', seal_constraint, weight_names[0])
                        dcc.set_attribute_value(seal_constraint, seal_weight_attr, 0)
                    elif len(broad_joints) == 2:
                        seal_weight_attr = weight_names[2]
                        dcc.set_attribute_value(seal_constraint, seal_weight_attr, 0)

                        seal_rev = dcc.create_node('reverse', node_name=lip_joint.replace('jnt', 'sealRev'))
                        jaw_rev_attr = dcc.create_node('reverse', node_name=lip_joint.replace('jnt', 'jawAttrRev'))
                        seal_mult = dcc.create_node('multiplyDivide', node_name=lip_joint.replace('jnt', 'sealMul'))

                        joint_attr = lip_joint.replace('_{}_'.format(joint_side), '_l_')

                        dcc.connect_attribute(seal_constraint, seal_weight_attr, seal_rev, 'inputX')
                        dcc.connect_attribute(seal_rev, 'outputX', seal_mult, 'input2X')
                        dcc.connect_attribute(seal_rev, 'outputX', seal_mult, 'input2Y')
                        dcc.connect_attribute(jaw_attrs, joint_attr, seal_mult, 'input1Y')
                        dcc.connect_attribute(jaw_attrs, joint_attr, jaw_rev_attr, 'inputX')
                        dcc.connect_attribute(jaw_rev_attr, 'outputX', seal_mult, 'input1X')
                        dcc.connect_attribute(seal_mult, 'outputX', seal_constraint, weight_names[0])
                        dcc.connect_attribute(seal_mult, 'outputY', seal_constraint, weight_names[1])

    def _create_initial_values(self, part):
        lip_part = self._get_lip_part(part)
        lip_joints = list()
        for lip_joint in lip_part:
            parse_joint = names.parse_name(lip_joint)
            if parse_joint['side'] != 'l':
                continue
            lip_joints.append(lip_joint)
        value = len(lip_joints)

        for index, attr_name in enumerate(lip_joints[::-1]):
            linear_value = float(index) / float(value - 1)
            div_value = linear_value / self.degree
            final_value = div_value * linear_value
            dcc.set_attribute_value(self.jaw_attributes.meta_node, attr_name, final_value)

    def _create_offset_follow(self):

        jaw_attributes = self.jaw_attributes.meta_node

        follow_group = dcc.create_empty_group(self._get_name('jawFollow', node_type='buffer'))
        follow_group = metanode.validate_obj_arg(follow_group, 'MetaObject', update_class=True)
        self.add_attribute('jaw_follow_buffer', follow_group, attr_type='messageSimple')
        follow_group.set_parent(dcc.node_parent(self.jaw_joint_buffer.meta_node))
        self.jaw_joint_buffer.set_parent(follow_group)

        unit = dcc.create_node('unitConversion', node_name=self._get_name('follow', node_type='unitConversion'))
        remap_y = dcc.create_node('remapValue', node_name=self._get_name('followY', node_type='remapValue'))
        remap_z = dcc.create_node('remapValue', node_name=self._get_name('followZ', node_type='remapValue'))
        mult_y = dcc.create_node('multDoubleLinear', node_name=self._get_name('followY', node_type='multDoubleLinear'))

        dcc.set_attribute_value(remap_y, 'inputMax', 1)
        dcc.set_attribute_value(remap_z, 'inputMax', 1)
        dcc.set_attribute_value(mult_y, 'input2', -1)

        dcc.connect_attribute(self.jaw_joint.meta_node, 'rx', unit, 'input')
        dcc.connect_attribute(unit, 'output', remap_y, 'inputValue')
        dcc.connect_attribute(unit, 'output', remap_z, 'inputValue')
        dcc.connect_attribute(jaw_attributes, 'follow_ty', mult_y, 'input1')
        dcc.connect_attribute(jaw_attributes, 'follow_tz', remap_z, 'outputMax')
        dcc.connect_attribute(mult_y, 'output', remap_y, 'outputMax')
        dcc.connect_attribute(remap_y, 'outValue', follow_group.meta_node, 'ty')
        dcc.connect_attribute(remap_z, 'outValue', follow_group.meta_node, 'tz')

        dcc.set_attribute_value(jaw_attributes, 'follow_ty', self.follow_y)
        dcc.set_attribute_value(jaw_attributes, 'follow_tz', self.follow_z)

    def _create_seal_setup(self, part):

        jaw_attrs = self.jaw_attributes.meta_node
        seal_name = 'seal{}'.format(part)
        lip_joints = self._get_lip_part(part)
        value = len(lip_joints)
        seal_driver = dcc.create_node('lightInfo', node_name=self._get_name(seal_name, node_type='driver'))

        triggers = {self.left_side: list(), self.right_side: list()}

        for side in [self.left_side, self.right_side]:
            delay_sub_name = self._get_name('{}Delay'.format(seal_name), side=side, node_type='plusMinusAverage')
            delay_sub = dcc.create_node('plusMinusAverage', node_name=delay_sub_name)
            dcc.set_attribute_value(delay_sub, 'operation', 2)
            dcc.set_attribute_value(delay_sub, 'input1D[0]', 10)
            dcc.connect_attribute(jaw_attrs, 'seal_delay_{}'.format(side), delay_sub, 'input1D[1]')
            lerp = 1 / float(value - 1)
            delay_div_name = self._get_name('jawDelay', side=side, node_type='multDoubleLinear')
            delay_div = dcc.create_node('multDoubleLinear', node_name=delay_div_name)
            dcc.set_attribute_value(delay_div, 'input2', lerp)
            dcc.connect_attribute(delay_sub, 'output1D', delay_div, 'input1')

            mult_triggers = list()
            sub_triggers = list()
            triggers[side].append(mult_triggers)
            triggers[side].append(sub_triggers)

            for index in range(value):

                # create mult node
                delay_mult_name = self._get_name(
                    '{}Delay'.format(seal_name), side=side, id=index, node_type='multDoubleLinear')
                delay_mult = dcc.create_node('multDoubleLinear', node_name=delay_mult_name)
                dcc.set_attribute_value(delay_mult, 'input1', index)
                dcc.connect_attribute(delay_div, 'output', delay_mult, 'input2')
                mult_triggers.append(delay_mult)

                # create sub node
                delay_sub_name = self._get_name(
                    '{}Delay'.format(seal_name), side=side, id=index, node_type='plusMinusAverage')
                delay_sub = dcc.create_node('plusMinusAverage', node_name=delay_sub_name)
                dcc.connect_attribute(delay_mult, 'output', delay_sub, 'input1D[0]')
                dcc.connect_attribute(jaw_attrs, 'seal_delay_{}'.format(side), delay_sub, 'input1D[1]')
                sub_triggers.append(delay_sub)

        # get constraints
        constraint_targets = list()
        for lip_joint in lip_joints:
            attrs = dcc.list_attributes('{}_parentConstraint1'.format(lip_joint), ud=True)
            for attr in attrs:
                if 'seal' in attr:
                    constraint_targets.append('{}_parentConstraint1.{}'.format(lip_joint, attr))

        # connect seal triggers to driver
        for left_index, const_target in enumerate(constraint_targets):
            right_index = value - left_index - 1
            # right_index = num_spans - left_index - 1
            index_name = '{}{}'.format(seal_name, left_index)

            left_mult_trigger = triggers[self.left_side][0][left_index]
            left_sub_trigger = triggers[self.left_side][1][left_index]
            right_mult_trigger = triggers[self.right_side][0][right_index]
            right_sub_trigger = triggers[self.right_side][1][right_index]

            # left side
            left_remap_name = self._get_name('{}Remap'.format(seal_name), side=self.left_side, node_type='remapValue')
            left_remap = dcc.create_node('remapValue', node_name=left_remap_name)
            dcc.set_attribute_value(left_remap, 'outputMax', 1)
            dcc.set_attribute_value(left_remap, 'value[0].value_Interp', 2)
            dcc.connect_attribute(left_mult_trigger, 'output', left_remap, 'inputMin')
            dcc.connect_attribute(left_sub_trigger, 'output1D', left_remap, 'inputMax')
            dcc.connect_attribute(jaw_attrs, 'seal_{}'.format(self.left_side), left_remap, 'inputValue')

            # right side
            right_sub_name = self._get_name(
                '{}Sub'.format(seal_name), side=self.right_side, node_type='plusMinusAverage')
            right_sub = dcc.create_node('plusMinusAverage', node_name=right_sub_name)
            dcc.set_attribute_value(right_sub, 'input1D[0]', 1)
            dcc.set_attribute_value(right_sub, 'operation', 2)  # subtraction
            dcc.connect_attribute(left_remap, 'outValue', right_sub, 'input1D[1]')
            right_remap_name = self._get_name('{}Remap'.format(seal_name), side=self.right_side, node_type='remapValue')
            right_remap = dcc.create_node('remapValue', node_name=right_remap_name)
            dcc.set_attribute_value(right_remap, 'outputMax', 1)
            dcc.set_attribute_value(right_remap, 'value[0].value_Interp', 2)
            dcc.connect_attribute(right_mult_trigger, 'output', right_remap, 'inputMin')
            dcc.connect_attribute(right_sub_trigger, 'output1D', right_remap, 'inputMax')
            dcc.connect_attribute(jaw_attrs, 'seal_{}'.format(self.right_side), right_remap, 'inputValue')
            dcc.connect_attribute(right_sub, 'output1D', right_remap, 'outputMax')

            # final addition of both sides
            plus_name = self._get_name(seal_name, side=self.left_side, node_type='plusMinusAverage')
            plus = dcc.create_node('plusMinusAverage', node_name=plus_name)
            dcc.connect_attribute(left_remap, 'outValue', plus, 'input1D[0]')
            dcc.connect_attribute(right_remap, 'outValue', plus, 'input1D[1]')
            clamp_name = self._get_name('{}Clamp'.format(seal_name), side=self.left_side, node_type='remapValue')
            clamp = dcc.create_node('remapValue', node_name=clamp_name)
            dcc.connect_attribute(plus, 'output1D', clamp, 'inputValue')
            dcc.add_double_attribute(seal_driver, index_name, min_value=0, max_value=1, default_value=0)
            dcc.connect_attribute(clamp, 'outValue', seal_driver, index_name)

            # connect to constraint
            constraint_name, constraint_attr = const_target.split('.')
            dcc.connect_attribute(seal_driver, index_name, constraint_name, constraint_attr)

    def _create_jaw_pin(self):
        jaw_attrs = self.jaw_attributes.meta_node
        pin_driver = dcc.create_node('lightInfo', node_name=self._get_name('pin', node_type='driver'))
        for side in [self.left_side, self.right_side]:

            # create attributes
            dcc.add_bool_attribute(jaw_attrs, '{}_auto_corner_pin'.format(side))
            dcc.add_double_attribute(
                jaw_attrs, '{}_corner_pin'.format(side), min_value=-10, max_value=10, default_value=0)
            dcc.add_double_attribute(
                jaw_attrs, '{}_input_ty'.format(side), min_value=-10, max_value=10, default_value=0)

            # create clamp and connect the input_ty to it
            clamp = dcc.create_node('clamp', node_name=self._get_name('cornerPinAuto', side=side, node_type='clamp'))
            dcc.set_attribute_value(clamp, 'minR', -10)
            dcc.set_attribute_value(clamp, 'maxR', 10)
            dcc.connect_attribute(jaw_attrs, '{}_input_ty'.format(side), clamp, 'inputR')

            # create condition for the two possible scenarios
            condition_name = self._get_name('cornerPinAuto', side=side, node_type='condition')
            condition = dcc.create_node('condition', node_name=condition_name)
            dcc.set_attribute_value(condition, 'operation', 0)
            dcc.set_attribute_value(condition, 'secondTerm', 1)
            dcc.connect_attribute(jaw_attrs, '{}_auto_corner_pin'.format(side), condition, 'firstTerm')
            dcc.connect_attribute(clamp, 'outputR', condition, 'colorIfTrueR')
            dcc.connect_attribute(jaw_attrs, '{}_corner_pin'.format(side), condition, 'colorIfFalseR')

            # create addition
            plus_name = self._get_name('cornerPin', side=side, node_type='plusMinusAverage')
            plus = dcc.create_node('plusMinusAverage', node_name=plus_name)
            dcc.set_attribute_value(plus, 'input1D[1]', 10)
            dcc.connect_attribute(condition, 'outColorR', plus, 'input1D[0]')

            # create division
            div_name = self._get_name('cornerPin', side=side, node_type='multDoubleLinear')
            div = dcc.create_node('multDoubleLinear', node_name=div_name)
            dcc.set_attribute_value(div, 'input2', 0.05)
            dcc.connect_attribute(plus, 'output1D', div, 'input1')

            # add final output attributes to the driver node
            dcc.add_double_attribute(pin_driver, '{}_pin'.format(side), min_value=0, max_value=1, default_value=0)
            dcc.connect_attribute(div, 'output', pin_driver, '{}_pin'.format(side))

            # connect driver to broad joint constraint targets
            corner_offset = self.get_attr('{}_broad_offset'.format(side), as_attr=False).meta_node
            corner_constraint = dcc.list_node_constraints(corner_offset)[0]
            corner_constraint_weight_names = constraint.Constraint().get_weight_names(corner_constraint)
            upper_constraint_weight_name = corner_constraint_weight_names[0]
            lower_constraint_weight_name = corner_constraint_weight_names[1]
            dcc.connect_attribute(pin_driver, '{}_pin'.format(side), corner_constraint, upper_constraint_weight_name)
            rev_node_name = self._get_name('cornerPin', side=side, node_type='reverse')
            rev_node = dcc.create_node('reverse', node_name=rev_node_name)
            dcc.connect_attribute(pin_driver, '{}_pin'.format(side), rev_node, 'inputX')
            dcc.connect_attribute(rev_node, 'outputX', corner_constraint, lower_constraint_weight_name)
