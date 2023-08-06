#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""
Module that contains data Maya Skin Cluster weights
"""

from __future__ import print_function, division, absolute_import

import os
import re
import json
import logging
import threading
from collections import OrderedDict

from tpDcc import dcc
from tpDcc.core import dcc as core_dcc
from tpDcc.libs.python import python, fileio, folder, path as path_utils

# from tpRigToolkit.core import data

from tpDcc.libs.datalibrary.core import datapart

logger = logging.getLogger('tpRigToolkit-dccs-maya')


class SkinWeightsData(datapart.DataPart):

    DATA_TYPE = 'maya.skincluster'
    MENU_ICON = 'maya'
    MENU_NAME = 'Skin Cluster Weights'
    PRIORITY = 10
    EXTENSION = '.skin'

    _has_trait = re.compile(r'\.skin$', re.I)

    @classmethod
    def can_represent(cls, identifier, only_extension=False):
        if SkinWeightsData._has_trait.search(identifier):
            if only_extension:
                return True
            if os.path.isfile(identifier):
                return True

        return False

    @classmethod
    def supported_dccs(cls):
        return [core_dcc.Dccs.Maya]

    def label(self):
        return os.path.basename(self.identifier())

    def extension(self):
        return '.skin'

    def icon(self):
        return 'maya'

    def type(self):
        return 'maya.skincluster'

    def menu_name(self):
        return 'Skin Cluster Weights'

    def save_schema(self):
        """
        Returns the schema used for saving the item
        :return: dict
        """

        return [
            {
                'name': 'objects',
                'type': 'objects',
                'layout': 'vertical',
                'errorVisible': True
            }
        ]

    def save_validator(self, **kwargs):
        """
        Validates the given save fields
        Called when an input field has changed
        :param kwargs: dict
        :return: list(dict)
        """

        fields = list()

        selection = dcc.client().selected_nodes() or list()
        msg = ''
        if not selection:
            msg = 'No objects selected. Please select at least one object.'

        fields.append({'name': 'objects', 'value': selection, 'error': msg})

        return fields

    def functionality(self):
        return dict(
            move=self.move,
            save=self.save,
            import_data=self.import_data,
            export_data=self.export_data
        )

    def move(self, new_folder):

        if not new_folder or not os.path.isdir(new_folder):
            return

        identifier = self.format_identifier()

        file_directory, file_name, file_extension = path_utils.split_path(identifier)
        new_path = path_utils.join_path(new_folder, '{}{}'.format(file_name, file_extension))

        valid = fileio.move_file(self.format_identifier(), new_path)
        if not valid:
            return

        dependencies = self.get_dependencies()

        self._db.move(identifier, new_path)

        skin_folder = dependencies.get('skin_folder', None)
        if not skin_folder or not os.path.isdir(skin_folder):
            return

        skin_folder_item = self.library.get(skin_folder)
        move_function = skin_folder_item.functionality().get('move')
        if move_function:
            move_function(new_folder)

        return new_folder

    def save(self, *args, **kwargs):

        dependencies = dict()

        filepath = self.format_identifier()
        if not filepath.endswith(SkinWeightsData.EXTENSION):
            filepath = '{}{}'.format(filepath, SkinWeightsData.EXTENSION)

        if not filepath:
            logger.warning('Impossible to save Maya Skin Weights file because save file path not defined!')
            return

        objects = kwargs.get('objects', None)
        if not objects:
            objects = dcc.client().selected_nodes(full_path=True)
        if not objects:
            logger.warning(
                'Nothing selected to export skin weights of. Please, select a mesh,'
                ' curve, NURBS surface or lattice with skin weights to export')
            return False

        logger.debug('Saving {} | {}'.format(filepath, kwargs))

        valid_nodes = list()

        # Check that all objects that we are going to export have at least one skin cluster node associated
        # Make sure also that all objects skin output folder have been created
        obj_dirs = OrderedDict()
        skin_nodes = OrderedDict()
        geo_paths = OrderedDict()
        skin_weights = OrderedDict()
        for obj in objects:
            if dcc.client().node_is_a_shape(obj):
                obj = dcc.client().node_parent(obj, full_path=True)
            obj_filename = obj
            if obj.find('|') > -1:
                obj_filename = obj_filename.replace('|', '.')
                if obj_filename.startswith('.'):
                    obj_filename = obj_filename[1:]
            if obj_filename.find(':') > -1:
                obj_filename = obj_filename.replace(':', '-')

            skin = dcc.client().find_deformer_by_type(obj, 'skinCluster')
            if not skin:
                logger.warning('Skip skin weights export for object because no skinCluster found!'.format(obj))
                continue
            valid_nodes.append((obj, obj_filename, skin))

        if not valid_nodes:
            logger.warning('Skin exported failed! No objects found with skinClusters applied!')
            return False

        # Create skin folder only is valid nodes are available
        file_name = '.{}'.format(os.path.basename(filepath))
        file_folder = path_utils.join_path(os.path.dirname(filepath), file_name)
        if not os.path.isdir(file_folder):
            skin_folder = folder.create_folder(file_folder, make_unique=True)
            dependencies[skin_folder] = 'skin_folder'

        for node_data in valid_nodes:
            obj, obj_filename, skin = node_data

            geo_path = path_utils.join_path(file_folder, obj_filename)
            if path_utils.is_dir(geo_path):
                folder.delete_folder(obj_filename, file_folder)
            geo_path = folder.create_folder(obj_filename, file_folder)
            if not geo_path:
                logger.error(
                    'Unable to create skin weights directory: "{}" in "{}"'.format(obj_filename, file_folder))
                return False
            dependencies[geo_path] = 'geo_path'

            weights = dcc.client().get_skin_weights(skin)

            obj_dirs[obj] = obj_filename
            skin_nodes[obj] = skin
            geo_paths[obj] = geo_path
            skin_weights[obj] = weights

        for (obj, skin_node), (_, geo_path), (_, skin_weights) in zip(
                skin_nodes.items(), geo_paths.items(), skin_weights.items()):

            logger.info('Exporting weights: {} > {} --> "{}"'.format(obj, skin_node, geo_path))

            info_lines = list()
            info_file = fileio.create_file('influence.info', geo_path)
            dependencies[info_file] = 'info_file'

            for influence in skin_weights:
                if influence is None or influence == 'None':
                    continue
                weight_list = skin_weights[influence]
                if not weight_list:
                    continue
                thread = LoadWeightFileThread()
                influence_line, weight_path = thread.run(influence, skin_node, skin_weights[influence], geo_path)
                if influence_line:
                    info_lines.append(influence_line)
                if weight_path and os.path.isfile(weight_path):
                    dependencies[weight_path] = 'weight'

            writer = fileio.FileWriter(info_file)
            writer.write(info_lines)

            settings_file = fileio.create_file('settings.info', geo_path)
            dependencies[settings_file] = 'settings'
            setting_lines = list()
            if dcc.client().node_has_shape_of_type(obj, 'mesh'):
                mesh_path = self._export_mesh_obj(obj, geo_path)
                if mesh_path and os.path.isfile(mesh_path):
                    dependencies[mesh_path] = 'geo_file'

            if dcc.client().attribute_exists(skin_node, 'blendWeights'):
                blend_weights = dcc.client().get_skin_blend_weights(skin_node)
                setting_lines.append("['blendWeights', {}]".format(blend_weights))
            if dcc.client().attribute_exists(skin_node, 'skinningMethod'):
                skin_method = dcc.client().get_attribute_value(skin_node, 'skinningMethod')
                setting_lines.append("['skinningMethod', {}]".format(skin_method))

            write_settings = fileio.FileWriter(settings_file)
            write_settings.write(setting_lines)

            logger.info('Skin weights exported successfully: {} > {} --> "{}"'.format(obj, skin_node, geo_path))

        data_to_save = OrderedDict()
        for obj, obj_filename in obj_dirs.items():
            data_to_save[obj] = {'enabled': True, 'folder': obj_filename}
        with open(filepath, 'w') as fh:
            json.dump(data_to_save, fh)

        logger.info('Skin weights export operation completed successfully!')

        return dependencies

    def export_data(self, **kwargs):
        filepath = self.format_identifier()
        if not filepath.endswith(SkinWeightsData.EXTENSION):
            filepath = '{}{}'.format(filepath, SkinWeightsData.EXTENSION)

        if not filepath or not os.path.isfile(filepath):
            logger.warning('Impossible to export skin weights data to: "{}"'.format(filepath))
            return

        objects = kwargs.get('objects', list())
        selected_objects = dcc.client().selected_nodes(full_path=True)
        objects = list(set(objects + selected_objects))
        kwargs['objects'] = objects

        # TODO: Retrieve dependencies
        # At this moment, if we rename the skin data, skin data folder is not renamed so when we resave the skin
        # data, old folder will not be taken into account

        return self.save(**kwargs)

    def import_data(self, **kwargs):

        filepath = self.format_identifier()
        if not filepath.endswith(SkinWeightsData.EXTENSION):
            filepath = '{}{}'.format(filepath, SkinWeightsData.EXTENSION)

        if not filepath:
            logger.warning('Impossible to load Maya Skin Weights from file: "{}"!'.format(filepath))
            return False

        with open(filepath, 'r') as fh:
            skin_data = json.load(fh)
        if not skin_data:
            logger.warning('No skin data found in file: "{}"'.format(filepath))
            return False

        file_folder = os.path.dirname(filepath)
        file_dependencies = self.get_dependencies()

        objects = kwargs.get('objects', None)
        if not objects:
            objects = dcc.client().selected_nodes(full_path=True) or list()

        for obj in objects:
            if obj in skin_data:
                continue
            skin_data[obj] = {'folder': dcc.client().node_short_name(obj), 'enabled': True}

        skin_folder = file_dependencies.get('skin_folder', None)

        for obj, obj_data in skin_data.items():
            obj_folder = obj_data.get('folder', None)
            if not obj_folder:
                continue

            obj_enabled = obj_data.get('enabled', False)

            if skin_folder and os.path.isdir(skin_folder):
                obj_path = path_utils.join_path(skin_folder, obj_folder)
            else:
                default_skin_folder = path_utils.join_path(
                    file_folder, '.{}{}'.format(self.name(), SkinWeightsData.EXTENSION))
                if os.path.isdir(default_skin_folder):
                    obj_path = path_utils.join_path(default_skin_folder, obj_folder)
                else:
                    obj_path = path_utils.join_path(file_folder, obj_folder)

            if not obj_enabled or not os.path.isdir(obj_path):
                continue
            obj_exists = dcc.client().node_exists(obj)
            if not obj_exists:
                continue

            self._import_skin_weights(obj_path, obj)

        # self._center_view()

        logger.info('Imported "{}" skin data'.format(self.name()))

        return True

#     def get_skin_meshes(self, file_path=None):
#         """
#         Returns all skinned meshes fro ma .skin file
#         :param file_path: str
#         :return: list(str)
#         """
#
#         if not dcc.is_maya():
#             return
#
#         file_path = file_path or self.get_file()
#         if not file_path or not os.path.isfile(file_path):
#             return
#         skin_path = path_utils.join_path(path_utils.get_dirname(file_path), self.name)
#
#         meshes = None
#         if path_utils.is_dir(skin_path):
#             meshes = folder.get_folders(skin_path)
#
#         return meshes
#
#     def remove_mesh(self, mesh, file_path=None):
#         """
#         Removes a mesh from a .skin file
#         :param mesh: str
#         :param file_path: str
#         :return: bool
#         """
#
#         if not dcc.is_maya():
#             return
#
#         file_path = file_path or self.get_file()
#         if not file_path or not os.path.isfile(file_path):
#             return
#         skin_path = path_utils.join_path(path_utils.get_dirname(file_path), self.name)
#
#         folder.delete_folder(mesh, skin_path)
#         test_path = path_utils.join_path(skin_path, mesh)
#
#         return bool(path_utils.is_dir(test_path))

    # ============================================================================================================
    # INTERNAL
    # ============================================================================================================

    def _export_mesh_obj(self, mesh, data_path):
        """
        Internal function that exports given mesh object (creates a backup of the mesh in disk)
        :param mesh: str
        :param data_path: str
        """

        dcc.client().load_plugin('objExport')

        envelope_value = dcc.client().get_skin_envelope(mesh)
        dcc.client().set_skin_envelope(mesh, 0)

        dcc.client().select_node(mesh)
        mesh_path = '{}/mesh.obj'.format(data_path)

        dcc.client().export_current_selection(
            mesh_path, 'OBJexport', preserve_references=False, force=True,
            options="groups=0;ptgroups=0;materials=0;smoothing=0;normals=0")

        dcc.client().set_skin_envelope(mesh, envelope_value)

        return mesh_path

    def _import_mesh_obj(self, data_path):
        """
        Internal function that imports mesh object stored in given path
        :param data_path: str, path that contains already exported mesh object
        :return: str, name of the imported mesh
        """

        dependencies = self.get_dependencies(data_path)
        mesh_path = dependencies.get('geo_file', None)
        if not mesh_path or not os.path.isfile(mesh_path):
            mesh_path = path_utils.join_path(data_path, 'mesh.obj')
        if not path_utils.is_file(mesh_path):
            return None

        nodes = dcc.client().list_nodes(node_type='mesh', full_path=False)
        dcc.client().import_file(mesh_path, import_type='OBJ', ignore_version=True, options='mo=1')
        current_nodes = dcc.client().list_nodes(node_type='mesh', full_path=False)
        delta = list(set(current_nodes).difference(nodes))
        if delta:
            delta = dcc.client().node_parent(delta, full_path=True)

        return delta

    def _import_skin_weights(self, data_path, mesh):

        if not dcc.client().node_exists(mesh) or not os.path.isdir(data_path):
            return False

        dependencies = self.get_dependencies(data_path)

        is_valid_mesh = False
        shape_types = ['mesh', 'nurbsSurface', 'nurbsCurve', 'lattice']
        for shape_type in shape_types:
            if dcc.client().node_has_shape_of_type(mesh, shape_type):
                is_valid_mesh = True
                break
        if not is_valid_mesh:
            logger.warning(
                'Node "{}" is not a valid mesh node! Currently supported nodes include: {}'.format(mesh, shape_types))
            return False

        logger.info('Importing skin clusters {} --> "{}"'.format(mesh, data_path))

        influence_dict = self._get_influences(data_path)
        if not influence_dict:
            logger.warning('No influences data found for: {}'.format(mesh))
            return False

        influences = list(influence_dict.keys())
        if not influences:
            logger.warning('No influences found for: "{}"'.format(mesh))
            return False
        influences.sort()
        logger.debug('Influences found for {}: {}'.format(mesh, influences))

        short_name = dcc.client().node_short_name(mesh)
        transfer_mesh = None

        if dcc.client().node_has_shape_of_type(mesh, 'mesh'):
            orig_mesh = self._import_mesh_obj(data_path)
            if orig_mesh:
                mesh_match = dcc.client().meshes_are_similar(orig_mesh, mesh)
                if not mesh_match:
                    transfer_mesh = mesh
                    mesh = orig_mesh
                else:
                    dcc.client().delete_node(orig_mesh)

        # Check if there are duplicated influences and also for the creation of influences that does not currently
        # in the scene
        add_joints = list()
        remove_entries = list()
        for inf in influences:
            joints = dcc.client().list_nodes(inf, full_path=True)
            if type(joints) == list and len(joints) > 1:
                add_joints.append(joints[0])
                jnts_count = len(joints)
                logger.warning(
                    'Found {} joints with name {}. Using only the first one: {}'.format(jnts_count, inf, joints[0]))
                remove_entries.append(inf)
                inf = joints[0]
            if not dcc.client().node_exists(inf):
                dcc.client().clear_selection()
                dcc.client().create_joint(name=inf, position=influence_dict[inf]['position'])
        for entry in remove_entries:
            influences.remove(entry)
        influences += add_joints

        # Create skin cluster and removes if it already exists
        orig_skin = dcc.client().find_deformer_by_type(mesh, 'skinCluster')
        if orig_skin:
            dcc.client().delete_node(orig_skin)

        skin_cluster_name = orig_skin if orig_skin else dcc.client().find_unique_name('skin_%s' % short_name)
        skin_cluster = dcc.client().create_skin(mesh, influences, only_selected_influences=True, name=skin_cluster_name)
        dcc.client().set_attribute_value(skin_cluster, 'normalizeWeights', 0)
        dcc.client().clear_skin_weights(skin_cluster)

        dcc.client().apply_skin_influences_from_data(skin_cluster, influences=influences, influence_dict=influence_dict)

        dcc.client().set_skin_normalize_weights_mode(skin_cluster, 1)   # interactive normalization
        dcc.client().set_skin_force_normalize_weights(skin_cluster, True)

        settings_path = dependencies.get('settings', None)
        if not settings_path or not os.path.isfile(settings_path):
            settings_path = path_utils.join_path(data_path, 'settings.info')

        if path_utils.is_file(settings_path):
            lines = fileio.get_file_lines(settings_path)
            for line in lines:
                test_line = line.strip()
                if not test_line:
                    continue
                line_list = eval(line)
                attr_name = line_list[0]
                value = line_list[1]
                if attr_name == 'blendWeights':
                    dcc.client().set_skin_blend_weights(skin_cluster, value)
                else:
                    if dcc.client().attribute_exists(skin_cluster, attr_name):
                        dcc.client().set_attribute_value(skin_cluster, attr_name, value)

        if transfer_mesh:
            logger.info('Import sking weights: mesh topology does not match. Trying to transfer topology ...')
            dcc.client().skin_mesh_from_mesh(mesh, transfer_mesh)
            dcc.client().delete_node(mesh)

        logger.info('Import skinCluster weights: {} from {}'.format(short_name, data_path))

        return True

    def _get_influences(self, folder_path):
        """
        Internal function that returns a dictionary containing influences data from influence files
        contained in the given directory
        :param folder_path: str, path that contains influence file
        :return: dict, influence data
        """

        influence_dict = dict()

        files = fileio.get_files(folder_path)
        dependencies = self.get_dependencies(folder_path) or dict()

        info_file = dependencies.get('info_file', None)
        if not info_file or not os.path.isfile(info_file):
            if not files:
                return influence_dict
            info_file = path_utils.join_path(folder_path, 'influence.info')
            if not path_utils.is_file(info_file):
                return influence_dict

        info_lines = fileio.get_file_lines(info_file)
        for line in info_lines:
            if not line:
                continue
            line_dict = eval(line)
            influence_dict.update(line_dict)

        weight_files = python.force_list(dependencies.get('weight', list()))
        if not weight_files:
            for influence in files:
                if not influence.endswith('.weights') or influence == 'influence.info':
                    continue
                weight_files.append(path_utils.join_path(folder_path, influence))

        for weight_file in weight_files:
            read_thread = ReadWeightFileThread()
            try:
                influence_dict = read_thread.run(influence_dict, weight_file)
            except Exception as exc:
                logger.error(
                    'Errors with influence "{}" while reading weight file: "{}" | {}'.format(
                        weight_file, info_file, exc))

        return influence_dict


class LoadWeightFileThread(threading.Thread, object):
    def __init__(self):
        super(LoadWeightFileThread, self).__init__()

    def run(self, influence_index, skin, weights, file_path):
        influence_name = dcc.client().get_skin_influence_at_index(influence_index, skin)
        if not influence_name or not dcc.client().node_exists(influence_name):
            return None, None
        weight_path = fileio.create_file('{}.weights'.format(influence_name), file_path)
        if not path_utils.is_file(weight_path):
            logger.warning('"{}" is not a valid path to save skin weights into!'.format(file_path))
            return None, None

        writer = fileio.FileWriter(weight_path)
        writer.write_line(weights)

        influence_position = dcc.client().node_world_space_translation(influence_name)

        return "{'%s' : {'position' : %s}}" % (influence_name, str(influence_position)), weight_path


class ReadWeightFileThread(threading.Thread):
    def __init__(self):
        super(ReadWeightFileThread, self).__init__()

    def run(self, influence_dict, influence_file):

        influence = os.path.splitext(os.path.basename(influence_file))[0]

        lines = fileio.get_file_lines(influence_file)

        if not lines:
            influence_dict[influence]['weights'] = None
            return influence_dict

        weights = eval(lines[0])

        if influence in influence_dict:
            influence_dict[influence]['weights'] = weights

        return influence_dict


# class MayaSkinClusterWeightsPreviewWidget(data.DataPreviewWidget, object):
#     def __init__(self, item, parent=None):
#         super(MayaSkinClusterWeightsPreviewWidget, self).__init__(item=item, parent=parent)
#
#         self._export_btn.setText('Save')
#         self._export_btn.setVisible(True)
#         self._load_btn.setVisible(False)
#
#
# class MayaSkinClusterWeights(data.DataItem, object):
#
#     Extension = '.{}'.format(SkinWeightsData.get_data_extension())
#     Extensions = ['.{}'.format(SkinWeightsData.get_data_extension())]
#     MenuName = SkinWeightsData.get_data_title()
#     MenuOrder = 4
#     MenuIconName = 'skin_weights_data.png'
#     TypeIconPath = 'skin_weights_data.png'
#     DataType = SkinWeightsData.get_data_type()
#     PreviewWidgetClass = MayaSkinClusterWeightsPreviewWidget
#
#     def __init__(self, *args, **kwargs):
#         super(MayaSkinClusterWeights, self).__init__(*args, **kwargs)
#
#         self.set_data_class(SkinWeightsData)
