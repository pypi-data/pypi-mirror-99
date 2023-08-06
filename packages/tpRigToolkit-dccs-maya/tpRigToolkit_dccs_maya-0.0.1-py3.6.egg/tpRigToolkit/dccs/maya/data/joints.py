#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""
Module that contains Joints data implementation
"""

from __future__ import print_function, division, absolute_import

import os
import re
import json
import logging

from tpDcc import dcc
from tpDcc.core import dcc as core_dcc

from tpDcc.libs.datalibrary.core import datapart

LOGGER = logging.getLogger('tpRigToolkit-dccs-maya')


class JointsData(datapart.DataPart, object):

    DATA_TYPE = 'maya.joints'
    MENU_ICON = 'joints_data'
    MENU_NAME = 'Joints'
    PRIORITY = 5
    EXTENSION = '.joints'

    _has_trait = re.compile(r'\.joints$', re.I)

    @classmethod
    def can_represent(cls, identifier, only_extension=False):
        if JointsData._has_trait.search(identifier):
            if only_extension:
                return True
            if os.path.isfile(identifier):
                return True

        return False

    @classmethod
    def supported_dccs(cls):
        return [core_dcc.Dccs.Maya]

    def type(self):
        return 'maya.joints'

    def icon(self):
        return 'joints_data'

    def menu_name(cls):
        return 'Joints'

    def label(self):
        return os.path.basename(self.identifier())

    def extension(self):
        return '.joints'

    def functionality(self):
        return dict(
            import_data=self.import_data,
            export_data=self.export_data,
            save=self.save
        )

    def metadata_dict(self):
        return {
            'dccName': str(dcc.client().get_name()),
            'dccVersion': str(dcc.client().get_version()),
            'upAxis': str(dcc.client().get_up_axis_name())
        }

    def save(self, **kwargs):

        filepath = self.format_identifier()
        if not filepath.endswith(JointsData.EXTENSION):
            filepath = '{}{}'.format(filepath, JointsData.EXTENSION)

        if not filepath:
            LOGGER.warning('Impossible to save Maya Joints file because save file path not defined!')
            return

        objects = kwargs.get('objects', None)
        if not objects:
            objects = dcc.client().selected_nodes(full_path=True)
        if not objects:
            LOGGER.warning('Select root node of the skeleton to export or the list of skeleton nodes to export')
            return False

        LOGGER.debug('Saving {} | {}'.format(filepath, kwargs))

        joints_data = list()

        visited_nodes = dict()
        for i, node in enumerate(objects):
            node_data = dict()
            node_short_name = dcc.client().node_short_name(node, remove_namespace=True)
            node_data['name'] = node_short_name
            node_data['index'] = i
            node_data['type'] = dcc.client().node_type(node)
            node_data['world_matrix'] = dcc.client().node_world_matrix(node)
            visited_nodes[node_short_name] = i
            parent_index = None
            node_data['parent_name'] = ''
            parent_node = dcc.client().node_parent(node)
            if parent_node:
                parent_short_name = dcc.client().node_short_name(parent_node, remove_namespace=True)
                node_data['parent_name'] = parent_short_name
                if parent_short_name in visited_nodes:
                    parent_index = visited_nodes[parent_short_name]
            if parent_index is None:
                parent_index = -1
            node_data['parent_index'] = parent_index

            node_data['side'] = dcc.client().get_side_labelling(node)
            node_data['bone_type'] = dcc.client().get_type_labelling(node)
            node_data['bone_other_type'] = dcc.client().get_other_type_labelling(node)
            node_data['draw_label'] = dcc.client().get_draw_label_labelling(node)
            node_data['radius'] = dcc.client().get_joint_radius(node)

            node_namespace = dcc.client().node_namespace(node) or ''
            if node_namespace.startswith('|'):
                node_namespace = node_namespace[1:]
            node_data['namespace'] = node_namespace

            joints_data.append(node_data)

        if not joints_data:
            LOGGER.warning('No joints data found!')
            return False

        LOGGER.info('Saving joints data: {}'.format(joints_data))

        try:
            with open(filepath, 'w') as json_file:
                json.dump(joints_data, json_file, indent=2)
        except IOError:
            LOGGER.error('Joints data not saved to file {}'.format(filepath))
            return False

        LOGGER.debug('Saved {} successfully!'.format(filepath))

        return True

    def import_data(self, *args, **kwargs):

        filepath = self.format_identifier()
        if not filepath.endswith(JointsData.EXTENSION):
            filepath = '{}{}'.format(filepath, JointsData.EXTENSION)

        if not filepath or not os.path.isfile(filepath):
            LOGGER.warning('Impossible to import joints data from: "{}"'.format(filepath))
            return

        LOGGER.debug('Loading: {} | {}'.format(filepath, kwargs))

        with open(filepath, 'r') as fh:
            joints_data = json.load(fh)
        if not joints_data:
            LOGGER.warning('No joints data found in file: "{}"'.format(filepath))
            return False

        # TODO: Use metadata to verify DCC and also to create nodes with proper up axis
        metadata = self.metadata()

        nodes_list = list()
        created_nodes = dict()
        for node_data in joints_data:
            node_index = node_data.get('index', 0)
            node_parent_index = node_data.get('parent_index', -1)
            node_parent_name = node_data.get('parent_name', '')
            node_name = node_data.get('name', 'new_node')
            node_type = node_data.get('type', 'joint')
            node_namespace = node_data.get('namespace', '')
            node_label_side = node_data.get('side', '')
            node_label_type = node_data.get('bone_type', '')
            node_label_other_type = node_data.get('bone_other_type', '')
            node_label_draw = node_data.get('draw_label', False)
            node_radius = node_data.get('radius', 1.0)
            node_world_matrix = node_data.get(
                'world_matrix', [1.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0, 0.0, 1.0])
            dcc.client().clear_selection()
            if node_type == 'joint':
                new_node = dcc.client().create_joint(name=node_name)
            else:
                new_node = dcc.client().create_empty_group(name=node_name)
            dcc.client().set_node_world_matrix(new_node, node_world_matrix)
            created_nodes[node_index] = {
                'node': new_node, 'parent_index': node_parent_index, 'parent_name': node_parent_name,
                'namespace': node_namespace, 'label_side': node_label_side, 'label_type': node_label_type,
                'label_other_type': node_label_other_type, 'label_draw': node_label_draw, 'radius': node_radius
            }

            if node_type == 'joint':
                dcc.client().zero_orient_joint(new_node)

            nodes_list.append(new_node)

        for node_index, node_data in created_nodes.items():
            parent_index = node_data['parent_index']
            if parent_index < -1:
                continue
            node_data = created_nodes.get(node_index, None)
            if not node_data:
                continue
            node_name = node_data.get('node')

            dcc.client().set_side_labelling(node_name, node_data.get('label_side'))
            dcc.client().set_type_labelling(node_name, node_data.get('label_type'))
            dcc.client().set_other_type_labelling(node_name, node_data.get('label_other_type'))
            dcc.client().set_draw_label_labelling(node_name, node_data.get('label_draw'))
            dcc.client().set_joint_radius(node_name, node_data.get('radius'))

            parent_node_name = None
            parent_node_data = created_nodes.get(parent_index, None)
            if not parent_node_data:
                parent_node_name = node_data.get('parent_name', '')
                if not parent_node_name or not dcc.node_exists(parent_node_name):
                    continue

            if not parent_node_name:
                parent_node_name = parent_node_data.get('node')
            dcc.client().set_parent(node_name, parent_node_name)

        # We assign namespaces once the hierarchy of nodes is created
        for node_index, node_data in created_nodes.items():
            node_name = node_data.get('node')
            node_namespace = node_data.get('namespace')
            if node_namespace:
                dcc.client().assign_node_namespace(node_name, node_namespace, force_create=True)

        # dcc.client().select_node(nodes_list)
        # dcc.client().fit_view()
        dcc.client().clear_selection()

        LOGGER.debug('Loaded: {} | {}'.format(filepath, kwargs))

        return nodes_list

    def export_data(self, *args, **kwargs):

        filepath = self.format_identifier()
        if not filepath.endswith(JointsData.EXTENSION):
            filepath = '{}{}'.format(filepath, JointsData.EXTENSION)

        if not filepath or not os.path.isfile(filepath):
            LOGGER.warning('Impossible to export joints data to: "{}"'.format(filepath))
            return

        LOGGER.debug('Exporting: {} | {}'.format(filepath, kwargs))

        with open(filepath, 'r') as fh:
            joints_data = json.load(fh)
        if not joints_data:
            LOGGER.warning('No joints data found in file: "{}"'.format(filepath))
            return False

        selected_nodes = dcc.client().selected_nodes(full_path=False)

        saved_nodes = list()
        if not selected_nodes:
            for node_data in joints_data:
                node_name = node_data.get('name')
                if not node_name:
                    continue
                saved_nodes.append(node_name)
        else:
            for selected_node in selected_nodes:
                if selected_node not in saved_nodes:
                    saved_nodes.append(selected_node)

        valid_nodes = list()
        for selected_node in saved_nodes:
            if not dcc.client().node_exists(selected_node):
                continue
            valid_nodes.append(selected_node)

        if not valid_nodes:
            LOGGER.warning('No joints to export to file found: "{}"'.format(filepath))
            return False

        return self.save(objects=valid_nodes)
