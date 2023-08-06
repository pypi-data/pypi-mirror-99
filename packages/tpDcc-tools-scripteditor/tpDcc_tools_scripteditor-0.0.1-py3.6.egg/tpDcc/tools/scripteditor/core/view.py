#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""
Module that contains view implementation for Script Editor
"""

from __future__ import print_function, division, absolute_import

import os
import sys
import logging
from functools import partial

from Qt.QtCore import Qt, Signal, QSize, QEvent
from Qt.QtWidgets import QWidget, QSplitter, QMenu, QAction, QToolBar, QMenuBar
from Qt.QtGui import QKeySequence

from tpDcc.managers import resources
from tpDcc.libs.python import path as path_utils
from tpDcc.libs.qt.core import base, contexts as qt_contexts
from tpDcc.libs.qt.widgets import window, layouts, label, buttons, stack, dividers

from tpDcc.tools.scripteditor.core import model as script_model, controller as script_controller
from tpDcc.tools.scripteditor.widgets import console, script

LOGGER = logging.getLogger('tpDcc-tools-scripteditor')


class ScriptEditorView(window.BaseWindow, object):

    lastTabClosed = Signal()
    scriptSaved = Signal(str)

    def __init__(self, model, controller, parent=None):

        self._model = model or script_model.ScriptEditorModel()
        self._controller = controller or script_controller.ScriptEditorController(model=self._model)

        super(ScriptEditorView, self).__init__(parent=parent)

        self._controller.update_namespace({'self_output': self._output_console})

        # self._load_settings()

        self.refresh()

        # self._process_args()

    # =================================================================================================================
    # OVERRIDES
    # =================================================================================================================

    @property
    def model(self):
        return self._model

    # =================================================================================================================
    # OVERRIDES
    # =================================================================================================================

    def ui(self):
        super(ScriptEditorView, self).ui()

        self._stack = stack.SlidingOpacityStackedWidget(parent=self)
        main_splitter = QSplitter(Qt.Vertical, parent=self)
        self._output_console = console.OutputConsole(parent=self)
        # NOTE: Scripts Tab MUST pass ScriptEditor as parent because internally some ScriptEditor functions
        # NOTE: are connected to some signals. If we don't do this Maya will crash when opening new Script Editors :)
        self._scripts_tab = script.ScriptsTab(controller=self._controller, parent=self)

        main_splitter.addWidget(self._output_console)
        main_splitter.addWidget(self._scripts_tab)

        self._menu_bar = self._setup_menubar()
        self._tool_bar = self._setup_toolbar()
        self._tool_bar_divider = dividers.Divider()

        # Empty widget
        empty_widget = QWidget(self)
        empty_layout = layouts.HorizontalLayout(spacing=5, margins=(5, 5, 5, 5))
        empty_widget.setLayout(empty_layout)
        main_empty_layout = layouts.VerticalLayout(spacing=5, margins=(5, 5, 5, 5))
        self._empty_label = label.BaseLabel('No Scripts Opened', parent=self).h4().strong()
        self._empty_label.setAlignment(Qt.AlignCenter)
        main_empty_layout.addStretch()
        main_empty_layout.addWidget(self._empty_label)
        main_empty_layout.addStretch()
        empty_layout.addStretch()
        empty_layout.addLayout(main_empty_layout)
        empty_layout.addStretch()

        self._stack.addWidget(empty_widget)
        self._stack.addWidget(main_splitter)

        self.main_layout.addWidget(self._menu_bar)
        self.main_layout.addWidget(self._tool_bar)
        self.main_layout.addWidget(self._tool_bar_divider)
        self.main_layout.addWidget(self._stack)

    def setup_signals(self):
        self._scripts_tab.lastTabClosed.connect(self.lastTabClosed.emit)
        self._output_console.outputTextChanged.connect(self._controller.set_output_text)
        self._scripts_tab.currentChanged.connect(self._on_current_tab_changed)
        self._scripts_tab.selectionChanged.connect(self._on_selection_changed)
        self._scripts_tab.scriptTextChanged.connect(self._on_script_text_changed)

        self._model.consoleVisibleChanged.connect(self._on_console_visible_changed)
        self._model.toolbarVisibleChanged.connect(self._on_toolbar_visible_changed)
        self._model.menubarVisibleChanged.connect(self._on_menubar_visible_changed)
        self._model.sessionPathChanged.connect(self._on_session_changed)
        self._model.currentScriptChanged.connect(self._on_current_script_changed)
        self._model.currentTextChanged.connect(self._on_current_text_changed)
        self._model.outputTextChanged.connect(self._on_output_text_changed)
        self._model.scriptOpened.connect(self._on_script_opened)
        self._model.scriptSaved.connect(self._on_script_saved)
        self._model.scriptClosed.connect(self._on_script_closed)

    def eventFilter(self, obj, event):
        if event.type() in (QEvent.Move, QEvent.Resize):
            self._adjust_completers()

        return super(ScriptEditorView, self).eventFilter(obj, event)

    def closeEvent(self, event):
        # self.save_current_session()
        # self._save_settings()
        super(ScriptEditorView, self).closeEvent(event)

    # =================================================================================================================
    # BASE
    # =================================================================================================================

    def refresh(self):
        self._update_session()
        self._execute_selected_action.setEnabled(bool(self._model.selected_text))
        self._output_console.setVisible(self._model.console_visible)
        self._tool_bar.setVisible(self._model.toolbar_visible)
        self._tool_bar_divider.setVisible(self._model.toolbar_visible)
        self._menu_bar.setVisible(self._model.menubar_visible)
        self._refresh_stack()

    # =================================================================================================================
    # INTERNAL
    # =================================================================================================================

    def _setup_menubar(self):
        """
        Internal function that setups menu bar for the widget
        :return:
        """

        menubar = self.menuBar()

        save_icon = resources.icon('save')
        load_icon = resources.icon('open_folder')
        play_icon = resources.icon('play')
        clear_icon = resources.icon('delete')
        resume_icon = resources.icon('resume')
        undo_icon = resources.icon('undo')
        redo_icon = resources.icon('redo')
        copy_icon = resources.icon('copy')
        cut_icon = resources.icon('cut')
        paste_icon = resources.icon('paste')
        tab_icon = resources.icon('tab')
        quote_icon = resources.icon('quote')
        rename_icon = resources.icon('rename')
        keyboard_icon = resources.icon('keyboard')
        help_icon = resources.icon('help')

        file_menu = QMenu('File', menubar)
        menubar.addMenu(file_menu)
        save_session_action = QAction(save_icon, 'Save Session', file_menu)
        load_script_action = QAction(load_icon, 'Load Script', file_menu)
        save_script_action = QAction(save_icon, 'Save Script', file_menu)
        file_menu.addAction(save_session_action)
        file_menu.addAction(load_script_action)
        file_menu.addAction(save_script_action)
        load_script_action.setShortcut('Ctrl+O')
        # load_script_action.setShortcutContext(Qt.WidgetShortcut)
        save_script_action.setShortcut('Ctrl+S')
        # save_script_action.setShortcutContext(Qt.WidgetShortcut)

        edit_menu = QMenu('Edit', self)
        menubar.addMenu(edit_menu)
        undo_action = QAction(undo_icon, 'Undo', edit_menu)
        redo_action = QAction(redo_icon, 'Redo', edit_menu)
        copy_action = QAction(copy_icon, 'Copy', edit_menu)
        cut_action = QAction(cut_icon, 'Cut', edit_menu)
        paste_action = QAction(paste_icon, 'Paste', edit_menu)
        tab_to_spaces_action = QAction(tab_icon, 'Tab to Spaces', edit_menu)
        comment_action = QAction(quote_icon, 'Comment', edit_menu)
        find_and_replace = QAction(rename_icon, 'Find and Replace', edit_menu)
        edit_menu.addAction(undo_action)
        edit_menu.addAction(redo_action)
        edit_menu.addSeparator()
        edit_menu.addAction(copy_action)
        edit_menu.addAction(cut_action)
        edit_menu.addAction(paste_action)
        edit_menu.addSeparator()
        edit_menu.addAction(tab_to_spaces_action)
        edit_menu.addAction(comment_action)
        edit_menu.addAction(find_and_replace)

        run_menu = QMenu('Run', self)
        menubar.addMenu(run_menu)
        self._execute_all_action = QAction(play_icon, 'Execute All', run_menu)
        self._execute_all_action.setShortcut('Ctrl+Shift+Return')
        self._execute_all_action.setShortcutContext(Qt.ApplicationShortcut)
        self._execute_selected_action = QAction(resume_icon, 'Execute Selected', run_menu)
        self._execute_selected_action.setShortcut('Ctrl+Return')
        self._execute_selected_action.setShortcutContext(Qt.WidgetWithChildrenShortcut)
        self._clear_output_action = QAction(clear_icon, 'Clear Output', run_menu)

        run_menu.addAction(self._execute_all_action)
        run_menu.addAction(self._execute_selected_action)
        run_menu.addAction(self._clear_output_action)

        help_menu = QMenu('Help', self)
        menubar.addMenu(help_menu)
        show_shortcuts_action = QAction(keyboard_icon, 'Show Shortcuts', help_menu)
        print_help_action = QAction(help_icon, 'Print Help', help_menu)
        help_menu.addAction(show_shortcuts_action)
        help_menu.addSeparator()
        help_menu.addAction(print_help_action)
        undo_action.setShortcut('Ctrl+Z')
        undo_action.setShortcutContext(Qt.WidgetShortcut)
        redo_action.setShortcut('Ctrl+Y')
        redo_action.setShortcutContext(Qt.WidgetShortcut)
        copy_action.setShortcut('Ctrl+C')
        copy_action.setShortcutContext(Qt.WidgetShortcut)
        cut_action.setShortcut('Ctrl+X')
        cut_action.setShortcutContext(Qt.WidgetShortcut)
        paste_action.setShortcut('Ctrl+V')
        paste_action.setShortcutContext(Qt.WidgetShortcut)
        comment_action.setShortcut(QKeySequence(Qt.ALT + Qt.Key_Q))
        comment_action.setShortcutContext(Qt.WidgetShortcut)

        self._execute_all_action.triggered.connect(self._controller.execute_script)
        self._execute_selected_action.triggered.connect(partial(self._controller.execute_script, True))
        self._clear_output_action.triggered.connect(partial(self._controller.set_output_text, ''))
        # open_settings_folder_action.triggered.connect(self._open_settings)
        # show_shortcuts_action.triggered.connect(self._open_shortcuts)
        # print_help_action.triggered.connect(self.editor_help)
        save_session_action.triggered.connect(self._controller.save_current_session)
        save_script_action.triggered.connect(self._controller.save_script)
        load_script_action.triggered.connect(self._controller.load_script)
        undo_action.triggered.connect(self._scripts_tab.undo)
        redo_action.triggered.connect(self._scripts_tab.redo)
        copy_action.triggered.connect(self._scripts_tab.copy)
        cut_action.triggered.connect(self._scripts_tab.cut)
        paste_action.triggered.connect(self._scripts_tab.paste)
        tab_to_spaces_action.triggered.connect(self._controller.convert_tab_to_spaces)
        # find_and_replace.triggered.connect(self._open_find_replace)
        comment_action.triggered.connect(self._scripts_tab.comment)

        return menubar

    def _setup_toolbar(self):
        """
        Internal function that setups script editor toolbar
        """

        toolbar = QToolBar('Script Editor ToolBar', parent=self)
        toolbar.setIconSize(QSize(16, 16))

        execute_btn = buttons.BaseToolButton(parent=self)
        execute_btn.setToolButtonStyle(Qt.ToolButtonTextUnderIcon)
        execute_selected_btn = buttons.BaseToolButton(parent=self)
        execute_selected_btn.setToolButtonStyle(Qt.ToolButtonTextUnderIcon)
        clear_output_btn = buttons.BaseToolButton(parent=self)
        clear_output_btn.setToolButtonStyle(Qt.ToolButtonTextUnderIcon)

        toolbar.addWidget(execute_btn)
        toolbar.addWidget(execute_selected_btn)
        toolbar.addWidget(clear_output_btn)

        execute_btn.setDefaultAction(self._execute_all_action)
        execute_selected_btn.setDefaultAction(self._execute_selected_action)
        clear_output_btn.setDefaultAction(self._clear_output_action)

        return toolbar

    def _update_session(self):
        """
        Internal function that updates ui taking into account the current active session
        """

        current_session = self._controller.get_session()
        if not current_session:
            self._scripts_tab.add_new_tab()
        else:
            sessions = current_session.read()
            self._scripts_tab.clear()
            active = 0
            if sessions:
                for i, s in enumerate(sessions):
                    script_file = s.get('file', None)
                    script_name = s.get('name', '')
                    script_text = s.get('text', '')
                    if script_file and os.path.isfile(script_file):
                        script_editor = self._scripts_tab.add_new_tab(script_name, script_file)
                    else:
                        script_editor = self._scripts_tab.add_new_tab(script_name, script_text)
                    if s.get('active', False):
                        active = i
                    script_editor.set_font_size(s.get('size', None))
                else:
                    self._scripts_tab.add_new_tab()
                self._scripts_tab.setCurrentIndex(active)

    def _adjust_completers(self):
        """
        Internal callback function that updates the size of the completers depending on its visiblity
        """

        for i in range(self._scripts_tab.count()):
            script_widget = self._scripts_tab.widget(i)
            if not script_widget:
                continue
            if script_widget.editor.completer.isVisible():
                script_widget.editor.move_completer()

    def _refresh_stack(self):
        """
        Internal function that updates stack status
        """

        total_scripts = len(list(self._model.scripts.items()))
        if total_scripts <= 0:
            self._stack.setCurrentIndex(0)
        else:
            self._stack.setCurrentIndex(1)
            # self._scripts_tab.widget(0).editor.setFocus()

    def _process_args(self):
        """
        Internal function that adds processes given args
        If file path is given in sys.argv, we tyr to open it ...
        :return:
        """

        if sys.argv:
            f = sys.argv[-1]
            if os.path.exists(f):
                if not os.path.basename(f) == os.path.basename(__file__):
                    if os.path.splitext(f)[-1] in ['.txt', '.py']:
                        self._output_console.show_message(os.path.splitext(f)[-1])
                        self._output_console.show_message('Open File: ' + f)
                        self._scripts_tab.add_new_tab(os.path.basename(f), f)
                        if self._scripts_tab.count() == 2:
                            self._scripts_tab.removeTab(0)

    # =================================================================================================================
    # CALLBACKS
    # =================================================================================================================

    def _on_console_visible_changed(self, flag):
        """
        Internal callback function that is called when console visibility is changed in the model
        :param flag: bool
        """

        self._output_console.setVisible(flag)

    def _on_toolbar_visible_changed(self, flag):
        """
        Internal callback function that is called when toolbar visibility is changed in the model
        :param flag: bool
        """

        self._tool_bar.setVisible(flag)
        self._tool_bar_divider.setVisible(flag)

    def _on_menubar_visible_changed(self, flag):
        """
        Internal callback function that is called when menubar visibility is changed in the model
        :param flag: bool
        """

        self._menu_bar.setVisible(flag)

    def _on_current_tab_changed(self, index):
        """
        Internal callback function that is called when current user selects a new script tab
        :param index: int
        """

        script_widget = self._scripts_tab.widget(index)
        if not script_widget:
            return

        script_path = script_widget.file_path

        all_text = self._scripts_tab.get_current_text()
        with qt_contexts.block_signals(self._model):
            self._controller.set_current_script(script_path)
            self._controller.set_current_text(all_text.strip() if all_text else '')

    def _on_selection_changed(self, text):
        """
        Internal callback function that is called when user selects new script text
        :param text: str
        """

        with qt_contexts.block_signals(self._model):
            self._controller.set_selected_text(text)
        self._execute_selected_action.setEnabled(bool(self._model.selected_text))

    def _on_script_text_changed(self, text):
        """
        Internal callback function that is called when script text changes
        :param text: str
        """

        with qt_contexts.block_signals(self._model):
            self._controller.set_current_text(text)

    def _on_session_changed(self):
        """
        Internal callback function that is called when current session is changed in the model
        """

        self._update_session()

    def _on_current_script_changed(self, script_path):
        """
        Internal callback function that is called each time current selected script is updated in the model
        :param script_path: str
        :return:
        """

        script_path = path_utils.clean_path(script_path)
        for i in range(self._scripts_tab.count()):
            script_widget = self._scripts_tab.widget(i)
            if not script_widget:
                continue
            if path_utils.clean_path(script_widget.file_path) == script_path:
                self._scripts_tab.setCurrentIndex(i)
                return

    def _on_current_text_changed(self, script_text):
        """
        Internal callback function that is called when current script text is updated by the model
        :param script_text: str
        """

        script_widget = self._scripts_tab.currentWidget()
        if not script_widget:
            return

        with qt_contexts.block_signals(self._model):
            script_widget.editor.setPlainText(script_text)

    def _on_output_text_changed(self, output_text):
        """
        Internal callback function that is called when output text is updated in the model
        :param output_text: str
        """

        with qt_contexts.block_signals(self._model):
            self._output_console.setText(output_text)
            self._output_console.move_cursor_to_line_end()

    def _on_script_opened(self, script_path):
        """
        Internal callback function that is called when a new script is opened by the model
        :param script_path: str
        """

        if not script_path or not os.path.isfile(script_path):
            return

        self._scripts_tab.add_new_tab(os.path.basename(script_path), script_path, skip_if_exists=True)

        self._refresh_stack()

    def _on_script_saved(self, script_path):
        """
        Internal callback function that is called when a script is saved
        :param script_path: str
        """

        script_widget = self._scripts_tab.currentWidget()
        if not script_widget:
            return

        with qt_contexts.block_signals(self._model):
            script_path = path_utils.clean_path(script_path)
            current_file_path = path_utils.clean_path(script_widget.file_path)
            if script_path != current_file_path:
                script_widget.file_path = script_path
            self._scripts_tab.set_current_tab_name(os.path.basename(script_widget.file_path))
            self._controller.set_current_script(script_widget.file_path)
            self._controller.set_current_text(self._scripts_tab.get_current_text())
            self._controller.set_selected_text(self._scripts_tab.get_current_selected_text())

    def _on_script_closed(self, script_path):
        """
        Internal callback function that is called when a script is closed by model
        :param script_path: str
        """

        if not script_path:
            return

        script_path = path_utils.clean_path(script_path)

        for i in range(self._scripts_tab.count()):
            script_widget = self._scripts_tab.widget(i)
            if not script_widget:
                continue
            if path_utils.clean_path(script_widget.file_path) == script_path:
                self._scripts_tab.removeTab(i, force=True)
                break

        self._refresh_stack()
