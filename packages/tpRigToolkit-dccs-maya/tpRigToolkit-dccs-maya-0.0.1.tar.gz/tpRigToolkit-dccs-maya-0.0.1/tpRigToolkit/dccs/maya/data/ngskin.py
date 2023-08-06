#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""
Module that contains data NGSkin Cluster weights
"""

from __future__ import print_function, division, absolute_import

import os
import re
import json
import logging
from collections import OrderedDict

from tpDcc import dcc
from tpDcc.core import dcc as core_dcc
from tpDcc.libs.python import fileio, folder, path as path_utils
from tpDcc.libs.datalibrary.core import consts, datapart

if dcc.is_maya():
    import maya.cmds
    from tpDcc.dccs.maya.core import skin as skin_utils, shape as shape_utils, geometry as geo_utils
    from tpDcc.dccs.maya.core import deformer as deform_utils


logger = logging.getLogger(consts.LIB_ID)


class NgSkinWeightsData(datapart.DataPart):

    DATA_TYPE = 'maya.ngskincluster'
    MENU_ICON = 'ngskin'
    MENU_NAME = 'NGSkin Cluster Weights'
    PRIORITY = 15
    EXTENSION = '.ngskin'

    _has_trait = re.compile(r'\.ngskin$', re.I)

    @classmethod
    def can_represent(cls, identifier, only_extension=False):
        if NgSkinWeightsData._has_trait.search(identifier):
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
        return '.ngskin'

    def icon(self):
        return 'ngskin'

    def type(self):
        return 'maya.ngskincluster'

    def menu_name(self):
        return 'NGSkin Cluster Weights'

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
            save=self.save,
            import_data=self.import_data,
            export_data=self.export_data
        )

    def save(self, *args, **kwargs):
        """
        Saves NG Skin weights file
        """

        dependencies = dict()

        filepath = self.format_identifier()
        if not filepath:
            logger.warning('Impossible to save NGSkin Cluster Weights file because save file path not defined!')
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

        try:
            if not dcc.is_plugin_loaded('ngSkinTools2'):
                dcc.load_plugin('ngSkinTools2')
            import ngSkinTools2
            from ngSkinTools2 import api as ngst_api
        except ImportError:
            logger.warning('NgSkinTools 2.0 is not installed. Impossible to export ngSkin data')
            return False

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

            for influence in skin_weights:
                if influence is None or influence == 'None':
                    continue
                weight_list = skin_weights[influence]
                if not weight_list:
                    continue

                influence_name = skin_utils.get_skin_influence_at_index(influence, skin_node)
                if not influence_name or not dcc.node_exists(influence_name):
                    continue

                influence_position = dcc.node_world_space_translation(influence_name)
                influence_line = "{'%s' : {'position' : %s}}" % (influence_name, str(influence_position))
                info_lines.append(influence_line)

            writer = fileio.FileWriter(info_file)
            writer.write(info_lines)

            settings_file = fileio.create_file('settings.info', geo_path)
            setting_lines = list()
            if shape_utils.has_shape_of_type(obj, 'mesh'):
                self._export_mesh_obj(obj, geo_path)

            setting_lines.append("['skinNodeName', '{}']".format(dcc.node_short_name(skin_node)))
            if dcc.attribute_exists(skin_node, 'blendWeights'):
                blend_weights = skin_utils.get_skin_blend_weights(skin_node)
                setting_lines.append("['blendWeights', {}]".format(blend_weights))
            if dcc.attribute_exists(skin_node, 'skinningMethod'):
                skin_method = dcc.get_attribute_value(skin_node, 'skinningMethod')
                setting_lines.append("['skinningMethod', {}]".format(skin_method))

            write_settings = fileio.FileWriter(settings_file)
            write_settings.write(setting_lines)

            ng_skin_file_name = os.path.join(geo_path, 'ngdata.json')
            ngst_api.export_json(obj, file=ng_skin_file_name)

            logger.info('Skin weights exported successfully: {} > {} --> "{}"'.format(obj, skin_node, geo_path))

        data_to_save = OrderedDict()
        for obj, obj_filename in obj_dirs.items():
            data_to_save[obj] = {'enabled': True, 'folder': obj_filename}
        with open(filepath, 'w') as fh:
            json.dump(data_to_save, fh)

        logger.info('Skin weights export operation completed successfully!')

        return True

    def _import_skin_weights(self, data_path, mesh):
        if not dcc.node_exists(mesh) or not os.path.isdir(data_path):
            return False

        try:
            if not dcc.is_plugin_loaded('ngSkinTools2'):
                dcc.load_plugin('ngSkinTools2')
            import ngSkinTools2
            from ngSkinTools2 import api as ngst_api
        except ImportError:
            logger.warning('NgSkinTools 2.0 is not installed. Impossible to import ngSkin data')
            return False

        ng_skin_data_path = path_utils.join_path(data_path, 'ngdata.json')
        if not path_utils.is_file(ng_skin_data_path):
            logger.warning(
                'No Ng Skin Data file found: "{}", aborting import skin weights operation ...'.format(
                    ng_skin_data_path))
            return False

        is_valid_mesh = False
        shape_types = ['mesh', 'nurbsSurface', 'nurbsCurve', 'lattice']
        for shape_type in shape_types:
            if shape_utils.has_shape_of_type(mesh, shape_type):
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

        influences = influence_dict.keys()
        if not influences:
            logger.warning('No influences found for: "{}"'.format(mesh))
            return False
        influences.sort()
        logger.debug('Influences found for {}: {}'.format(mesh, influences))

        short_name = dcc.node_short_name(mesh)
        transfer_mesh = None

        if shape_utils.has_shape_of_type(mesh, 'mesh'):
            orig_mesh = self._import_mesh_obj(data_path)
            if orig_mesh:
                mesh_match = geo_utils.is_mesh_compatible(orig_mesh, mesh)
                if not mesh_match:
                    transfer_mesh = mesh
                    mesh = orig_mesh
                else:
                    dcc.delete_node(orig_mesh)

        # Check if there are duplicated influences and also for the creation of influences that does not currently
        # in the scene
        add_joints = list()
        remove_entries = list()
        for influence in influences:
            joints = dcc.list_nodes(influence, full_path=True)
            if type(joints) == list and len(joints) > 1:
                add_joints.append(joints[0])
                conflicting_count = len(joints)
                logger.warning(
                    'Found {} joints with name {}. Using only the first one: {}'.format(
                        conflicting_count, influence, joints[0]))
                remove_entries.append(influence)
                influence = joints[0]
            if not dcc.node_exists(influence):
                dcc.clear_selection()
                dcc.create_joint(name=influence, position=influence_dict[influence]['position'])
        for entry in remove_entries:
            influences.remove(entry)
        influences += add_joints

        settings_data = dict()
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
                settings_data[attr_name] = value

        # Create skin cluster and removes if it already exists
        skin_cluster = deform_utils.find_deformer_by_type(mesh, 'skinCluster')
        if skin_cluster:
            dcc.delete_node(skin_cluster)

        skin_node_name = settings_data.pop('skinNodeName', 'skin_{}'.format(short_name))
        skin_cluster = maya.cmds.skinCluster(
            influences, mesh, tsb=True, n=dcc.find_unique_name(skin_node_name))[0]
        dcc.set_attribute_value(skin_cluster, 'normalizeWeights', 0)
        skin_utils.set_skin_weights_to_zero(skin_cluster)

        # TODO: This Influence mapping configuration should be generated during export and imported here as JSON file
        # Import ng skin data
        config = ngst_api.InfluenceMappingConfig()
        config.use_distance_matching = True
        config.use_label_matching = True
        config.use_name_matching = True

        ngst_api.import_json(mesh, file=ng_skin_data_path, influences_mapping_config=config)

        maya.cmds.skinCluster(skin_cluster, edit=True, normalizeWeights=1)
        maya.cmds.skinCluster(skin_cluster, edit=True, forceNormalizeWeights=True)

        for attr_name, value in settings_data.items():
            if attr_name == 'blendWeights':
                skin_utils.set_skin_blend_weights(skin_cluster, value)
            else:
                if dcc.attribute_exists(skin_cluster, attr_name):
                    dcc.set_attribute_value(skin_cluster, attr_name, value)

        if transfer_mesh:
            logger.info('Import sking weights: mesh topology does not match. Trying to transfer topology ...')
            skin_utils.skin_mesh_from_mesh(mesh, transfer_mesh)
            dcc.delete_node(mesh)

        logger.info('Import skinCluster weights: {} from {}'.format(short_name, data_path))

        return True

    def _get_influences(self, folder_path):
        influence_dict = dict()

        info_file = path_utils.join_path(folder_path, 'influence.info')
        if not path_utils.is_file(info_file):
            return influence_dict

        info_lines = fileio.get_file_lines(info_file)
        for line in info_lines:
            if not line:
                continue
            line_dict = eval(line)
            influence_dict.update(line_dict)

        return influence_dict

    def export_data(self, **kwargs):
        filepath = self.format_identifier()

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
        if not filepath:
            logger.warning('Impossible to load Ng Skin Weights from file: "{}"!'.format(filepath))
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
                    file_folder, '.{}{}'.format(self.name(), NgSkinWeightsData.EXTENSION))
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

        logger.info('Imported "{}" skin data'.format(self.name()))

        return True

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
