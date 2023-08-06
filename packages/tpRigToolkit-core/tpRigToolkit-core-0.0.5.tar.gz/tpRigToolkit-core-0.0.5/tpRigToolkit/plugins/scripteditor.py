#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""
Module that contains script editor tool implementation
"""

from __future__ import print_function, division, absolute_import

from Qt.QtCore import Qt, Signal
from Qt.QtWidgets import QSizePolicy, QWidget

from tpDcc.core import plugin
from tpDcc.managers import resources
from tpDcc.libs.qt.widgets import layouts
from tpDcc.tools.scripteditor.core import client, tool, toolset


class ScriptsEditorPlugin(plugin.DockPlugin, object):

    NAME = 'Scripts Editor'
    TOOLTIP = 'Allow to edit scripts easily'
    DEFAULT_DOCK_AREA = Qt.RightDockWidgetArea
    IS_SINGLETON = True

    def __init__(self):
        super(ScriptsEditorPlugin, self).__init__()

        self._script_editor_widget = None
        self._content = QWidget()
        self._content_layout = layouts.VerticalLayout(spacing=0, margins=(0, 0, 0, 0))
        self._content.setLayout(self._content_layout)
        self.setWidget(self._content)

    @staticmethod
    def icon():
        return resources.icon('source_code')

    def show_plugin(self):
        super(ScriptsEditorPlugin, self).show_plugin()

        if not self._script_editor_widget:

            # Settings are used to colorize script editor text depending on current theme
            settings = self._app.settings()
            self._script_editor_widget = ScriptEditorWidget(settings=settings, parent=self)
            # self._script_editor_widget = scripteditor.ScriptEditorWidget(settings=settings, load_session=False)
            # self._script_editor_widget.scriptSaved.connect(self._on_script_saved)
            self._script_editor_widget.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
            self._content_layout.addWidget(self._script_editor_widget)
            self._script_editor_widget.editorClosed.connect(self.close)

    def load_script(self, script_file):
        if not self._script_editor_widget:
            return

        self._script_editor_widget.controller.load_script(script_file)

    def _on_script_saved(self, file_path):
        pass


class ScriptEditorWidget(toolset.ScriptEditorToolset):

    editorClosed = Signal()

    def __init__(self, *args, **kwargs):
        kwargs['load_session'] = False
        super(ScriptEditorWidget, self).__init__(*args, **kwargs)

        # NOTE: Important to store client in a variable to avoid Python garbage collector to delete it
        self._script_editor_client = client.ScriptEditorClient.create_and_connect_to_server(tool.ScriptEditorTool.ID)

        self.initialize(client=self._script_editor_client)

        self._title_frame.setVisible(False)

        self.model.console_visible = False
        self.model.menubar_visible = False
        self.model.toolbar_visible = False
        # self.model.enable_save_script = False

        self.controller.close_all_scripts()

        self.view.lastTabClosed.connect(self.editorClosed.emit)
