# coding: utf-8

# PACKAGES
import filecmp
import os
import sys
import inspect
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0, parentdir)

# MODULES
from main import *
from tools.data_pars import DataPars

# test QApp
test_app = QApplication(sys.argv)


# TESTS
# warning system
def test_warning_system_no_problem_max_test():
    def assert_verif(respond_key):
        icon_respond = win.tool_tip_dict[respond_key][2] in win.tool_tip_dict[respond_key][0].text()
        text_output_respond = win.tool_tip_dict[respond_key][1].text() == win.tool_tip_dict[respond_key][3]
        if icon_respond and text_output_respond:
            return True
        else:
            print(f"icon: {win.tool_tip_dict[respond_key][0].text()}")
            print(f"text_output: {win.tool_tip_dict[respond_key][1].text()}")
            return False
    # inputs
    spectrum_file_path = "tests/files/sources/simple.txt"
    transmission_file_path = "resources/transmission_sapphire_window.txt"
    windows_quantity_index = 1
    correction_type_index = 1
    win = CorrectorMainW()
    # parameters set
    win.ui.transmission_preset.setCurrentIndex(0)
    win.ui.windows_quantity.setCurrentIndex(0)
    win.ui.correction_type.setCurrentIndex(0)
    # on load
    assert assert_verif("spectrum empty")
    assert assert_verif("transmission from preset")
    assert assert_verif("not ready to calc")
    assert assert_verif("nothing to export")
    # spectrum load error
    win.select_file_action("not a path at all", "spectrum loaded")
    assert assert_verif("spectrum empty")
    assert assert_verif("transmission from preset") or assert_verif("transmission loaded")
    assert assert_verif("not ready to calc")
    assert assert_verif("nothing to export")
    # spectrum load
    win.select_file_action(spectrum_file_path, "spectrum loaded")
    assert assert_verif("spectrum loaded")
    assert assert_verif("transmission from preset")
    assert assert_verif("not calc yet")
    assert assert_verif("nothing to export")
    # transmission load error
    win.select_file_action("not a path at all", "transmission loaded")
    assert assert_verif("spectrum loaded")
    assert assert_verif("transmission from preset")
    assert assert_verif("not calc yet")
    assert assert_verif("nothing to export")
    # transmission load
    win.select_file_action(transmission_file_path, "transmission loaded")
    assert assert_verif("spectrum loaded")
    assert assert_verif("transmission loaded")
    assert assert_verif("not calc yet")
    assert assert_verif("nothing to export")
    # calculate correction
    win.calculate_correction()
    assert assert_verif("spectrum loaded")
    assert assert_verif("transmission loaded")
    assert assert_verif("calc finished")
    assert assert_verif("export ready")
    # export
    win.export_action("temp_file.txt")
    assert assert_verif("spectrum loaded")
    assert assert_verif("transmission loaded")
    assert assert_verif("calc finished")
    assert assert_verif("export finished")
    os.remove("temp_file.txt")
    # parameters change: windows quantity
    win.ui.windows_quantity.setCurrentIndex(windows_quantity_index)
    assert assert_verif("spectrum loaded")
    assert assert_verif("transmission loaded")
    assert assert_verif("calc expired")
    assert assert_verif("export expired")
    win.calculate_correction()
    assert assert_verif("spectrum loaded")
    assert assert_verif("transmission loaded")
    assert assert_verif("calc finished")
    assert assert_verif("export ready")
    # parameters change: correction type
    win.ui.correction_type.setCurrentIndex(correction_type_index)
    assert assert_verif("spectrum loaded")
    assert assert_verif("transmission loaded")
    assert assert_verif("calc expired")
    assert assert_verif("export expired")
    win.calculate_correction()
    assert assert_verif("spectrum loaded")
    assert assert_verif("transmission loaded")
    assert assert_verif("calc finished")
    assert assert_verif("export ready")
    win.close()


# full tests
# 3 columns simple files
def test_3_col_file_simple_1_window():
    # inputs
    spectrum_file_path = "tests/files/sources/simple.txt"
    transmission_preset_index = 0 # sapphire windows preset
    windows_quantity_index = 0 # 1
    correction_type_index = 0 # "parasitic reflections"
    # app run
    win = CorrectorMainW()
    # transmission preset
    win.ui.transmission_preset.setCurrentIndex(transmission_preset_index)
    # spectrum set & verif
    assert win.ui.spectrum_label.text() == "no file selected"
    assert "question" in win.ui.spectrum_state.text()
    assert win.ui.spectrum_text_output.text() == "Load a spectrum file to correct"
    win.select_file_action(spectrum_file_path, "spectrum loaded")
    assert win.ui.spectrum_label.text() == "simple.txt"
    assert "ok" in win.ui.spectrum_state.text()
    assert win.ui.spectrum_text_output.text() == "The spectrum file has been successfully loaded"
    # windows_quantity & correction_type set
    win.ui.windows_quantity.setCurrentIndex(0)
    win.ui.windows_quantity.setCurrentIndex(1)
    win.ui.correction_type.setCurrentIndex(0)
    win.ui.correction_type.setCurrentIndex(1)
    win.ui.windows_quantity.setCurrentIndex(windows_quantity_index)
    win.ui.correction_type.setCurrentIndex(correction_type_index)
    # calc & state verif
    win.calculate_correction()
    assert win.ui.correction_text_output.text() == "The calculation has been successfully completed!"
    # export
    export_file_path = "tests/files/main/export.txt"
    win.export_action(export_file_path)
    # expected result load & assert
    expected_result_path = "tests/files/main/3_col_simple_1_window.txt"
    assert filecmp.cmp(expected_result_path, export_file_path, shallow=False)
    win.close()

def test_3_col_file_simple_2_window():
    # inputs
    spectrum_file_path = "tests/files/sources/simple.txt"
    transmission_preset_index = 0  # sapphire windows preset
    windows_quantity_index = 1  # 2
    correction_type_index = 0  # "parasitic reflections"
    # app run
    win = CorrectorMainW()
    # transmission set
    win.ui.transmission_preset.setCurrentIndex(transmission_preset_index)
    # spectrum set
    win.select_file_action(spectrum_file_path, "spectrum loaded")
    # windows_quantity & correction_type set
    win.ui.windows_quantity.setCurrentIndex(0)
    win.ui.windows_quantity.setCurrentIndex(1)
    win.ui.correction_type.setCurrentIndex(0)
    win.ui.correction_type.setCurrentIndex(1)
    win.ui.windows_quantity.setCurrentIndex(windows_quantity_index)
    win.ui.correction_type.setCurrentIndex(correction_type_index)
    # calc & state verif
    win.calculate_correction()
    # export
    export_file_path = "tests/files/main/export.txt"
    win.export_action(export_file_path)
    # expected result load & assert
    expected_result_path = "tests/files/main/3_col_simple_2_window.txt"
    assert filecmp.cmp(expected_result_path, export_file_path, shallow=False)
    win.close()

def test_3_col_file_extended_1_window():
    # inputs
    spectrum_file_path = "tests/files/sources/simple.txt"
    transmission_preset_index = 0  # sapphire windows preset
    windows_quantity_index = 0  # 1
    correction_type_index = 1  # "extended correction"
    # app run
    win = CorrectorMainW()
    # spectrum set
    win.select_file_action(spectrum_file_path, "spectrum loaded")
    # transmission set
    win.ui.transmission_preset.setCurrentIndex(transmission_preset_index)
    # windows_quantity & correction_type set
    win.ui.windows_quantity.setCurrentIndex(0)
    win.ui.windows_quantity.setCurrentIndex(1)
    win.ui.correction_type.setCurrentIndex(0)
    win.ui.correction_type.setCurrentIndex(1)
    win.ui.windows_quantity.setCurrentIndex(windows_quantity_index)
    win.ui.correction_type.setCurrentIndex(correction_type_index)
    # calc & state verif
    win.calculate_correction()
    # export
    export_file_path = "tests/files/main/export.txt"
    win.export_action(export_file_path)
    # expected result load & assert
    expected_result_path = "tests/files/main/3_col_extended_1_window.txt"
    assert filecmp.cmp(expected_result_path, export_file_path, shallow=False)
    win.close()

def test_3_col_file_extended_2_window():
    # inputs
    spectrum_file_path = "tests/files/sources/simple.txt"
    transmission_preset_index = 0  # sapphire windows preset
    windows_quantity_index = 1  # 2
    correction_type_index = 1  # "extended correction"
    # app run
    win = CorrectorMainW()
    # spectrum set
    win.select_file_action(spectrum_file_path, "spectrum loaded")
    # transmission set
    win.ui.transmission_preset.setCurrentIndex(transmission_preset_index)
    # windows_quantity & correction_type set
    win.ui.windows_quantity.setCurrentIndex(0)
    win.ui.windows_quantity.setCurrentIndex(1)
    win.ui.correction_type.setCurrentIndex(0)
    win.ui.correction_type.setCurrentIndex(1)
    win.ui.windows_quantity.setCurrentIndex(windows_quantity_index)
    win.ui.correction_type.setCurrentIndex(correction_type_index)
    # calc & state verif
    win.calculate_correction()
    # export
    export_file_path = "tests/files/main/export.txt"
    win.export_action(export_file_path)
    # expected result load & assert
    expected_result_path = "tests/files/main/3_col_extended_2_window.txt"
    assert filecmp.cmp(expected_result_path, export_file_path, shallow=False)
    win.close()

def test_2_col_file_simple_2_window():
    # inputs
    spectrum_file_path = "tests/files/sources/simple_2_col.txt"
    transmission_preset_index = 0  # sapphire windows preset
    windows_quantity_index = 1  # 2
    correction_type_index = 0  # "parasitic reflections"
    # app run
    win = CorrectorMainW()
    # spectrum set
    win.select_file_action(spectrum_file_path, "spectrum loaded")
    # transmission set
    win.ui.transmission_preset.setCurrentIndex(transmission_preset_index)
    # windows_quantity & correction_type set
    win.ui.windows_quantity.setCurrentIndex(0)
    win.ui.windows_quantity.setCurrentIndex(1)
    win.ui.correction_type.setCurrentIndex(0)
    win.ui.correction_type.setCurrentIndex(1)
    win.ui.windows_quantity.setCurrentIndex(windows_quantity_index)
    win.ui.correction_type.setCurrentIndex(correction_type_index)
    # calc & state verif
    win.calculate_correction()
    # export
    export_file_path = "tests/files/main/export.txt"
    win.export_action(export_file_path)
    # expected result load & assert
    expected_result_path = "tests/files/main/2_col_simple_2_window.txt"
    assert filecmp.cmp(expected_result_path, export_file_path, shallow=False)
    win.close()


# raw files
def test_raw_file_simple_1_window():
    # inputs
    spectrum_file_path = "tests/files/sources/raw.txt"
    transmission_preset_index = 0  # sapphire windows preset
    windows_quantity_index = 0 # 1
    correction_type_index = 0 # "parasitic reflections"
    # app run
    win = CorrectorMainW()
    # spectrum set
    win.select_file_action(spectrum_file_path, "spectrum loaded")
    # transmission set
    win.ui.transmission_preset.setCurrentIndex(transmission_preset_index)
    # windows_quantity & correction_type set
    win.ui.windows_quantity.setCurrentIndex(0)
    win.ui.windows_quantity.setCurrentIndex(1)
    win.ui.correction_type.setCurrentIndex(0)
    win.ui.correction_type.setCurrentIndex(1)
    win.ui.windows_quantity.setCurrentIndex(windows_quantity_index)
    win.ui.correction_type.setCurrentIndex(correction_type_index)
    # calc & state verif
    win.calculate_correction()
    # export
    export_file_path = "tests/files/main/export.txt"
    win.export_action(export_file_path)
    # expected result load & assert
    expected_result_path = "tests/files/main/raw_simple_1_window.txt"
    assert filecmp.cmp(expected_result_path, export_file_path, shallow=False)
    win.close()

def test_raw_file_simple_2_window():
    # inputs
    spectrum_file_path = "tests/files/sources/raw.txt"
    transmission_preset_index = 0  # sapphire windows preset
    windows_quantity_index = 1  # 2
    correction_type_index = 0  # "parasitic reflections"
    # app run
    win = CorrectorMainW()
    # spectrum set
    win.select_file_action(spectrum_file_path, "spectrum loaded")
    # transmission set
    win.ui.transmission_preset.setCurrentIndex(transmission_preset_index)
    # windows_quantity & correction_type set
    win.ui.windows_quantity.setCurrentIndex(0)
    win.ui.windows_quantity.setCurrentIndex(1)
    win.ui.correction_type.setCurrentIndex(0)
    win.ui.correction_type.setCurrentIndex(1)
    win.ui.windows_quantity.setCurrentIndex(windows_quantity_index)
    win.ui.correction_type.setCurrentIndex(correction_type_index)
    # calc & state verif
    win.calculate_correction()
    # export
    export_file_path = "tests/files/main/export.txt"
    win.export_action(export_file_path)
    # expected result load & assert
    expected_result_path = "tests/files/main/raw_simple_2_window.txt"
    assert filecmp.cmp(expected_result_path, export_file_path, shallow=False)
    win.close()

def test_raw_file_extended_1_window():
    # inputs
    spectrum_file_path = "tests/files/sources/raw.txt"
    transmission_preset_index = 0  # sapphire windows preset
    windows_quantity_index = 0  # 1
    correction_type_index = 1  # "extended correction"
    # app run
    win = CorrectorMainW()
    # spectrum set
    win.select_file_action(spectrum_file_path, "spectrum loaded")
    # transmission set
    win.ui.transmission_preset.setCurrentIndex(transmission_preset_index)
    # windows_quantity & correction_type set
    win.ui.windows_quantity.setCurrentIndex(0)
    win.ui.windows_quantity.setCurrentIndex(1)
    win.ui.correction_type.setCurrentIndex(0)
    win.ui.correction_type.setCurrentIndex(1)
    win.ui.windows_quantity.setCurrentIndex(windows_quantity_index)
    win.ui.correction_type.setCurrentIndex(correction_type_index)
    # calc & state verif
    win.calculate_correction()
    # export
    export_file_path = "tests/files/main/export.txt"
    win.export_action(export_file_path)
    # expected result load & assert
    expected_result_path = "tests/files/main/raw_extended_1_window.txt"
    assert filecmp.cmp(expected_result_path, export_file_path, shallow=False)
    win.close()

def test_raw_file_extended_2_window():
    # inputs
    spectrum_file_path = "tests/files/sources/raw.txt"
    transmission_preset_index = 0  # sapphire windows preset
    windows_quantity_index = 1  # 2
    correction_type_index = 1  # "extended correction"
    # app run
    win = CorrectorMainW()
    # spectrum set
    win.select_file_action(spectrum_file_path, "spectrum loaded")
    # transmission set
    win.ui.transmission_preset.setCurrentIndex(transmission_preset_index)
    # windows_quantity & correction_type set
    win.ui.windows_quantity.setCurrentIndex(0)
    win.ui.windows_quantity.setCurrentIndex(1)
    win.ui.correction_type.setCurrentIndex(0)
    win.ui.correction_type.setCurrentIndex(1)
    win.ui.windows_quantity.setCurrentIndex(windows_quantity_index)
    win.ui.correction_type.setCurrentIndex(correction_type_index)
    # calc & state verif
    win.calculate_correction()
    # export
    export_file_path = "tests/files/main/export.txt"
    win.export_action(export_file_path)
    # expected result load & assert
    expected_result_path = "tests/files/main/raw_extended_2_window.txt"
    assert filecmp.cmp(expected_result_path, export_file_path, shallow=False)
    win.close()

def test_raw_12_col_file_extended_1_window():
    # inputs
    spectrum_file_path = "tests/files/sources/raw_12_col.txt"
    transmission_preset_index = 0  # sapphire windows preset
    windows_quantity_index = 0  # 1
    correction_type_index = 1  # "extended correction"
    # app run
    win = CorrectorMainW()
    # spectrum set
    win.select_file_action(spectrum_file_path, "spectrum loaded")
    # transmission set
    win.ui.transmission_preset.setCurrentIndex(transmission_preset_index)
    # windows_quantity & correction_type set
    win.ui.windows_quantity.setCurrentIndex(0)
    win.ui.windows_quantity.setCurrentIndex(1)
    win.ui.correction_type.setCurrentIndex(0)
    win.ui.correction_type.setCurrentIndex(1)
    win.ui.windows_quantity.setCurrentIndex(windows_quantity_index)
    win.ui.correction_type.setCurrentIndex(correction_type_index)
    # calc & state verif
    win.calculate_correction()
    # export
    export_file_path = "tests/files/main/export.txt"
    win.export_action(export_file_path)
    # expected result load & assert
    expected_result_path = ("tests/files/main/raw_12_col_extended_1_window.txt")
    assert filecmp.cmp(expected_result_path, export_file_path, shallow=False)
    win.close()

def test_raw_11_col_file_simple_1_window():
    # inputs
    spectrum_file_path = "tests/files/sources/raw_11_col.txt"
    transmission_preset_index = 0  # sapphire windows preset
    windows_quantity_index = 0 # 1
    correction_type_index = 0 # "parasitic reflections"
    # app run
    win = CorrectorMainW()
    # spectrum set
    win.select_file_action(spectrum_file_path, "spectrum loaded")
    # transmission set
    win.ui.transmission_preset.setCurrentIndex(transmission_preset_index)
    # windows_quantity & correction_type set
    win.ui.windows_quantity.setCurrentIndex(0)
    win.ui.windows_quantity.setCurrentIndex(1)
    win.ui.correction_type.setCurrentIndex(0)
    win.ui.correction_type.setCurrentIndex(1)
    win.ui.windows_quantity.setCurrentIndex(windows_quantity_index)
    win.ui.correction_type.setCurrentIndex(correction_type_index)
    # calc & state verif
    win.calculate_correction()
    # export
    export_file_path = "tests/files/main/export.txt"
    win.export_action(export_file_path)
    # expected result load & assert
    expected_result_path = "tests/files/main/raw_11_col_simple_1_window.txt"
    assert filecmp.cmp(expected_result_path, export_file_path, shallow=False)
    win.close()


# compilation files: geo - BRDF
def test_geo_file_simple_1_window():
    # inputs
    spectrum_file_path = "tests/files/sources/geo.txt"
    transmission_preset_index = 0  # sapphire windows preset
    windows_quantity_index = 0 # 1
    correction_type_index = 0 # "parasitic reflections"
    # app run
    win = CorrectorMainW()
    # spectrum set
    win.select_file_action(spectrum_file_path, "spectrum loaded")
    # transmission set
    win.ui.transmission_preset.setCurrentIndex(transmission_preset_index)
    # windows_quantity & correction_type set
    win.ui.windows_quantity.setCurrentIndex(0)
    win.ui.windows_quantity.setCurrentIndex(1)
    win.ui.correction_type.setCurrentIndex(0)
    win.ui.correction_type.setCurrentIndex(1)
    win.ui.windows_quantity.setCurrentIndex(windows_quantity_index)
    win.ui.correction_type.setCurrentIndex(correction_type_index)
    # calc & state verif
    win.calculate_correction()
    # export
    export_file_path = "tests/files/main/export.txt"
    win.export_action(export_file_path)
    # expected result load & assert
    expected_result_path = "tests/files/main/geo_simple_1_window.txt"
    assert filecmp.cmp(expected_result_path, export_file_path, shallow=False)
    win.close()

def test_geo_file_simple_2_window():
    # inputs
    spectrum_file_path = "tests/files/sources/geo.txt"
    transmission_preset_index = 0  # sapphire windows preset
    windows_quantity_index = 1  # 2
    correction_type_index = 0  # "parasitic reflections"
    # app run
    win = CorrectorMainW()
    # spectrum set
    win.select_file_action(spectrum_file_path, "spectrum loaded")
    # transmission set
    win.ui.transmission_preset.setCurrentIndex(transmission_preset_index)
    # windows_quantity & correction_type set
    win.ui.windows_quantity.setCurrentIndex(0)
    win.ui.windows_quantity.setCurrentIndex(1)
    win.ui.correction_type.setCurrentIndex(0)
    win.ui.correction_type.setCurrentIndex(1)
    win.ui.windows_quantity.setCurrentIndex(windows_quantity_index)
    win.ui.correction_type.setCurrentIndex(correction_type_index)
    # calc & state verif
    win.calculate_correction()
    # export
    export_file_path = "tests/files/main/export.txt"
    win.export_action(export_file_path)
    # expected result load & assert
    expected_result_path = "tests/files/main/geo_simple_2_window.txt"
    assert filecmp.cmp(expected_result_path, export_file_path, shallow=False)
    win.close()

def test_geo_file_extended_1_window():
    # inputs
    spectrum_file_path = "tests/files/sources/geo.txt"
    transmission_preset_index = 0  # sapphire windows preset
    windows_quantity_index = 0  # 1
    correction_type_index = 1  # "extended correction"
    # app run
    win = CorrectorMainW()
    # spectrum set
    win.select_file_action(spectrum_file_path, "spectrum loaded")
    # transmission set
    win.ui.transmission_preset.setCurrentIndex(transmission_preset_index)
    # windows_quantity & correction_type set
    win.ui.windows_quantity.setCurrentIndex(0)
    win.ui.windows_quantity.setCurrentIndex(1)
    win.ui.correction_type.setCurrentIndex(0)
    win.ui.correction_type.setCurrentIndex(1)
    win.ui.windows_quantity.setCurrentIndex(windows_quantity_index)
    win.ui.correction_type.setCurrentIndex(correction_type_index)
    # calc & state verif
    win.calculate_correction()
    # export
    export_file_path = "tests/files/main/export.txt"
    win.export_action(export_file_path)
    # expected result load & assert
    expected_result_path = "tests/files/main/geo_extended_1_window.txt"
    assert filecmp.cmp(expected_result_path, export_file_path, shallow=False)
    win.close()

def test_geo_file_extended_2_window():
    # inputs
    spectrum_file_path = "tests/files/sources/geo.txt"
    transmission_preset_index = 0  # sapphire windows preset
    windows_quantity_index = 1  # 2
    correction_type_index = 1  # "extended correction"
    # app run
    win = CorrectorMainW()
    # spectrum set
    win.select_file_action(spectrum_file_path, "spectrum loaded")
    # transmission set
    win.ui.transmission_preset.setCurrentIndex(transmission_preset_index)
    # windows_quantity & correction_type set
    win.ui.windows_quantity.setCurrentIndex(0)
    win.ui.windows_quantity.setCurrentIndex(1)
    win.ui.correction_type.setCurrentIndex(0)
    win.ui.correction_type.setCurrentIndex(1)
    win.ui.windows_quantity.setCurrentIndex(windows_quantity_index)
    win.ui.correction_type.setCurrentIndex(correction_type_index)
    # calc & state verif
    win.calculate_correction()
    # export
    export_file_path = "tests/files/main/export.txt"
    win.export_action(export_file_path)
    # expected result load & assert
    expected_result_path = "tests/files/main/geo_extended_2_window.txt"
    assert filecmp.cmp(expected_result_path, export_file_path, shallow=False)
    win.close()


# compilation files: temp - temperature
def test_temp_file_simple_1_window():
    # inputs
    spectrum_file_path = "tests/files/sources/temp.txt"
    transmission_preset_index = 0  # sapphire windows preset
    windows_quantity_index = 0 # 1
    correction_type_index = 0 # "parasitic reflections"
    # app run
    win = CorrectorMainW()
    # spectrum set
    win.select_file_action(spectrum_file_path, "spectrum loaded")
    # transmission set
    win.ui.transmission_preset.setCurrentIndex(transmission_preset_index)
    # windows_quantity & correction_type set
    win.ui.windows_quantity.setCurrentIndex(0)
    win.ui.windows_quantity.setCurrentIndex(1)
    win.ui.correction_type.setCurrentIndex(0)
    win.ui.correction_type.setCurrentIndex(1)
    win.ui.windows_quantity.setCurrentIndex(windows_quantity_index)
    win.ui.correction_type.setCurrentIndex(correction_type_index)
    # calc & state verif
    win.calculate_correction()
    # export
    export_file_path = "tests/files/main/export.txt"
    win.export_action(export_file_path)
    # expected result load & assert
    expected_result_path = "tests/files/main/temp_simple_1_window.txt"
    assert filecmp.cmp(expected_result_path, export_file_path, shallow=False)
    win.close()

def test_temp_file_simple_2_window():
    # inputs
    spectrum_file_path = "tests/files/sources/temp.txt"
    transmission_preset_index = 0  # sapphire windows preset
    windows_quantity_index = 1  # 2
    correction_type_index = 0  # "parasitic reflections"
    # app run
    win = CorrectorMainW()
    # spectrum set
    win.select_file_action(spectrum_file_path, "spectrum loaded")
    # transmission set
    win.ui.transmission_preset.setCurrentIndex(transmission_preset_index)
    # windows_quantity & correction_type set
    win.ui.windows_quantity.setCurrentIndex(0)
    win.ui.windows_quantity.setCurrentIndex(1)
    win.ui.correction_type.setCurrentIndex(0)
    win.ui.correction_type.setCurrentIndex(1)
    win.ui.windows_quantity.setCurrentIndex(windows_quantity_index)
    win.ui.correction_type.setCurrentIndex(correction_type_index)
    # calc & state verif
    win.calculate_correction()
    # export
    export_file_path = "tests/files/main/export.txt"
    win.export_action(export_file_path)
    # expected result load & assert
    expected_result_path = "tests/files/main/temp_simple_2_window.txt"
    assert filecmp.cmp(expected_result_path, export_file_path, shallow=False)
    win.close()

def test_temp_file_extended_1_window():
    # inputs
    spectrum_file_path = "tests/files/sources/temp.txt"
    transmission_preset_index = 0  # sapphire windows preset
    windows_quantity_index = 0  # 1
    correction_type_index = 1  # "extended correction"
    # app run
    win = CorrectorMainW()
    # spectrum set
    win.select_file_action(spectrum_file_path, "spectrum loaded")
    # transmission set
    win.ui.transmission_preset.setCurrentIndex(transmission_preset_index)
    # windows_quantity & correction_type set
    win.ui.windows_quantity.setCurrentIndex(0)
    win.ui.windows_quantity.setCurrentIndex(1)
    win.ui.correction_type.setCurrentIndex(0)
    win.ui.correction_type.setCurrentIndex(1)
    win.ui.windows_quantity.setCurrentIndex(windows_quantity_index)
    win.ui.correction_type.setCurrentIndex(correction_type_index)
    # calc & state verif
    win.calculate_correction()
    # export
    export_file_path = "tests/files/main/export.txt"
    win.export_action(export_file_path)
    # expected result load & assert
    expected_result_path = "tests/files/main/temp_extended_1_window.txt"
    assert filecmp.cmp(expected_result_path, export_file_path, shallow=False)
    win.close()

def test_temp_file_extended_2_window():
    # inputs
    spectrum_file_path = "tests/files/sources/temp.txt"
    transmission_preset_index = 0  # sapphire windows preset
    windows_quantity_index = 1  # 2
    correction_type_index = 1  # "extended correction"
    # app run
    win = CorrectorMainW()
    # spectrum set
    win.select_file_action(spectrum_file_path, "spectrum loaded")
    # transmission set
    win.ui.transmission_preset.setCurrentIndex(transmission_preset_index)
    # windows_quantity & correction_type set
    win.ui.windows_quantity.setCurrentIndex(0)
    win.ui.windows_quantity.setCurrentIndex(1)
    win.ui.correction_type.setCurrentIndex(0)
    win.ui.correction_type.setCurrentIndex(1)
    win.ui.windows_quantity.setCurrentIndex(windows_quantity_index)
    win.ui.correction_type.setCurrentIndex(correction_type_index)
    # calc & state verif
    win.calculate_correction()
    # export
    export_file_path = "tests/files/main/export.txt"
    win.export_action(export_file_path)
    # expected result load & assert
    expected_result_path = "tests/files/main/temp_extended_2_window.txt"
    assert filecmp.cmp(expected_result_path, export_file_path, shallow=False)
    win.close()

def file_end():
    pass
