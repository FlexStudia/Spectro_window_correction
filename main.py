# coding: utf-8
import copy

# MODULES
from PyQt6 import QtWidgets
from PyQt6.QtGui import QAction
from PyQt6.QtWidgets import QFileDialog, QApplication, QMessageBox
from PyQt6.QtCore import Qt, QSettings
import sys
import os
from pathlib import Path
import numpy as np
import pyqtgraph as pg

# PACKAGES
from tools.data_pars import DataPars as DataPars
from tools.array_tools import is_array_empty
from presets.transmission_sapphire_window import SAPPHIRE_WINDOW_WAVELENGTHS, SAPPHIRE_WINDOW_TRANSMISSION
from core import CoreWindowCorrection

# TEMPLATES
from templates.mw import Ui_MainWindow as Ui_MainWindow

# GLOBALS
version = "0.1.2"
copyright = "<a href='https:www.gnu.org/licenses/gpl-3.0.html'>The GNU General Public License v3.0</a>"
author_mail = "<a href='mailto: flex.studia.dev@gmail.com'>flex.studia.dev@gmail.com</a>"
bug_support_mail = "<a href='mailto: flex.studia.help@gmail.com'>flex.studia.help@gmail.com</a>"
github_url = "https://github.com/FlexStudia/Spectro_window_correction"
__app_name__ = "Window correction"
__org_name__ = "Flex Studia Dev"
__org_site__ = github_url
settings = QSettings(__org_name__, __app_name__)
about_text = (f"<b>{__app_name__}</b> v.{version}"
              f"<p>Copyright: {copyright}</p>"
              f"<p><a href='{github_url}'>GitHub repository</a> (program code and more information)</p>"
              f"<p>Created by Gorbacheva Maria ({author_mail})</p>"
              "<p>Scientific base by Bernard Schmitt, IPAG (<a href='mailto: bernard.schmitt@univ-grenoble-alpes.fr'>bernard.schmitt@univ-grenoble-alpes.fr</a>)</p>"
              f"<p>For any questions and bug reports, please, mail at {bug_support_mail}</p>"
              "<p>In case of a bug, please report it and specify your operating system, "
              "provide a detailed description of the problem with screenshots "
              "and the files used and produced, if possible. Your contribution matters to make this program better!</p>")


class CorrectorMainW(QtWidgets.QMainWindow):
    def __init__(self):
        super(CorrectorMainW, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        # setter & globals
        self.class_setter()
        self.set_globals()
        # window tilte
        self.setWindowTitle(f"{__app_name__} v.{version}")
        # menu
        self.set_menu()
        # UI
        self.set_ui()

    # init -> class setter & globals
    def class_setter(self):
        # spectrum
        self.spectrum_data = np.zeros(0)
        self.spectrum_path = ""
        self.spectrum_file_header = ""
        self.spectrum_file_separator = ""
        self.spectrum_file_accuracy = []
        # transmission
        self.transmission_data = np.zeros(0)
        # windows quantity
        self.windows_quantity = 1
        # correction type
        self.correction_type = "parasitic reflections"

    def set_globals(self):
        # bigger btn style
        self.bigger_btn_style = "QPushButton{padding: 7px; font-size: 14px;}"
        # reflectance factor columns list
        self.reflectance_columns_list =[]
        # transmission list
        self.window_transmission_presets_dict = {"sapphire window": [SAPPHIRE_WINDOW_WAVELENGTHS, SAPPHIRE_WINDOW_TRANSMISSION]}
        self.window_material = list(self.window_transmission_presets_dict.keys())[0]
        # advanced transmission settings toggle
        self.settings_on = False
        # graph lines
        line_width = 2
        pen_st = pg.mkPen(color=(54, 135, 211), width=line_width)
        self.initial_spectrum_line = pg.PlotCurveItem(clear=True, pen=pen_st, name="initial spectrum")
        pen_st = pg.mkPen(color=(234, 129, 0), width=line_width)
        self.corrected_spectrum_line = pg.PlotCurveItem(clear=True, pen=pen_st, name="corrected spectrum")
        # warning system dict
        self.tool_tip_dict = {
            # spectrum
            "spectrum empty": (self.ui.spectrum_state, self.ui.spectrum_text_output, "question",
                               "Load a spectrum file to correct"),
            "spectrum loaded": (self.ui.spectrum_state, self.ui.spectrum_text_output, "ok",
                                "The spectrum file has been successfully loaded"),
            "spectrum error": (self.ui.spectrum_state, self.ui.spectrum_text_output, "error",
                               "Unable to load the spectrum file"),
            "spectrum exceeds t": (self.ui.spectrum_state, self.ui.spectrum_text_output, "error",
                                             "The wavelengths of the spectrum exceed the transmission wavelengths!"),
            "spectrum exceeds no more": (self.ui.spectrum_state, self.ui.spectrum_text_output, "ok",
                                         "The wavelengths of the spectrum no longer exceed the transmission wavelengths!"),
            # transmission
            "transmission from preset": (self.ui.transmission_state, self.ui.transmission_text_output, "ok",
                                   "The transmission was successfully loaded from the built-in preset."),
            "transmission loaded": (self.ui.transmission_state, self.ui.transmission_text_output, "ok",
                                    "The transmission file has been successfully loaded"),
            "transmission error": (self.ui.transmission_state, self.ui.transmission_text_output, "error",
                                   "Unable to load the transmission file"),
            "transmission is exceeded by s": (self.ui.transmission_state, self.ui.transmission_text_output, "error",
                                              "The wavelengths of the spectrum exceed the transmission wavelengths!"),
            "transmission is exceeded no more": (self.ui.transmission_state, self.ui.transmission_text_output, "ok",
                                                 "The wavelengths of the spectrum no longer exceed the transmission wavelengths!"),
            # calc
            "not ready to calc": (self.ui.correction_state, self.ui.correction_text_output, "error",
                                  "Complete entering the parameters before performing the calculation"),
            "not calc yet": (self.ui.correction_state, self.ui.correction_text_output, "question",
                             "Everything is ready for calculation!"),
            "calc expired": (self.ui.correction_state, self.ui.correction_text_output, "question",
                             "The parameters have changed.\nPlease recalculate"),
            "calc error": (self.ui.correction_state, self.ui.correction_text_output, "error",
                           "Something has gone wrong.\nUnable to calculate"),
            "calc finished": (self.ui.correction_state, self.ui.correction_text_output, "ok",
                              "The calculation has been successfully completed!"),
            # export
            "export expired": (self.ui.export_state, self.ui.export_text_output, "question",
                               "The parameters have changed. The previous result is still available for export."
                               "\nHowever, to be able to export the result for the new parameters, please perform the calculation."),
            "nothing to export": (self.ui.export_state, self.ui.export_text_output, "question",
                                  "The calculation has not yet been performed.\nPlease enter the parameters first and then perform the calculation."),
            "export ready": (self.ui.export_state, self.ui.export_text_output, "ok",
                             "The export is ready!"),
            "export finished": (self.ui.export_state, self.ui.export_text_output, "ok",
                                "The export has been completed successfully!"),
            "export error": (self.ui.export_state, self.ui.export_text_output, "error",
                             "Something has gone wrong.\nUnable to export"),
        }
        # OUTPUTS
        self.corrected_spectrum = np.zeros(0)

    # messages
    def show_dialog(self, message, title, icon, buttons=QMessageBox.StandardButton.Ok):
        dlg = QMessageBox(self)
        dlg.setWindowTitle(title)
        dlg.setText(message)
        dlg.setIcon(icon)
        dlg.setStandardButtons(buttons)
        return dlg.exec()

    def show_info_dialog(self, message, title="Information"):
        self.show_dialog(message, title, QMessageBox.Icon.Information)

    def show_error_dialog(self, message, title="Error!"):
        self.show_dialog(message, title, QMessageBox.Icon.Critical)

    # init -> set_menu
    def set_menu(self):
        try:
            extractAction = QAction("&About", self)
            extractAction.setStatusTip('About The App')
            extractAction.triggered.connect(self.show_about)
            self.statusBar()
            mainMenu = self.menuBar()
            fileMenu = mainMenu.addMenu('&Help')
            fileMenu.addAction(extractAction)
        except Exception as e:
            message = f"Error in set_menu: {e}"
            self.show_error_dialog(self, message)

    # init -> set_menu -> show_about
    def show_about(self):
        self.show_info_dialog(about_text, "About")

    # init -> set_ui
    def set_ui(self):
        try:
            self.set_parameters_tab()
            self.set_calc_tab()
            self.set_export_tab()
        except Exception as e:
            message = f"Error in set_ui: {e}"
            self.show_error_dialog(self, message)

    # init -> set_ui -> set_parameters_tab
    def set_parameters_tab(self):
        try:
            self.set_spectrum()
            self.set_transmission()
            self.set_windows_quantity()
            self.set_correction_type()
        except Exception as e:
            message = f"Error in set_parameters_tab: {e}"
            self.show_error_dialog(self, message)

    # init -> set_ui -> set_parameters_tab -> set_spectrum
    def set_spectrum(self):
        try:
            # WS call: no spectrum on load
            self.warning_system("spectrum empty")
            # spectrum_select btn dilog & style
            self.ui.spectrum_select.clicked.connect(lambda: self.select_file_dialog("spectrum loaded"))
            self.ui.spectrum_select.setStyleSheet(f"{self.bigger_btn_style}")
        except Exception as e:
            message = f"Error in set_spectrum: {e}"
            self.show_error_dialog(self, message)

    # init -> set_ui -> set_parameters_tab -> set_transmission
    def set_transmission(self):
        try:
            # preset qcb setup
            self.ui.transmission_preset.insertItems(0, self.window_transmission_presets_dict.keys())
            self.ui.transmission_preset.currentIndexChanged.connect(self.on_transmission_preset_change)
            # advanced settings btn
            self.ui.advanced_settings_toggle.clicked.connect(self.advanced_settings_toggle)
            # custome transmission from file
            self.ui.custome_transmission_container.setVisible(self.settings_on)
            self.warning_system("transmission from preset")
            self.ui.transmission_select.clicked.connect(lambda: self.select_file_dialog("transmission loaded"))
            self.ui.transmission_select.setStyleSheet(f"{self.bigger_btn_style}")
            # load settings saved from previous session
            self.load_transmission_from_settings()
        except Exception as e:
            message = f"Error in set_transmission: {e}"
            self.show_error_dialog(self, message)

    # init -> set_ui -> set_parameters_tab -> set_transmission -> on_transmission_preset_change
    def on_transmission_preset_change(self):
        # save new index value in settings
        settings.setValue("transmission_preset_index", self.ui.transmission_preset.currentIndex())

    # init -> set_ui -> set_parameters_tab -> set_transmission -> advanced_settings_toggle
    def advanced_settings_toggle(self):
        try:
            self.settings_on = not self.settings_on  # switch the flag
            self.ui.custome_transmission_container.setVisible(self.settings_on)  # toggle container visibility
            if self.settings_on:  # change text for the visual effect
                self.ui.advanced_settings_toggle.setText("⯆ Advanced settings")
            else:
                self.ui.advanced_settings_toggle.setText("> Advanced settings")
        except Exception as e:
            message = f"Error in advanced_settings_toggle: {e}"
            self.show_error_dialog(self, message)

    # init -> set_ui -> set_parameters_tab -> set_transmission -> load_transmission_settings
    def load_transmission_from_settings(self):
        if not settings.value("transmission_preset_index") and not settings.value("transmission_preset_index") == 0: # if no settings yet
            settings.setValue("transmission_preset_index", 0)
        else:
            if settings.value("transmission_preset_index") == len(self.window_transmission_presets_dict.keys()):
                # transmission from file
                if os.path.exists(settings.value("transmission_file_path")): # load from file if exists
                    self.advanced_settings_toggle()
                    self.select_file_action(settings.value("transmission_file_path"), "transmission loaded")
                else: # change settings if file in settings doesn't exist
                    settings.setValue("transmission_preset_index", 0)
            else: # transmission from preset
                self.ui.transmission_preset.setCurrentIndex(settings.value("transmission_preset_index"))

    # init -> set_ui -> set_parameters_tab -> set_windows_quantity
    def set_windows_quantity(self):
        try:
            # fill windows_quantity
            windows_quantity_list = ["1", "2"]
            self.ui.windows_quantity.insertItems(0, windows_quantity_list)
            # load windows quantity saved from the last session in settings
            if settings.value("windows_quantity_index") or settings.value("windows_quantity_index") == 0:
                self.ui.windows_quantity.setCurrentIndex(settings.value("windows_quantity_index"))
            else:
                settings.setValue("windows_quantity_index", 0)
            # connect function on change
            self.ui.windows_quantity.currentIndexChanged.connect(self.on_windows_quantity_change)
        except Exception as e:
            message = f"Error in set_windows_quantity: {e}"
            self.show_error_dialog(self, message)

    # init -> set_ui -> set_parameters_tab -> set_windows_quantity -> on_windows_quantity_change
    def on_windows_quantity_change(self):
        try:
            # set the global variable
            self.windows_quantity = int(self.ui.windows_quantity.currentText())
            # save new value in settings
            settings.setValue("windows_quantity_index", self.ui.windows_quantity.currentIndex())
            # propagate the change to calc & export tabs
            self.on_any_parameter_change()
        except Exception as e:
            message = f"Error in on_windows_quantity_change: {e}"
            self.show_error_dialog(self, message)

    # init -> set_ui -> set_parameters_tab -> set_correction_type
    def set_correction_type(self):
        try:
            # fill correction_type qcb
            correction_type = ["parasitic reflections (SHINE collimated beam)",
                               "extended correction (SHADOWS, or SHINE in Gognito mode)"]
            self.ui.correction_type.insertItems(0, correction_type)
            # load from settings tha last saved value
            if settings.value("correction_type_index") or settings.value("correction_type_index") == 0:
                self.ui.correction_type.setCurrentIndex(settings.value("correction_type_index"))
            else:
                settings.setValue("correction_type_index", 0)
            # connect function on change
            self.ui.correction_type.currentIndexChanged.connect(self.on_correction_type_change)
        except Exception as e:
            message = f"Error in set_correction_type: {e}"
            self.show_error_dialog(self, message)

    # init -> set_ui -> set_parameters_tab -> set_correction_type -> on_correction_type_change
    def on_correction_type_change(self):
        try:
            # save the new value in settings
            settings.setValue("correction_type_index", self.ui.correction_type.currentIndex())
            # and in the global variable too
            if self.ui.correction_type.currentIndex() == 0:
                self.correction_type = "parasitic reflections"
            else:
                self.correction_type = "extended correction"
            # propagate the change to the calc & export tabs
            self.on_any_parameter_change()
        except Exception as e:
            message = f"Error in correction_type_changed: {e}"
            self.show_error_dialog(self, message)

    # on_any_parameter_change
    def on_any_parameter_change(self):
        try:
            if "ok" in self.ui.correction_state.text():
                self.warning_system("calc expired")
            if "ok" in self.ui.export_state.text():
                self.warning_system("export expired")
        except Exception as e:
            message = f"Error in on_any_parameter_change: {e}"
            self.show_error_dialog(self, message)

    # init -> set_ui -> set_parameters_tab -> set_spectrum/set_transmission -> select_file_dialog
    def select_file_dialog(self, action_type):
        try:
            # search in settings for the last saved location
            if settings.value(action_type + "_dir") and os.path.isdir(settings.value(action_type + "_dir")):
                dir_name = settings.value(action_type + "_dir")
            else:
                dir_name = ""
            # file path dialog
            file_path, _ = QFileDialog.getOpenFileName(self, "Select a file", dir_name,
                                                       "Text documents (*.txt *.csv *tsv);;All files (*.*)")
            # if valid file path
            if os.path.isfile(file_path):
                settings.setValue(action_type + "_dir", os.path.dirname(file_path)) # update settings
                self.select_file_action(file_path, action_type) # run further processing
        except Exception as e:
            message = f"Error in select_file_dialog: {e}"
            self.show_error_dialog(self, message)

    # init -> set_ui -> set_parameters_tab -> set_spectrum/set_transmission -> select_file_dialog -> select_file_action
    def select_file_action(self, file_path, action_type):
        def get_file_data(file_path):
            try:
                data_read = DataPars(file_path)
                data_read.file_pars_f()
                return data_read.file_body, data_read.file_header, data_read.file_separator, data_read.file_accuracy
            except:
                return np.zeros(0), "", "", np.zeros(0)

        try:
            if os.path.isfile(file_path):
                # file read: get all data & parameters
                file_content, file_header, file_separator, file_accuracy = get_file_data(file_path)
                # set label with file nme
                self.set_file_label(file_path, action_type)
                # file data processing
                if not is_array_empty(file_content) or len(file_content) > 1: # there is data
                    # set globals
                    self.set_globals_with_loaded_data(action_type, file_content)
                    # expire calc & export if exist
                    self.on_any_parameter_change()
                    # on specific data type load
                    if action_type == "spectrum loaded":
                        self.on_spectrum_load(file_path, file_header, file_separator, file_accuracy)
                    elif action_type == "transmission loaded":
                        self.on_transmission_load(file_path)
                else: # there is no data
                    self.on_no_data_in_file(action_type)
        except Exception as e:
            message = f"Error in select_file_action: {e}"
            self.show_error_dialog(self, message)

    # init -> set_ui -> set_parameters_tab -> set_spectrum/set_transmission -> select_file_dialog -> select_file_action
    # -> set_file_label
    def set_file_label(self, file_path, action_type):
        try:
            if action_type == "spectrum loaded":
                self.ui.spectrum_label.setText(os.path.basename(file_path))
            elif action_type == "transmission loaded":
                self.ui.transmission_label.setText(os.path.basename(file_path))
        except Exception as e:
            message = f"Error in set_file_label: {e}"
            self.show_error_dialog(self, message)

    # init -> set_ui -> set_parameters_tab -> set_spectrum/set_transmission -> select_file_dialog -> select_file_action
    # -> set_globals_with_loaded_data
    def set_globals_with_loaded_data(self, action_type, file_content):
        try:
            if action_type == "spectrum loaded":
                self.spectrum_data = file_content
            elif action_type == "transmission loaded":
                self.transmission_data = file_content
        except Exception as e:
            message = f"Error in set_globals_with_loaded_data: {e}"
            self.show_error_dialog(self, message)

    # init -> set_ui -> set_parameters_tab -> set_spectrum/set_transmission -> select_file_dialog -> select_file_action
    # -> on_spectrum_load
    def on_spectrum_load(self, file_path, file_header, file_separator, file_accuracy):
        def there_is_transmission():
            if (self.ui.transmission_preset.currentIndex() != self.ui.transmission_preset.count() - 1
                    or "ok" in self.ui.transmission_state.text()
                    or "exceed" in self.ui.transmission_text_output.text()):
                return True
            return False

        try:
            # WS change
            if there_is_transmission():
                if self.spectrum_exceeds_transmission():
                    self.warning_system("spectrum exceeds t") # update spectrum status
                    self.warning_system("not ready to calc") # change calc status
                else:
                    self.warning_system("spectrum loaded") # update spectrum status
                    if "exceed" in self.ui.transmission_text_output.text(): # update transmission status
                        self.warning_system("transmission is exceeded no more")
                    self.warning_system("not calc yet") # change calc status
            else:
                self.warning_system("spectrum loaded") # update file status
            # save spectrum file parameters for later use in export
            self.spectrum_path = file_path
            self.spectrum_file_header = file_header
            self.spectrum_file_separator = file_separator
            self.spectrum_file_accuracy = file_accuracy
            # fill reflectance factor columns list
            self.fill_reflectance_columns_list()
            # plot the initial spectrum
            self.plot_initial_spectrum()
        except Exception as e:
            message = f"Error in on_spectrum_load: {e}"
            self.show_error_dialog(self, message)

    # init -> set_ui -> set_parameters_tab -> set_spectrum/set_transmission -> select_file_dialog -> select_file_action
    # -> on_spectrum_load -> fill_reflectance_columns_list
    def fill_reflectance_columns_list(self):
        try:
            # initialize the list
            self.reflectance_columns_list = []
            if len(self.spectrum_data[0]) in [2, 3]: # simple 3-column
                self.reflectance_columns_list = [1]
            elif len(self.spectrum_data[0]) in [11, 12, 13] and "Raw" in self.spectrum_file_header[-1]: # raw
                self.reflectance_columns_list = [3]
            else: # compilations
                self.reflectance_columns_list = [num for num in range(len(self.spectrum_data[0]) - 1) if num % 2 != 0]
        except Exception as e:
            message = f"Error in fill_reflectance_columns_list: {e}"
            self.show_error_dialog(self, message)

    # init -> set_ui -> set_parameters_tab -> set_spectrum/set_transmission -> select_file_dialog -> select_file_action
    # -> on_spectrum_load -> plot_initial_spectrum
    def plot_initial_spectrum(self):
        try:
            # fill graph_plot_options
            if len(self.reflectance_columns_list) == 1: # on column case
                self.ui.graph_plot_options.setVisible(False)
                graph_options = ["reflectance factor"]
            else: # compilation case
                self.ui.graph_plot_options.setVisible(True)
                headers_list = self.spectrum_file_header[-1].split(self.spectrum_file_separator)
                graph_options = []
                for column in self.reflectance_columns_list:
                    graph_options.append(f"{headers_list[column]}")
            self.ui.graph_plot_options.clear()
            self.ui.graph_plot_options.insertItems(0, graph_options)
            # plot first possible column
            self.initial_spectrum_line.setData(self.spectrum_data[:, 0],
                                               self.spectrum_data[:, self.reflectance_columns_list[0]],
                                               connect='finite')
            # clear expired corrected data graph
            self.corrected_spectrum_line.setData(np.zeros(0), np.zeros(0))
        except Exception as e:
            message = f"Error in plot_initial_spectrum: {e}"
            self.show_error_dialog(self, message)

    # init -> set_ui -> set_parameters_tab -> set_spectrum/set_transmission -> select_file_dialog -> select_file_action
    # -> on_transmission_load
    def on_transmission_load(self, file_path):
        def there_is_spectrum():
            if "ok" in self.ui.spectrum_state.text() or "exceed" in self.ui.spectrum_text_output.text():
                return True
            return False

        try:
            # warning system update
            if there_is_spectrum():
                if self.spectrum_exceeds_transmission():
                    self.warning_system("transmission is exceeded by s") # update transmission status
                    self.warning_system("not ready to calc") # change calc status
                else:
                    self.warning_system("transmission loaded") # update transmission status
                    if "exceed" in self.ui.spectrum_text_output.text(): # update spectrum status
                        self.warning_system("spectrum exceeds no more")
                    self.warning_system("not calc yet") # change calc status
            else:
                self.warning_system("transmission loaded") # update file status
            # add custom option to transmission_preset
            if self.ui.transmission_preset.count() == len(self.window_transmission_presets_dict.keys()):
                self.ui.transmission_preset.insertItem(self.ui.transmission_preset.count(), "custom")
            # activate custom option in transmission_preset
            self.ui.transmission_preset.setCurrentIndex(self.ui.transmission_preset.count() - 1)
            # update settings
            settings.setValue("transmission_preset_index", len(self.window_transmission_presets_dict.keys()))
            settings.setValue("transmission_file_path", file_path)
        except Exception as e:
            message = f"Error in on_transmission_load: {e}"
            self.show_error_dialog(self, message)

    # init -> set_ui -> set_parameters_tab -> set_spectrum/set_transmission -> select_file_dialog -> select_file_action
    # -> on_spectrum_load/on_transmission_load -> spectrum_exceeds_transmission
    def spectrum_exceeds_transmission(self):
        try:
            # spectrum min & max
            min_s = np.min(self.spectrum_data[:, 0])
            max_s = np.max(self.spectrum_data[:, 0])
            # transmission min & max
            if self.ui.transmission_preset.currentText() == "custom":
                window_wavelength = self.transmission_data[:, 0]
            else:
                window_wavelength = \
                self.window_transmission_presets_dict[self.ui.transmission_preset.currentText()][0]
            min_t = np.min(window_wavelength)
            max_t = np.max(window_wavelength)
            # comparison
            if min_s < min_t or max_s > max_t:
                return True
            return False
        except Exception as e:
            message = f"Error in spectrum_transmission_verification: {e}"
            self.show_error_dialog(self, message)

    # init -> set_ui -> set_parameters_tab -> set_spectrum/set_transmission -> select_file_dialog -> select_file_action
    # -> on_no_data_in_file
    def on_no_data_in_file(self, action_type):
        try:
            # WS update
            if action_type == "spectrum loaded":
                self.warning_system("spectrum error")
                self.warning_system("not ready to calc")
            elif action_type == "transmission loaded":
                self.warning_system("transmission error")
                self.warning_system("not ready to calc")
        except Exception as e:
            message = f"Error in on_no_data_in_file: {e}"
            self.show_error_dialog(self, message)

    # init -> set_ui -> set_calc_tab
    def set_calc_tab(self):
        try:
            # connect calc btn & its style
            self.ui.correction_calc.clicked.connect(self.calculate_correction)
            self.ui.correction_calc.setStyleSheet(f"{self.bigger_btn_style}")
            # WS update
            self.warning_system("not ready to calc")
            # hide & connect on change function to graph_plot_options qcb
            self.ui.graph_plot_options.setVisible(False)
            self.ui.graph_plot_options.currentIndexChanged.connect(self.on_graph_plot_options_change)
            # set up the graph
            self.set_graph()
        except Exception as e:
            message = f"Error in set_calc_tab: {e}"
            self.show_error_dialog(self, message)

    # init -> set_ui -> set_calc_tab -> calculate_correction
    def calculate_correction(self):
        try:
            if "ok" in self.ui.correction_state.text() or "question" in self.ui.correction_state.text():
                # output result
                self.corrected_spectrum = copy.deepcopy(self.spectrum_data)
                # spectrum wavelength
                spectrum_wavelength = self.spectrum_data[:, 0]
                # transmission data
                if self.ui.transmission_preset.currentText() == "custom":
                    window_wavelength = self.transmission_data[:, 0]
                    window_transmission = self.transmission_data[:, 1]
                    self.window_material = self.ui.transmission_label.text()
                else:
                    window_wavelength = self.window_transmission_presets_dict[self.ui.transmission_preset.currentText()][0]
                    window_transmission = self.window_transmission_presets_dict[self.ui.transmission_preset.currentText()][1]
                    self.window_material = list(self.window_transmission_presets_dict.keys())[self.ui.transmission_preset.currentIndex()]
                # windows quantity
                windows_quantity = self.windows_quantity
                # correction type
                correction_type = self.correction_type
                # reflectance factor columns
                for reflectance_column in self.reflectance_columns_list:
                    # reflectance
                    spectrum_reflectance = self.spectrum_data[:, reflectance_column]
                    # its uncertainty if available
                    if reflectance_column + 1 != len(self.spectrum_data[0]):
                        spectrum_reflectance_uncertainty = self.spectrum_data[:, reflectance_column + 1]
                    else:
                        spectrum_reflectance_uncertainty = np.zeros(len(spectrum_reflectance))
                    # call the core class to calculate the correction
                    my_window_correction = CoreWindowCorrection(spectrum_wavelength, spectrum_reflectance,
                                                                spectrum_reflectance_uncertainty,
                                                                window_wavelength, window_transmission,
                                                                windows_quantity, correction_type)
                    my_window_correction.window_correction()
                    # OUTPUT
                    self.corrected_spectrum[:, reflectance_column] =  my_window_correction.class_getter_reflectance()
                    if reflectance_column + 1 != len(self.spectrum_data[0]):
                        self.corrected_spectrum[:, reflectance_column + 1] = my_window_correction.class_getter_reflectance_uncertainty()
                # state toggle
                self.warning_system("calc finished")
                self.warning_system("export ready")
                # plot
                self.on_graph_plot_options_change()
        except Exception as e:
            self.warning_system("calc error")
            self.warning_system("no calc")
            message = f"Error in calculate_correction: {e}"
            self.show_error_dialog(self, message)

    # init -> set_ui -> set_calc_tab -> on_graph_plot_options_change
    def on_graph_plot_options_change(self):
        try:
            # get the column to plot
            column_to_plot = self.reflectance_columns_list[self.ui.graph_plot_options.currentIndex()]
            # plot initial spectrum
            self.initial_spectrum_line.setData(self.spectrum_data[:, 0], self.spectrum_data[:, column_to_plot],
                                               connect='finite')
            # plot corrected spectrum if available
            if "ok" in self.ui.correction_state.text():
                self.corrected_spectrum_line.setData(self.spectrum_data[:, 0],
                                                     self.corrected_spectrum[:, column_to_plot],
                                                     connect='finite')
        except Exception as e:
            message = f"Error in on_graph_plot_options_change: {e}"
            self.show_error_dialog(self, message)

    # init -> set_ui -> set_calc_tab -> set_graph
    def set_graph(self):
        try:
            # antialias setup
            pg.setConfigOptions(antialias=True)
            # clear
            self.ui.graphWidget.clear()
            # bg color
            self.ui.graphWidget.setBackground("#FFFFFF")
            # auto-scale on the graph
            self.ui.graphWidget.enableAutoRange(True)
            # create plot item
            graph_plot = self.ui.graphWidget.getPlotItem()
            graph_plot.showGrid(x=True, y=True)
            graph_plot.setContentsMargins(30, 30, 30, 30)
            # add legend
            graph_plot.addLegend()
            # set up axes
            axe_style = {'color': '#000000', 'font-size': '13px'}
            self.ui.graphWidget.setLabel('bottom', "Wavelength", **axe_style)
            self.ui.graphWidget.setLabel('left', "Reflectance factor", **axe_style)
            # set lines: initial_spectrum_line & corrected_spectrum_line
            self.ui.graphWidget.addItem(self.initial_spectrum_line)
            self.ui.graphWidget.addItem(self.corrected_spectrum_line)
        except Exception as e:
            message = f"Error in set_graph: {e}"
            self.show_error_dialog(self, message)

    # init -> set_ui -> set_export_tab
    def set_export_tab(self):
        try:
            # connect & style export btn
            self.ui.export_btn.clicked.connect(self.export_dialog)
            self.ui.export_btn.setStyleSheet(f"{self.bigger_btn_style}")
            # WS update
            self.warning_system("nothing to export")
        except Exception as e:
            message = f"Error in set_export_tab: {e}"
            self.show_error_dialog(self, message)

    # init -> set_ui -> set_export_tab -> export_dialog
    def export_dialog(self):
        try:
            if "ok" in self.ui.export_state.text():
                # file name creation: original name stem + _wincor + original file extension
                save_file_name = Path(self.spectrum_path).stem + "_wincor" +  Path(self.spectrum_path).suffix
                # export path saved in settings if available
                if settings.value("export_dir") and os.path.isdir(settings.value("export_dir")):
                    save_file_name = os.path.join(settings.value("export_dir"), save_file_name)
                # get export path
                export_path, _ = QFileDialog.getSaveFileName(self, "Save File", save_file_name, "Text Files (*.txt)")
                # if export path
                if export_path:
                    settings.setValue("export_dir", os.path.dirname(export_path)) # update settings
                    self.export_action(export_path) # run export action
        except Exception as e:
            self.warning_system("export error")
            message = f"Error in export_dialog: {e}"
            self.show_error_dialog(self, message)

    # init -> set_ui -> set_export_tab -> export_dialog -> export_action
    def export_action(self, export_path):
        try:
            def get_header():
                header_str = ""
                correction_info = (f"Window reflection correction: "
                                   f"material: {self.window_material}, "
                                   f"quantity: {self.windows_quantity}, "
                                   f"type: {self.correction_type}.\n")
                if len(self.spectrum_file_header) > 0:
                    for index, line in enumerate(self.spectrum_file_header):
                        if len(self.reflectance_columns_list) == 1:
                            if self.reflectance_columns_list[0] != 1:
                                if index == 1:
                                    header_str += correction_info # raw files get info as the second line
                        else:
                            if index == 0:
                                header_str += correction_info # compilations get info as the very first line
                        header_str += line
                else:
                    header_str += correction_info # if no header -> info in the first line
                if len(self.reflectance_columns_list) == 1:
                    if self.reflectance_columns_list[0] == 1:
                        header_str += correction_info # simple files get info line after the header
                return header_str

            def create_export_str():
                data_to_str = ""
                # header
                data_to_str += get_header()
                # data
                for line in self.corrected_spectrum:
                    for column_number, column in enumerate(line):
                        data_to_str += f"{column:.{self.spectrum_file_accuracy[column_number]}f}"
                        if column_number != len(line) - 1:
                            data_to_str += self.spectrum_file_separator
                    data_to_str += "\n"
                return data_to_str

            if "ok" in self.ui.export_state.text():
                with open(export_path, 'w+') as file_output:
                    file_output.write(create_export_str())
                self.warning_system("export finished")
        except Exception as e:
            self.warning_system("export error")
            message = f"Error in export_action: {e}"
            self.show_error_dialog(self, message)

    # warning_system
    def warning_system(self, action_type):
        try:
            icon_container = self.tool_tip_dict[action_type][0] # get icon container
            text_output_container = self.tool_tip_dict[action_type][1] # get text output container
            icon_type = self.tool_tip_dict[action_type][2] # get icon type
            tool_tip_text = self.tool_tip_dict[action_type][3] # gt output text
            icon_container.setText(f"<html><img src='icons/{icon_type}.svg'></html>") # set icon container
            text_output_container.setText(tool_tip_text) # set output text
        except Exception as e:
            message = f"Error in warning_system: {e}"
            self.show_error_dialog(self, message)


# APP RUN
if __name__ == '__main__':
    app = QtWidgets.QApplication([])
    win = CorrectorMainW()
    win.setWindowFlags(Qt.WindowType.WindowMinimizeButtonHint | Qt.WindowType.WindowMaximizeButtonHint | Qt.WindowType.WindowCloseButtonHint)
    win.show()
    sys.exit(app.exec())
