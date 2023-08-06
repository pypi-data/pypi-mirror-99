#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""
Module that contains HumanIK related data
"""

from __future__ import print_function, division, absolute_import

import os
import re
import logging
from xml.dom import minidom
from xml.etree import ElementTree

from tpDcc import dcc
from tpDcc.core import dcc as core_dcc
from tpDcc.libs.datalibrary.core import consts, datapart

logger = logging.getLogger(consts.LIB_ID)


class HIKSkeletonDefinition(datapart.DataPart):

    DATA_TYPE = 'maya.hikskeletondefinition'
    MENU_ICON = 'skeleton'
    MENU_NAME = 'HIK Skeleton Definition'
    PRIORITY = 15
    EXTENSION = '.hikskldef'

    _has_trait = re.compile(r'\.hikskldef', re.I)

    @classmethod
    def can_represent(cls, identifier, only_extension=False):
        if HIKSkeletonDefinition._has_trait.search(identifier):
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
        return '.hikskldef'

    def icon(self):
        return 'skeleton'

    def type(self):
        return 'maya.hikskeletondefinition'

    def menu_name(self):
        return 'HIK Skeleton Definition'

    def save_schema(self):
        """
        Returns the schema used for saving the item
        :return: dict
        """

        return [
            {
                'name': 'character',
                'type': 'enum',
                'default': '',
                'items': [''] + dcc.client().get_scene_hik_characters(),
                'persistent': True
            }
        ]

    def functionality(self):
        return dict(
            save=self.save,
            import_data=self.import_data,
            export_data=self.export_data
        )

    def save(self, *args, **kwargs):
        from tpDcc.dccs.maya.core import humanik

        filepath = self.format_identifier()
        if not filepath:
            logger.warning('Impossible to save HIK Character Definition because save file path not defined!')
            return

        hik_character = kwargs.get('character', None)
        if not hik_character:
            logger.warning('No HumanIK Character defined to export skeleton definition of!')
            return False

        if hik_character not in humanik.get_scene_characters():
            logger.warning('HumanIk Character "{}" is not a valid one!'.format(hik_character))
            return False

        logger.debug('Saving {} | {}'.format(filepath, kwargs))

        skeleton_mapping = dict()
        skeleton_def = humanik.get_skeleton_definition(hik_character)
        for hik_name in list(humanik.HIK_BONES.keys()):
            skeleton_mapping[hik_name] = skeleton_def[hik_name]['bone'] if hik_name in skeleton_def else ''

        root = ElementTree.Element('config_root')
        match = ElementTree.SubElement(root, 'match_list')
        for hik_name, bone_name in skeleton_mapping.items():
            hik_item = ElementTree.SubElement(match, 'item')
            hik_item.set('key', hik_name)
            hik_item.set('value', bone_name)

        skeleton_definition_data = ElementTree.tostring(root)
        with open(filepath, 'w') as fh:
            fh.write(skeleton_definition_data)

        logger.info('HumanIK Skeleton Definition export operation completed successfully!')

        return True

    def import_data(self, **kwargs):
        from tpDcc.dccs.maya.core import humanik

        filepath = self.format_identifier()
        if not filepath:
            logger.warning('Impossible to load HIK Character Definition from file: "{}"!'.format(filepath))
            return False

        hik_character = kwargs.get('character', None)
        if not hik_character:
            hik_characters = humanik.get_scene_characters()
            hik_character = hik_characters[0] if hik_characters else None
        if not hik_character:
            logger.warning('No HumanIK Character defined to export skeleton definition of!')
            return False

        skeleton_definition = dict()
        data = minidom.parse(filepath)
        items = data.getElementsByTagName('item')
        for item in items:
            skeleton_definition[item.attributes['key'].value] = {'bone': item.attributes['value'].value}

        humanik.set_skeleton_definition(hik_character, skeleton_definition)

    def export_data(self, **kwargs):
        from tpDcc.dccs.maya.core import humanik

        filepath = self.format_identifier()

        if not filepath or not os.path.isfile(filepath):
            logger.warning('Impossible to export HIK Character Definition data to: "{}"'.format(filepath))
            return

        hik_character = kwargs.get('character', None)
        if not hik_character:
            hik_characters = humanik.get_scene_characters()
            hik_character = hik_characters[0] if hik_characters else None
        if not hik_character:
            logger.warning('No HumanIK Character defined to export skeleton definition of!')
            return False

        return self.save(**kwargs)


class HIKCustomRigDefinition(datapart.DataPart):

    DATA_TYPE = 'maya.hikcustomrigdefinition'
    MENU_ICON = 'rig'
    MENU_NAME = 'HIK Custom Rig Definition'
    PRIORITY = 15
    EXTENSION = '.hikcsttrig'

    _has_trait = re.compile(r'\.hikcsttrig', re.I)

    @classmethod
    def can_represent(cls, identifier, only_extension=False):
        if HIKCustomRigDefinition._has_trait.search(identifier):
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
        return '.hikcsttrig'

    def icon(self):
        return 'rig'

    def type(self):
        return 'maya.hikcustomrigdefinition'

    def menu_name(self):
        return 'HIK Custom Rig Definition'

    def save_schema(self):
        """
        Returns the schema used for saving the item
        :return: dict
        """

        return [
            {
                'name': 'character',
                'type': 'enum',
                'default': '',
                'items': [''] + dcc.client().get_scene_hik_characters(),
                'persistent': True
            }
        ]

    def functionality(self):
        return dict(
            save=self.save,
            import_data=self.import_data,
            export_data=self.export_data
        )

    def save(self, *args, **kwargs):
        from tpDcc.dccs.maya.core import humanik

        filepath = self.format_identifier()
        if not filepath:
            logger.warning('Impossible to save HIK Custom Rig file because save file path not defined!')
            return

        hik_character = kwargs.get('character', None)
        if not hik_character:
            logger.warning('No HumanIK Character defined to export skeleton definition of!')
            return False

        if hik_character not in humanik.get_scene_characters():
            logger.warning('HumanIk Character "{}" is not a valid one!'.format(hik_character))
            return False

        logger.debug('Saving {} | {}'.format(filepath, kwargs))

        humanik.export_custom_rig_mapping(hik_character, filepath)

        logger.info('HumanIK Custom Rig export operation completed successfully!')

        return True

    def import_data(self, **kwargs):
        from tpDcc.dccs.maya.core import humanik

        filepath = self.format_identifier()
        if not filepath:
            logger.warning('Impossible to load HIK Custom Rig from file: "{}"!'.format(filepath))
            return False

        hik_character = kwargs.get('character', None)
        if not hik_character:
            hik_characters = humanik.get_scene_characters()
            hik_character = hik_characters[0] if hik_characters else None
        if not hik_character:
            logger.warning('No HumanIK Character defined to export skeleton definition of!')
            return False

        humanik.import_custom_rig_mapping(hik_character, filepath)

    def export_data(self, **kwargs):
        from tpDcc.dccs.maya.core import humanik

        filepath = self.format_identifier()

        if not filepath or not os.path.isfile(filepath):
            logger.warning('Impossible to export HIK Custom Rig data to: "{}"'.format(filepath))
            return

        hik_character = kwargs.get('character', None)
        if not hik_character:
            hik_characters = humanik.get_scene_characters()
            hik_character = hik_characters[0] if hik_characters else None
        if not hik_character:
            logger.warning('No HumanIK Character defined to export skeleton definition of!')
            return False

        return self.save(**kwargs)
