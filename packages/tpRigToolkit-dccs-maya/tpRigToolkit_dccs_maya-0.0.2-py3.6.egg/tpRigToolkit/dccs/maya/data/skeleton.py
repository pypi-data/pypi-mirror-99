#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""
Module that contains Skeleton data implementation
"""

from __future__ import print_function, division, absolute_import

import os
import re
# import json
import logging

from tpDcc import dcc
# from tpDcc.libs.python import fileio
# from tpRigToolkit.core import data as rig_data

from tpDcc.libs.datalibrary.core import datapart


LOGGER = logging.getLogger('tpRigToolkit-core')


class SkeletonFileData(datapart.DataPart, object):

    DATA_TYPE = 'dcc.skeleton'
    MENU_ICON = 'skeleton_data'
    MENU_NAME = 'Skeleton'
    PRIORITY = 5
    EXTENSION = '.skl'

    _has_trait = re.compile(r'\.skl', re.I)

    # ============================================================================================================
    # OVERRIDES
    # ============================================================================================================

    @classmethod
    def can_represent(cls, identifier, only_extension=False):
        if SkeletonFileData._has_trait.search(identifier):
            if only_extension:
                return True
            if os.path.isfile(identifier):
                return True
        return False

    def type(self):
        return 'dcc.skeleton'

    def icon(self):
        return 'skeleton_data'

    def label(self):
        return os.path.basename(self.identifier())

    def menu_name(self):
        return 'Skeleton'

    def save(self, thumbnail='', **kwargs):
        """
        Saves all the given data to the item path on disk
        :param thumbnail: str
        :param kwargs: dict
        """

        LOGGER.debug('Saving {} | {}'.format(self.path, kwargs))

        super(SkeletonFileData, self).save(thumbnail=thumbnail, **kwargs)

        objects = kwargs.get('objects', None)
        if not objects:
            objects = dcc.selected_nodes(full_path=True)
            if not objects:
                LOGGER.warning(
                    'Select root node of the skeleton to export or the list of skeleton nodes to export')
                return False


#     def export_data(self, file_path=None, comment='-', create_version=True, *args, **kwargs):


#
#         file_folder = os.path.dirname(file_path)
#
#         root_nodes = list()
#         if len(objects) == 1:
#             root_nodes.append(objects[0])
#         else:
#             for object in objects:
#                 object_parent = dcc.node_parent(object, full_path=False)
#                 if not object_parent or not dcc.node_is_joint(object_parent):
#                     root_nodes.append(object_parent)
#         if not root_nodes:
#             LOGGER.warning('No root joints found!')
#             return False
#         if len(root_nodes) > 1:
#             LOGGER.warning(
#                 'Multiple root nodes found in skeleton. Only first one will be exported: {}'.format(root_nodes[0]))
#         root_node = root_nodes[0]
#
#         skeleton_data = dict()
#         child_nodes = dcc.list_children(root_node, children_type='transform')
#         child_nodes.insert(0, root_node)
#
#         skeleton_data['header'] = dict()
#         skeleton_data['data'] = list()
#
#         # store skeleton header
#         dcc_name = dcc.get_name()
#         skeleton_data['header']['dcc'] = dcc_name
#         skeleton_data['header']['up_axis'] = dcc.get_up_axis_name()
#
#         # store skeleton data
#         visited_nodes = dict()
#         for i, node in enumerate(child_nodes):
#             node_data = dict()
#             node_short_name = dcc.node_short_name(node, remove_namespace=True)
#             node_data['name'] = node_short_name
#             node_data['index'] = i
#             node_data['type'] = dcc.node_type(node)
#             visited_nodes[node_short_name] = i
#             world_matrix = dcc.node_world_matrix(node)
#             node_data['world_matrix'] = world_matrix
#             parent_index = None
#             parent_node = dcc.node_parent(node)
#             if parent_node:
#                 parent_short_name = dcc.node_short_name(parent_node, remove_namespace=True)
#                 if parent_short_name in visited_nodes:
#                     parent_index = visited_nodes[parent_short_name]
#             if parent_index is None:
#                 parent_index = -1
#             node_data['parent_index'] = parent_index
#
#             node_data['side'] = dcc.get_side_labelling(node)
#             node_data['bone_type'] = dcc.get_type_labelling(node)
#             node_data['bone_other_type'] = dcc.get_other_type_labelling(node)
#             node_data['draw_label'] = dcc.get_draw_label_labelling(node)
#
#             node_namespace = dcc.node_namespace(node) or ''
#             if node_namespace.startswith('|'):
#                 node_namespace = node_namespace[1:]
#             node_data['namespace'] = node_namespace
#
#             skeleton_data['data'].append(node_data)
#         if not skeleton_data:
#             LOGGER.warning('No skeleton data found!')
#             return False
#         LOGGER.info('Exporting Skeleton Data: {}'.format(skeleton_data))
#
#         try:
#             with open(file_path, 'w') as json_file:
#                 json.dump(skeleton_data, json_file, indent=2)
#         except IOError:
#             LOGGER.error('Skeleton data not saved to file {}'.format(file_path))
#             return False
#
#         LOGGER.info('Skeleton data exported successfully!')
#
#         version = fileio.FileVersion(file_folder)
#         version.save(comment)
#
#         return True
#
#     def import_data(self, file_path='', objects=None, namespace=None):
#
#         file_path = file_path or self.get_file()
#         if not file_path or not os.path.isfile(file_path):
#             LOGGER.warning('Impossible to import skeleton data from: "{}"'.format(file_path))
#             return False
#
#         with open(file_path, 'r') as fh:
#             skeleton_data = json.load(fh)
#         if not skeleton_data:
#             LOGGER.warning('No skeleton data found in file: "{}"'.format(file_path))
#             return False
#
#         header = skeleton_data.get('header', dict())
#         data = skeleton_data.get('data', dict())
#         if not data:
#             # to support back compatibility
#             data = skeleton_data
#
#         created_nodes = dict()
#         for node_data in data:
#             node_index = node_data.get('index', 0)
#             node_parent_index = node_data.get('parent_index', -1)
#             node_name = node_data.get('name', 'new_node')
#             node_type = node_data.get('type', 'joint')
#             node_namespace = namespace if namespace else node_data.get('namespace', '')
#             node_label_side = node_data.get('side', '')
#             node_label_type = node_data.get('bone_type', '')
#             node_label_other_type = node_data.get('bone_other_type', '')
#             node_label_draw = node_data.get('draw_label', False)
#             node_world_matrix = node_data.get(
#                 'world_matrix', [1.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0, 0.0, 1.0])
#             dcc.clear_selection()
#             if node_type == 'joint':
#                 new_node = dcc.create_joint(name=node_name)
#             else:
#                 new_node = dcc.create_empty_group(name=node_name)
#             dcc.set_node_world_matrix(new_node, node_world_matrix)
#             created_nodes[node_index] = {
#                 'node': new_node, 'parent_index': node_parent_index, 'namespace': node_namespace,
#                 'label_side': node_label_side, 'label_type': node_label_type,
#                 'label_other_type': node_label_other_type, 'label_draw': node_label_draw
#             }
#
#             if node_type == 'joint':
#                 dcc.zero_orient_joint(new_node)
#
#         for node_index, node_data in created_nodes.items():
#             parent_index = node_data['parent_index']
#             if parent_index <= -1:
#                 continue
#             node_data = created_nodes.get(node_index, None)
#             if not node_data:
#                 continue
#             node_name = node_data.get('node')
#
#             dcc.set_side_labelling(node_name, node_data.get('label_side'))
#             dcc.set_type_labelling(node_name, node_data.get('label_type'))
#             dcc.set_other_type_labelling(node_name, node_data.get('label_other_type'))
#             dcc.set_draw_label_labelling(node_name, node_data.get('label_draw'))
#
#             parent_node_data = created_nodes.get(parent_index, None)
#             if not parent_node_data:
#                 continue
#
#             parent_node_name = parent_node_data.get('node')
#             dcc.set_parent(node_name, parent_node_name)
#
#         # We assign namespaces once the hierarchy of nodes is created
#         for node_index, node_data in created_nodes.items():
#             node_name = node_data.get('node')
#             node_namespace = node_data.get('namespace')
#             if node_namespace:
#                 dcc.assign_node_namespace(node_name, node_namespace, force_create=True)
#
#         return True
