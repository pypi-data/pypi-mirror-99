#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""
Module that contains attribute data part implementation
"""

from __future__ import print_function, division, absolute_import

import os
import re
import logging

from tpDcc import dcc
from tpDcc.core import dcc as core_dcc
from tpDcc.libs.python import folder, fileio, path as path_utils

from tpDcc.libs.datalibrary.core import consts, datapart

LOGGER = logging.getLogger(consts.LIB_ID)


class MayaAttributesData(datapart.DataPart):

    DATA_TYPE = 'maya.attributes'
    MENU_ICON = 'attributes_data'
    MENU_NAME = 'Attributes'
    PRIORITY = 12
    EXTENSION = '.attr'

    REMOVABLE_ATTRIBUTES = ['dofMask', 'inverseScaleX', 'inverseScaleY', 'inverseScaleZ']

    _has_trait = re.compile(r'\.attr$', re.I)

    @classmethod
    def can_represent(cls, identifier, only_extension=False):
        if MayaAttributesData._has_trait.search(identifier):
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

    def icon(self):
        return 'attributes_data'

    def extension(self):
        return '.attr'

    def type(self):
        return 'maya.attributes'

    def menu_name(self):
        return 'Attributes'

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
            export_data=self.export_data,
        )

    def move(self, new_folder):

        if not new_folder or not os.path.isdir(new_folder):
            return

        identifier = self.format_identifier()

        file_directory, file_name, file_extension = path_utils.split_path(identifier)
        new_path = path_utils.join_path(new_folder, '{}{}'.format(file_name, file_extension))

        valid = folder.move_folder(self.format_identifier(), new_path, only_contents=True)
        if not valid:
            return

        return new_path

    def save(self, *args, **kwargs):

        dependencies = dict()

        filepath = self.format_identifier()
        if not filepath.endswith(MayaAttributesData.EXTENSION):
            filepath = '{}{}'.format(filepath, MayaAttributesData.EXTENSION)

        if not filepath:
            LOGGER.warning('Impossible to save Attributes file because save file path not defined!')
            return

        objects = kwargs.get('objects', None)
        scope = self._get_scope(objects)
        if not scope:
            LOGGER.warning(
                'Nothing selected to export attributes of. Please, select a mesh,'
                ' curve, NURBS surface or lattice with skin weights to export')
            return False

        LOGGER.debug('Saving {} | {}'.format(filepath, kwargs))

        if not os.path.isdir(filepath):
            attributes_folder = folder.create_folder(filepath)
            dependencies[attributes_folder] = 'attributes_folder'

        for obj in scope:
            LOGGER.info('Exporting attributes of {}'.format(obj))
            file_name = fileio.create_file('{}{}'.format(obj, self.EXTENSION), filepath)
            lines = list()
            attributes_to_export = self._get_attributes(obj)
            shapes = self._get_shapes(obj)
            if shapes:
                shape = shapes[0]
                shape_attributes = self._get_shape_attributes(shape)
                if shape_attributes:
                    attributes_to_export = list(set(attributes_to_export).union(shape_attributes))
            if not attributes_to_export:
                continue

            for attribute_to_export in attributes_to_export:
                try:
                    value = dcc.get_attribute_value(obj, attribute_to_export)
                except Exception:
                    continue
                lines.append("[ '{}', {} ]".format(attribute_to_export, value))

            write_file = fileio.FileWriter(file_name)
            write_file.write(lines)
            if file_name and os.path.isfile(file_name):
                dependencies[file_name] = 'attribute'

        LOGGER.info('Attributes data export operation completed successfully!')

        return dependencies

    def _get_scope(self, objects):
        """
        Internal function that returns the list nodes to retrieve attributes of
        :return: list(str)
        """

        selection = dcc.client().selected_nodes(full_path=False)
        selection = list(set(selection or list() + objects or list()))
        if not selection:
            LOGGER.warning('Nothing selected. Please select at least one node to export attributes of.')
            return None

        return selection

    def _get_attributes(self, node):
        found_attributes = list()

        attributes = dcc.client().list_attributes(node, scalar=True, m=True, array=True)
        for attribute in attributes:
            if not dcc.is_attribute_connected(node, attribute):
                found_attributes.append(attribute)

        for removable_attribute in self.REMOVABLE_ATTRIBUTES:
            if removable_attribute in found_attributes:
                found_attributes.remove(removable_attribute)

        return found_attributes

    def _get_shapes(self, node):
        return dcc.client().list_shapes(node, full_path=False)

    def _get_shape_attributes(self, shape):
        return self._get_attributes(shape)

    def import_data(self, **kwargs):

        filepath = self.format_identifier()
        if not filepath.endswith(MayaAttributesData.EXTENSION):
            filepath = '{}{}'.format(filepath, MayaAttributesData.EXTENSION)

        if not filepath:
            LOGGER.warning('Impossible to load attributes from file: "{}"!'.format(filepath))
            return False

        valid_import = True
        selection = dcc.client().selected_nodes(full_path=False)
        current_extension = self.EXTENSION
        full_extension = current_extension

        files_to_search = selection if selection else folder.get_files_with_extension(current_extension, filepath)
        for file_name in files_to_search:
            if not file_name.endswith(full_extension):
                file_name = '{}{}'.format(file_name, full_extension)
            full_path = os.path.join(filepath, file_name)
            if not os.path.isfile(full_path):
                continue
            node_name = file_name.split('.')[0]
            if not dcc.client().node_exists(node_name):
                LOGGER.warning(
                    'Skipping attribute import for "{}". It does not exist in current scene'.format(node_name))
                valid_import = False
                continue
            lines = fileio.get_file_lines(full_path)
            for line in lines:
                if not line:
                    continue
                line_list = eval(line)
                attribute_name = line_list[0]
                attribute_value = line_list[1]
                attribute = '{}.{}'.format(node_name, attribute_name)
                if not dcc.client().attribute_exists(node_name, attribute_name):
                    LOGGER.warning('"{}" does not exist. Impossible to set attribute value.'.format(attribute))
                    valid_import = False
                    continue
                if dcc.client().is_attribute_locked(node_name, attribute_name):
                    continue
                if dcc.client().is_attribute_connected(node_name, attribute_name):
                    continue
                if attribute_value is None:
                    continue
                try:
                    dcc.client().set_attribute_value(node_name, attribute_name, attribute_value)
                except Exception as exc:
                    LOGGER.warning('Impossible to set {} to {}: "{}" '.format(attribute, attribute_value, exc))

        dcc.client().select_node(selection)

        if valid_import:
            LOGGER.info('Imported attributes successfully!')
        else:
            LOGGER.warning('Imported attributes with warnings!')

        return valid_import

    def export_data(self, **kwargs):
        filepath = self.format_identifier()
        if not filepath.endswith(MayaAttributesData.EXTENSION):
            filepath = '{}{}'.format(filepath, MayaAttributesData.EXTENSION)

        if not filepath or not os.path.isfile(filepath):
            LOGGER.warning('Impossible to export skin weights data to: "{}"'.format(filepath))
            return

        return self.save(**kwargs)
