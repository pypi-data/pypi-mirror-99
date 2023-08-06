#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""
Module that contains project widgets implementation for tpRigToolkit
"""

from __future__ import print_function, division, absolute_import

import os
import logging

from Qt.QtCore import Qt, Signal, QSize
from Qt.QtWidgets import QSizePolicy, QWidget, QLabel, QListWidget, QListWidgetItem, QMenu
from Qt.QtGui import QPixmap

from tpDcc.managers import resources, tools
from tpDcc.libs.python import python, path as path_utils
from tpDcc.libs.qt.core import base, qtutils
from tpDcc.libs.qt.widgets import layouts, dividers, buttons, combobox, directory, tabs

from tpRigToolkit.widgets.options import rigoptionsviewer

LOGGER = logging.getLogger('tpRigToolkit-core')


class ProjectSettingsWidget(base.BaseWidget, object):
    exitSettings = Signal()

    def __init__(self, project=None, parent=None):
        self._project = None
        super(ProjectSettingsWidget, self).__init__(parent=parent)

        self._fill_version_types_combo()

        if project:
            self.set_project(project)

    def ui(self):
        super(ProjectSettingsWidget, self).ui()

        image_layout = layouts.HorizontalLayout(spacing=2, margins=(2, 2, 2, 2))
        image_layout.setContentsMargins(2, 2, 2, 2)
        image_layout.setSpacing(2)
        self.main_layout.addLayout(image_layout)
        self._project_image = QLabel()
        self._project_image.setAlignment(Qt.AlignCenter)
        image_layout.addStretch()
        image_layout.addWidget(self._project_image)
        image_layout.addStretch()

        self._settings_tab = tabs.BaseTabWidget(parent=self)
        self.main_layout.addWidget(self._settings_tab)

        self._naming_widget = NamingWidget(project=self._project)
        self._project_options_widget = rigoptionsviewer.RigOptionsViewer(option_object=self._project, parent=self)
        self._external_code_widget = ExternalCodeDirectoryWidget(parent=self)
        version_control_widget = QWidget(parent=self)
        version_control_layout = layouts.VerticalLayout(spacing=0, margins=(2, 2, 2, 2))
        version_control_widget.setLayout(version_control_layout)
        self._version_type_combo = combobox.BaseComboBox(parent=self)
        version_control_layout.addWidget(self._version_type_combo)
        version_control_layout.addStretch()

        self._settings_tab.addTab(self._project_options_widget, 'Settings')
        self._settings_tab.addTab(self._naming_widget, 'Nomenclature')
        self._settings_tab.addTab(version_control_widget, 'Version Control')
        self._settings_tab.addTab(self._external_code_widget, 'External Code')

        bottom_layout = layouts.VerticalLayout(spacing=2, margins=(2, 2, 2, 2))
        bottom_layout.setAlignment(Qt.AlignBottom)
        self.main_layout.addLayout(bottom_layout)
        bottom_layout.addLayout(dividers.DividerLayout())

        buttons_layout = layouts.HorizontalLayout(spacing=2, margins=(2, 2, 2, 2))
        bottom_layout.addLayout(buttons_layout)

        ok_icon = resources.icon('ok')
        self._ok_btn = buttons.BaseButton(parent=self)
        self._ok_btn.setIcon(ok_icon)
        buttons_layout.addWidget(self._ok_btn)

    def setup_signals(self):
        self._version_type_combo.currentIndexChanged.connect(self._on_version_control_type_changed)
        self._ok_btn.clicked.connect(self._on_exit)

    def get_project(self):
        """
        Returns current RigBuilder project used by this widget
        :return: Project
        """

        return self._project

    def set_project(self, project):
        """
        Sets current project used by this widget
        :param project: Project
        """

        self._project = project

        self._project_options_widget.set_option_object(self._project)
        if self._project:
            self._project_image.setPixmap(
                QPixmap(self._project.get_project_image()).scaled(QSize(150, 150), Qt.KeepAspectRatio))
        self._naming_widget.set_project(self._project)
        self._external_code_widget.set_project(self._project)
        if self._project and self._project.settings.has_setting('version_control'):
            try:
                version_control_index = int(self._project.settings.has_setting('version_control'))
            except Exception:
                version_control_index = 0
            self._version_type_combo.setCurrentIndex(version_control_index)

    def update_options(self, do_reload=False):
        """
        Update options of the current project
        """

        if not self._project:
            return

        if do_reload:
            self._project.reload_options()

        self._project_options_widget.update_options()

    def _fill_version_types_combo(self):
        """
        Internal callback function that fills with the different types of supported version controls
        """

        self._version_type_combo.clear()
        for version_type in ['none', 'git']:
            self._version_type_combo.addItem(resources.icon(version_type), version_type)

    def _on_version_control_type_changed(self, index):
        """
        Internal callback function that is called when version control type is updated
        :param index: int
        :return:
        """

        if not self._project:
            return

        self._project.settings.set('version_control', int(index))

    def _on_exit(self):
        """
        Internal callback function that is called when the user exists settings widget
        """

        self.exitSettings.emit()


class NamingWidget(base.BaseWidget, object):
    def __init__(self, project=None, parent=None):

        self._project = project

        super(NamingWidget, self).__init__(parent=parent)

        self.update_rules()

    def get_main_layout(self):
        main_layout = layouts.VerticalLayout(spacing=2, margins=(0, 0, 0, 0))

        return main_layout

    def ui(self):
        super(NamingWidget, self).ui()

        naming_layout = layouts.HorizontalLayout(spacing=2, margins=(0, 0, 0, 0))
        edit_icon = resources.icon('edit')
        name_lbl = QLabel('Naming Rule: ')
        self._name_rules = combobox.BaseComboBox(parent=self)
        self._name_rules.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self._edit_btn = buttons.BaseButton(parent=self)
        self._edit_btn.setIcon(edit_icon)
        naming_layout.addWidget(name_lbl)
        naming_layout.addWidget(self._name_rules)
        naming_layout.addWidget(self._edit_btn)

        self.main_layout.addLayout(naming_layout)
        self.main_layout.addStretch()

    def setup_signals(self):
        self._name_rules.currentIndexChanged.connect(self._on_update_rule)
        self._edit_btn.clicked.connect(self._on_open_naming_manager)

    def set_project(self, project):
        self._project = project
        self.update_rules()

    def update_rules(self):

        try:
            self._name_rules.blockSignals(True)

            self._name_rules.clear()
            if not self._project:
                return
            naming_lib = self._project.naming_lib
            if not naming_lib:
                return
            naming_lib.load_session()
            rules = naming_lib.rules
            for rule in rules:
                self._name_rules.addItem(rule.name, userData=rule)
            rule_name = self._set_rule()
            self._name_rules.setCurrentText(rule_name)
        except Exception as exc:
            LOGGER.warning('Error while updating rules: {}'.format(exc))
        finally:
            self._name_rules.blockSignals(False)

    def _set_rule(self, rule=None):
        if not self._project:
            return
        naming_lib = self._project.naming_lib
        if not naming_lib:
            return

        if rule:
            rule_name = rule.name
            if self._project.settings.has_setting('naming_rule'):
                current_rule = self._project.settings.get('naming_rule')
                if current_rule == rule_name:
                    return
                self._project.settings.set('naming_rule', rule_name)
        else:
            if not self._project.settings.has_setting('naming_rule'):
                self._project.settings.set('naming_rule', self._name_rules.currentText())

        if not self._project.settings.has_setting('naming_rule'):
            return
        rule_name = self._project.settings.get('naming_rule')
        if not naming_lib.has_rule(rule_name):
            return
        naming_lib.set_active_rule(rule_name)

        return rule_name

    def _on_update_rule(self, index):
        rule = self._name_rules.itemData(index)
        self._set_rule(rule=rule)

    def _on_open_naming_manager(self):
        # naming_manager_tool = tools.ToolsManager().launch_tool_by_id(
        #     'tpRigToolkit-tools-namemanager', project=self._project)
        naming_manager_tool = tools.ToolsManager().launch_tool_by_id(
            'tpDcc-tools-nameit', naming_lib=self._project.naming_lib)
        attacher = naming_manager_tool.attacher
        attacher.closed.connect(self.update_rules)


class ExternalCodeList(QListWidget):

    directoriesChanged = Signal(object)

    def __init__(self, parent=None):
        super(ExternalCodeList, self).__init__(parent)

        self.setAlternatingRowColors(True)
        self.setSelectionMode(self.NoSelection)
        self.setContextMenuPolicy(Qt.CustomContextMenu)
        self.customContextMenuRequested.connect(self._on_item_menu)

        self._create_context_menu()

    def get_directories(self):
        count = self.count()
        found = list()
        if not count:
            return found
        for i in range(count):
            item = self.item(i)
            if not item:
                continue
            found.append(str(item.text()))

        return found

    def refresh(self, directories):
        directories = python.force_list(directories)
        self.clear()
        for diretory_found in directories:
            name = diretory_found
            if not path_utils.is_dir(diretory_found):
                name = 'Directory Not Valid! {}'.format(diretory_found)
            item = QListWidgetItem()
            item.setText(name)
            item.setSizeHint(QSize(20, 25))
            self.addItem(item)

    def _create_context_menu(self):
        self._context_menu = QMenu()
        remove_action = self._context_menu.addAction('Remove')
        remove_action.setIcon(resources.icon('trash'))
        remove_action.triggered.connect(self._on_remove_action)

    def _on_item_menu(self, pos):
        item = self.itemAt(pos)
        if not item:
            return
        self._context_menu.exec_(self.viewport().mapToGlobal(pos))

    def _on_remove_action(self):
        index = self.currentIndex()
        self.takeItem(index.row())
        self.directoriesChanged.emit(self.get_directories())


class ExternalCodeDirectoryWidget(directory.GetDirectoryWidget):
    def __init__(self, project=None, parent=None):
        self._project = None
        super(ExternalCodeDirectoryWidget, self).__init__(parent)

        self.set_project(project)

    def get_main_layout(self):
        return layouts.VerticalLayout(spacing=2, margins=(2, 2, 2, 2))

    def ui(self):
        super(ExternalCodeDirectoryWidget, self).ui()

        self._directory_widget.setVisible(False)
        self._directory_widget.setEnabled(False)

        self._list = ExternalCodeList(parent=self)

        file_layout = layouts.HorizontalLayout()
        self._directory_browse_button = buttons.BaseButton('Add External Code Path', parent=self)
        self._directory_browse_button.setIcon(resources.icon('folder'))
        file_layout.addWidget(self._directory_browse_button)

        self.main_layout.addWidget(self._list)
        self.main_layout.addLayout(file_layout)

    def setup_signals(self):
        super(ExternalCodeDirectoryWidget, self).setup_signals()

        self._list.directoriesChanged.connect(self._on_send_directories)
        self._directory_browse_button.clicked.connect(self._on_browse)

    def set_directory(self, directory):
        directory = python.force_list(directory)
        self._last_directory = self._directory
        self._directory = directory
        self._list.refresh(directory)

    def set_project(self, project):
        self._project = project
        if not self._project:
            self._list.clear()
            return
        external_code_paths = self._project.get_external_paths(relative=False) or list()
        self._list.refresh(external_code_paths)

    def get_external_code_paths(self):
        return self._list.get_directories()

    def set_external_code_paths(self, paths_list):
        self._list.refresh(paths_list)

    def _on_browse(self):
        projects_path = self._project.full_path if self._project else None
        if not projects_path or not os.path.isdir(projects_path):
            projects_path = 'C:/'

        filename = qtutils.get_folder(projects_path, parent=self)
        if not filename:
            return
        filename = path_utils.clean_path(filename)
        if filename and path_utils.is_dir(filename):
            self._on_text_changed(filename)

    def _on_text_changed(self, directory):
        directory = str(directory)
        if not path_utils.is_dir(directory):
            return
        found = self._list.get_directories()
        if directory in found:
            return
        if found:
            found.insert(0, directory)
        else:
            found = [directory]
        self.directoryChanged.emit(found)
        self._list.refresh(found)

        if self._project:
            self._project.set_external_code_paths(found)

    def _on_send_directories(self, directories):
        self.directoryChanged.emit(directories)
        if self._project:
            self._project.set_external_code_paths(directories)
