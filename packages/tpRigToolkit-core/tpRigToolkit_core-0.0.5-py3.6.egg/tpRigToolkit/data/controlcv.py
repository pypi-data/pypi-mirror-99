#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""
Module that contains Control CV position data implementation
"""

from __future__ import print_function, division, absolute_import

import os
import re
import logging

from tpDcc import dcc
from tpDcc.core import dcc as core_dcc
from tpDcc.libs.python import python, decorators, fileio, folder, jsonio, path as path_utils
from tpDcc.libs.datalibrary.core import consts, datapart
from tpDcc.libs.curves.core import curveslib

from tpRigToolkit.core import utils
from tpRigToolkit.data import curves
from tpRigToolkit.libs.controlrig.core import controllib

logger = logging.getLogger(consts.LIB_ID)


class _MetaControlCVsLib(type):

    def __call__(self, *args, **kwargs):
        if dcc.client().is_maya():
            from tpRigToolkit.dccs.maya.data import controlcv
            return type.__call__(controlcv.ControlCVsLibMaya, *args, **kwargs)
        else:
            return type.__call__(BaseControlCVsLib, *args, **kwargs)


class BaseControlCVsLib(object):
    def __init__(self):
        self._libraries = dict()
        self._library_curves = dict()
        self._active_library = None
        self._curves_data_path = None
        self._extension = ControlCVsData.EXTENSION

        self._load_libraries()

    # ==============================================================================================
    # ABSTRACT
    # ==============================================================================================

    @decorators.abstractmethod
    def _get_curve_transform(self, curve):
        pass

    # ==============================================================================================
    # BASE
    # ==============================================================================================

    def set_directory(self, directory_path):
        self._curves_data_path = directory_path
        self._libraries = dict()
        self._load_libraries()
        self._library_curves = dict()
        self._initialize_library_curve()

    def get_active_library(self):
        return self._active_library

    def set_active_library(self, library_name, skip_extension=False):
        if not skip_extension:
            file_name = '{}{}'.format(library_name, self._extension)
        else:
            file_name = library_name

        library_path = fileio.create_file(file_name, self._curves_data_path)
        self._active_library = library_name
        self._library_curves[library_name] = dict()
        if skip_extension:
            self.load_data_file(library_path)
        else:
            self.load_data_file()

    def get_library_names(self):
        return list(self._libraries.keys())

    def get_curve_names(self):
        if not self._active_library:
            logger.warning('Must set active library before running this function')
            return

        return self._library_curves[self._active_library].keys()

    def load_data_file(self, file_path=None):
        if not self._active_library:
            logger.warning('Must set active library before running this function.')
            return
        if not file_path:
            file_path = path_utils.join_path(
                self._curves_data_path, '{}{}'.format(self._active_library, self._extension))

        data = jsonio.read_file(file_path) or dict()
        for curve_name, curve_data in data.items():
            self._library_curves[self._active_library][curve_name] = curve_data

    def write_data_to_file(self):
        if not self._active_library:
            logger.warning('Must set active library before running this function')
            return

        file_path = path_utils.join_path(self._curves_data_path, self._active_library)
        if not file_path.endswith(self._extension):
            file_path = '{}{}'.format(file_path, self._extension)

        library_data = self._library_curves[self._active_library]
        jsonio.write_to_file(library_data, file_path)

        return file_path

    def add_curve(self, curve, library_name=None):
        if not curve:
            return
        if library_name:
            self.set_active_library(library_name)
        else:
            library_name = self._active_library
            if not self._active_library:
                logger.warning('Must set active library before running this function')
                return

        transform = self._get_curve_transform(curve)
        curve_data = curveslib.serialize_curve(transform, normalize=False)
        self._update_curve_data(transform, curve_data)
        self._library_curves[library_name][transform] = curve_data

    def remove_curve(self, curve, library_name=None):
        if not curve:
            return False

        if not library_name:
            library_name = self._active_library
            if not self._active_library:
                logger.warning('Must set active library before running this function')
                return False

        transform = self._get_curve_transform(curve)
        if library_name in self._library_curves:
            if transform in self._library_curves[library_name]:
                self._library_curves[library_name].pop(transform)
                return True

        return False

    def set_curve(self, curve, curve_in_library=None, check_curve=False):
        if not self._active_library:
            logger.warning('Must set active library before running this function')
            return

        curve_in_library = curve_in_library or curve

        curve_data = self._get_curve_data(curve_in_library, self._active_library)
        if not curve_data:
            return

        if check_curve:
            is_curve = self._is_curve_of_type(curve, curve_in_library)
            if not is_curve:
                logger.warning('curve data does not store expected curve type')
                return False

        transform = self._get_curve_transform(curve)
        controllib.replace_control_curves(transform, control_data=curve_data, auto_scale=False)

    # ==============================================================================================
    # INTERNAL
    # ==============================================================================================

    def _get_curves_data_path(self):
        current_path = curves.__path__[0]
        custom_curve_path = utils.get_custom('custom_curve_path')
        if custom_curve_path and os.path.isdir(custom_curve_path):
            curve_data = os.path.join(custom_curve_path)
            folder.create_folder(curve_data)
            logger.info('Using custom curve directory: {}'.format(custom_curve_path))
            current_path = custom_curve_path

        self._curves_data_path = current_path

        return self._curves_data_path

    def _load_libraries(self):
        curves_data_path = self._curves_data_path or self._get_curves_data_path()
        files = os.listdir(curves_data_path)
        for filename in files:
            if filename.endswith(self._extension):
                split_file = filename.split('.')
                self._library_curves[split_file[0]] = filename

    def _initialize_library_curve(self):
        names = self.get_library_names()
        for name in names:
            self._library_curves[name] = dict()

    def _update_curve_data(self, transform, curve_data):
        if dcc.attribute_exists(transform, 'curveType') or dcc.attribute_exists(transform, 'type'):
            value = dcc.get_attribute_value(transform, 'curveType')
            if value:
                curve_data['type'] = value
        if dcc.attribute_exists(transform, 'type'):
            value = dcc.get_attribute_value(transform, 'type')
            if value:
                curve_data['type'] = value

    def _get_curve_data(self, curve_name, curve_library):
        curve_dict = self._library_curves[curve_library]
        if curve_name not in curve_dict:
            # logger.warning('{} is not in the curve library {}'.format(curve_name, curve_library))
            return dict()

        return curve_dict[curve_name]

    def _get_curve_type(self, curve):
        curve_type_value = None
        if dcc.attribute_exists(curve, 'curveType'):
            curve_type_value = dcc.get_attribute_value(curve, 'curveType')
        elif dcc.attribute_exists(curve, 'type'):
            curve_type_value = dcc.get_attribute_value(curve, 'type')

        return curve_type_value

    def _is_curve_of_type(self, curve, type_curve):
        curve_data = self._get_curve_data(type_curve, self._active_library)
        if not curve_data:
            return False
        original_curve_type = curve_data.get('curveType', curve_data.get('type', ''))
        if not original_curve_type:
            return True
        curve_type_value = self._get_curve_type(curve)
        if curve_type_value and curve_type_value != original_curve_type:
            return False

        return True


class ControlCVsData(datapart.DataPart):
    DATA_TYPE = 'dcc.controlcvs'
    MENU_ICON = 'circle'
    MENU_NAME = 'Control CVs'
    PRIORITY = 13
    EXTENSION = '.cvs'

    _has_trait = re.compile(r'\.cvs$', re.I)

    @classmethod
    def can_represent(cls, identifier, only_extension=False):
        if ControlCVsData._has_trait.search(identifier):
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
        return 'circle'

    def extension(self):
        return '.cvs'

    def type(self):
        return 'dcc.controlcvs'

    def menu_name(self):
        return 'Control CVs'

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
            export_data=self.export_data,
            get_curves=self.get_curves,
            remove_curve=self.remove_curve
        )

    def save(self, *args, **kwargs):

        filepath = self.format_identifier()
        if not filepath.endswith(ControlCVsData.EXTENSION):
            filepath = '{}{}'.format(filepath, ControlCVsData.EXTENSION)

        if not filepath:
            logger.warning('Impossible to save Control CVs file because save file path not defined!')
            return

        logger.debug('Saving {} | {}'.format(filepath, kwargs))

        objects = kwargs.get('objects', None)
        if not objects:
            objects = dcc.client().selected_nodes(full_path=True)
        if not objects:
            logger.warning(
                'Nothing selected to export Control CVs of. Please, select a curve to export')
            return False

        # We make sure that we store the short name of the controls
        objects = [dcc.client().node_short_name(obj) for obj in objects]

        controls = objects or controllib.get_controls()
        valid_controls = list()
        for control in controls:
            if not controllib.is_control(control):
                continue
            valid_controls.append(control)
        if not valid_controls:
            logger.warning('No valid controls found to export.')
            return False

        library = self._initialize_library(filepath)
        if not controls:
            logger.warning('No controls found to export.')
            return False

        for control in controls:
            library.add_curve(control)

        library.write_data_to_file()

        logger.info('Saved {} data'.format(self.name()))

        return True

    def import_data(self, **kwargs):

        filepath = self.format_identifier()
        if not filepath.endswith(ControlCVsData.EXTENSION):
            filepath = '{}{}'.format(filepath, ControlCVsData.EXTENSION)

        if not filepath:
            logger.warning('Impossible to load Control CVs from file: "{}"!'.format(filepath))
            return False

        library = self._initialize_library(filepath)

        objects = kwargs.get('objects', None)
        if not objects:
            objects = dcc.client().selected_nodes(full_path=True) or list()

        # We make sure that we store the short name of the controls
        objects = [dcc.node_short_name(obj) for obj in objects]

        updated_controls = list()
        controls = objects or controllib.get_controls()
        for control in controls:
            shapes = dcc.client().get_curve_shapes(control)
            if not shapes:
                continue
            library.set_curve(control, check_curve=True)
            updated_controls.append(control)

        # We force the update of all the curves that are stored in the library and are in the scene
        for curve_data in list(library._library_curves.values()):
            for curve_name in list(curve_data.keys()):
                if curve_name and dcc.node_exists(curve_name) and curve_name not in updated_controls:
                    library.set_curve(curve_name, check_curve=True)
                    updated_controls.append(curve_name)

        logger.info('Imported {} data'.format(self.name()))

        return True

    def export_data(self, **kwargs):
        filepath = self.format_identifier()
        if not filepath.endswith(ControlCVsData.EXTENSION):
            filepath = '{}{}'.format(filepath, ControlCVsData.EXTENSION)

        if not filepath or not os.path.isfile(filepath):
            logger.warning('Impossible to export Control CVs data to: "{}"'.format(filepath))
            return

        objects = kwargs.get('objects', list())
        selected_objects = dcc.client().selected_nodes(full_path=True)
        objects = list(set(objects + selected_objects))
        kwargs['objects'] = objects

        return self.save(**kwargs)

    def get_curves(self, file_name=None):
        library = self._initialize_library(file_name)
        library.set_active_library(self.name)
        curves = library.get_curve_names()

        return curves

    def remove_curve(self, curve_name, file_name=None):
        curves_list = python.force_list(curve_name)
        library = self._initialize_library(file_name)
        library.set_active_library(self.name)
        for curve_found in curves_list:
            library.remove_curve(curve_found)
        library.write_data_to_file()

        return True

    def _initialize_library(self, file_name=None):
        if file_name:
            directory = path_utils.get_dirname(file_name)
            name = path_utils.get_basename(file_name)
        else:
            path = self.format_identifier()
            directory = path_utils.get_dirname(path)
            name = self.name()

        library = ControlCVsLib()
        library.set_directory(directory)

        if file_name:
            library.set_active_library(name, skip_extension=True)
        else:
            library.set_active_library(name)

        return library


@decorators.add_metaclass(_MetaControlCVsLib)
class ControlCVsLib(object):
    pass


# class ControlCVOptionsWidget(loadwidget.OptionsFileWidget, object):
#     def __init__(self, parent=None):
#         super(ControlCVOptionsWidget, self).__init__(parent=parent)
#
#     def ui(self):
#         super(ControlCVOptionsWidget, self).ui()
#
#         self._search_line = search.SearchFindWidget(parent=self)
#         self._search_line.set_placeholder_text('Filter Names')
#         self._curves_list = QListWidget()
#         self._curves_list.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
#         self._curves_list.setSelectionMode(self._curves_list.ExtendedSelection)
#         self._curves_list.setSortingEnabled(True)
#         self._delete_curve_button = buttons.BaseButton('Delete Curve CVs data', parent=self)
#
#         self.main_layout.addWidget(self._search_line)
#         self.main_layout.addWidget(self._curves_list)
#         self.main_layout.addWidget(dividers.Divider())
#         self.main_layout.addWidget(self._delete_curve_button)
#
#     def setup_signals(self):
#         self._search_line.textChanged.connect(self._on_filter_names)
#         self._delete_curve_button.clicked.connect(self._on_remove_curves)
#
#     def refresh(self):
#         self._curves_list.clear()
#
#         if not self._data_object:
#             return
#
#         curves = self._data_object.get_curves()
#         if not curves:
#             return
#
#         for curve_name in curves:
#             item = QListWidgetItem(curve_name)
#             self._curves_list.addItem(item)
#
#     def _on_filter_names(self):
#         self._unhide_names()
#         for i in range(self._curves_list.count()):
#             item = self._curves_list.item(i)
#             text = str(item.text())
#             filter_text = self._search_line.text()
#             if text.find(filter_text) == -1:
#                 item.setHidden(True)
#
#     def _on_remove_curves(self):
#         items = self._curves_list.selectedItems()
#         if not items:
#             return
#
#         for item in items:
#             curve_name = str(item.text())
#             removed = self._data_object.remove_curve(curve_name)
#             if removed:
#                 index = self._curves_list.indexFromItem(item)
#                 remove_item = self._curves_list.takeItem(index.row())
#                 del remove_item
#
#     def _unhide_names(self):
#         for i in range(self._curves_list.count()):
#             item = self._curves_list.item(i)
#             item.setHidden(False)
