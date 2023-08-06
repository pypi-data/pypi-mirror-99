from __future__ import annotations

import sys
from pathlib import Path

import pkg_resources
from PySide6.QtCore import QFile, QIODevice, Qt
from PySide6.QtGui import QCursor, QMovie
from PySide6.QtUiTools import QUiLoader
from PySide6.QtWidgets import QButtonGroup, QMainWindow, QFileDialog, QDialog

from plagdef.gui.model import ResultsTableModel

UI_FILES = {
    'main_window': pkg_resources.resource_filename(__name__, 'ui/main_window.ui'),
    'home_widget': pkg_resources.resource_filename(__name__, 'ui/home_widget.ui'),
    'loading_widget': pkg_resources.resource_filename(__name__, 'ui/loading_widget.ui'),
    'error_widget': pkg_resources.resource_filename(__name__, 'ui/error_widget.ui'),
    'no_results_widget': pkg_resources.resource_filename(__name__, 'ui/no_results_widget.ui'),
    'results_widget': pkg_resources.resource_filename(__name__, 'ui/results_widget.ui'),
}


class MainWindow:
    def __init__(self, views: list[View]):
        self._window = _load_ui_file(Path(UI_FILES['main_window']))
        self._views = views
        self._configure()

    def _configure(self):
        for view in self._views:
            self._window.stacked_widget.addWidget(view.widget)

    def switch_to(self, view_cls: type, data=None):
        idx = self._window.stacked_widget.currentIndex()
        for view in self._views:
            if type(view) == view_cls:
                self._views[idx].on_destroy()
                self._window.stacked_widget.setCurrentWidget(view.widget)
                view.on_init(data)

    def show(self):
        self._window.show()


class View:
    def on_init(self, data=None):
        pass

    def on_destroy(self):
        pass


class HomeView(View):
    def __init__(self):
        self.lang = None
        self.recursive = False
        self.widget = _load_ui_file(Path(UI_FILES['home_widget']))
        self._configure()

    def _configure(self):
        self.widget.lang_button_group = QButtonGroup()
        self.widget.lang_button_group.addButton(self.widget.eng_radio)
        self.widget.lang_button_group.addButton(self.widget.ger_radio)
        self.widget.open_folder_button.setCursor(QCursor(Qt.PointingHandCursor))
        self.widget.detect_button.setCursor(QCursor(Qt.PointingHandCursor))
        self.widget.folder_name_label.setVisible(False)
        self.widget.recursive_check_box.setVisible(False)
        self.widget.remove_folder_button.setCursor(QCursor(Qt.PointingHandCursor))
        self.widget.remove_folder_button.setVisible(False)
        self.widget.sel_lang_label.setVisible(False)
        self.widget.change_lang_button.setCursor(QCursor(Qt.PointingHandCursor))
        self.widget.change_lang_button.setVisible(False)

    def register_for_signals(self, open_folder=None, remove_folder=None, select_lang=None,
                             reset_lang_sel=None, detect=None):
        self.widget.open_folder_button.clicked.connect(lambda: open_folder())
        self.widget.remove_folder_button.clicked.connect(lambda: remove_folder())
        self.widget.lang_button_group.buttonClicked.connect(lambda: select_lang())
        self.widget.change_lang_button.clicked.connect(lambda: reset_lang_sel())
        self.widget.detect_button.clicked.connect(lambda: detect())

    def folder_selected(self, folder_name: str):
        self.widget.folder_name_label.setText(
            f'<html><head/><body><p align="center"><span style="font-size:12pt; color:#ffffff;"> '
            f'{folder_name}</span></p></body></html>')
        self.widget.open_folder_button.setVisible(False)
        self.widget.folder_name_label.setVisible(True)
        self.widget.recursive_check_box.setVisible(True)
        self.widget.remove_folder_button.setVisible(True)
        [radio.setEnabled(True) for radio in self.widget.lang_button_group.buttons()]

    def reset_folder_selection(self):
        self.recursive = False
        self.widget.recursive_check_box.setChecked(False)
        self.widget.open_folder_button.setVisible(True)
        self.widget.folder_name_label.setVisible(False)
        self.widget.recursive_check_box.setVisible(False)
        self.widget.remove_folder_button.setVisible(False)
        [radio.setEnabled(False) for radio in self.widget.lang_button_group.buttons()]

    def language_selected(self):
        self.recursive = self.widget.recursive_check_box.isChecked()
        lang_long = self.widget.lang_button_group.checkedButton().text()
        self.lang = lang_long[:3].lower()
        self.widget.sel_lang_label.setText(
            f'<html><head/><body><p align="center"><span style="font-size:12pt; color:#ffffff;"> '
            f'{lang_long}</span></p></body></html>')
        self.widget.recursive_check_box.setEnabled(False)
        self.widget.remove_folder_button.setVisible(False)
        [radio.setVisible(False) for radio in self.widget.lang_button_group.buttons()]
        self.widget.sel_lang_label.setVisible(True)
        self.widget.change_lang_button.setVisible(True)
        self.widget.detect_button.setEnabled(True)

    def reset_language_selection(self):
        self.lang = None
        self.widget.lang_button_group.setExclusive(False)
        self.widget.lang_button_group.checkedButton().setChecked(False)
        self.widget.lang_button_group.setExclusive(True)
        self.widget.detect_button.setEnabled(False)
        self.widget.sel_lang_label.setVisible(False)
        self.widget.change_lang_button.setVisible(False)
        [radio.setVisible(True) for radio in self.widget.lang_button_group.buttons()]
        self.widget.remove_folder_button.setVisible(True)
        self.widget.recursive_check_box.setEnabled(True)

    def on_destroy(self):
        self.reset_language_selection()
        [radio.setEnabled(False) for radio in self.widget.lang_button_group.buttons()]
        self.reset_folder_selection()


class FileDialog(QFileDialog):
    def __init__(self):
        super().__init__()
        self.setFileMode(QFileDialog.Directory)
        self.selected_dir = None

    def open(self) -> bool:
        if self.exec_() == QDialog.Accepted:
            self.selected_dir = self.selectedFiles()[0]
            return True


class LoadingView(View):
    def __init__(self):
        self._movie = QMovie(':/loading.gif')
        self.widget = _load_ui_file(Path(UI_FILES['loading_widget']))
        self._configure()

    def _configure(self):
        self.widget.loading_movie_label.setMovie(self._movie)

    def on_init(self, data=None):
        self._movie.start()

    def on_destroy(self):
        self._movie.stop()


class NoResultsView(View):
    def __init__(self):
        self.widget = _load_ui_file(Path(UI_FILES['no_results_widget']))
        self._configure()

    def _configure(self):
        self.widget.again_button_no_res.setCursor(QCursor(Qt.PointingHandCursor))

    def register_for_signals(self, again=None):
        self.widget.again_button_no_res.clicked.connect(lambda: again())


class ErrorView(View):
    def __init__(self):
        self.widget = _load_ui_file(Path(UI_FILES['error_widget']))
        self._configure()

    def _configure(self):
        self.widget.again_button_err.setCursor(QCursor(Qt.PointingHandCursor))

    def on_init(self, data=None):
        self.widget.error_msg_label.setText(
            f'<html><head/><body><p align="center"><span style=" font-size:12pt; color:#ffffff;"> '
            f'{data}</span></p></body></html>')
        self.widget.error_msg_label.setWordWrap(True)

    def register_for_signals(self, again=None):
        self.widget.again_button_err.clicked.connect(lambda: again())


class ResultView(View):
    def __init__(self):
        self.widget = _load_ui_file(Path(UI_FILES['results_widget']))
        self._configure()

    def _configure(self):
        self.widget.again_button_res.setCursor(QCursor(Qt.PointingHandCursor))

    def on_init(self, data=None):
        model = ResultsTableModel(data)
        self.widget.results_table.setModel(model)
        self.widget.results_table.resizeRowsToContents()
        self.widget.results_table.resizeColumnsToContents()

    def register_for_signals(self, again=None):
        self.widget.again_button_res.clicked.connect(lambda: again())


def _load_ui_file(path: Path) -> QMainWindow:
    main_ui = QFile(str(path))
    if not main_ui.open(QIODevice.ReadOnly):
        print(f"Cannot open {path}: {main_ui.errorString()}")
        sys.exit(-1)
    loader = QUiLoader()
    window = loader.load(main_ui)
    main_ui.close()
    if not window:
        print(loader.errorString())
        sys.exit(-1)
    return window
