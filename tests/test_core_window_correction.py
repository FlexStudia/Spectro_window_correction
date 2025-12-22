# coding: utf-8

# PACKAGES
import os
import sys
import inspect
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0, parentdir)

# MODULES
from list_compare import list_compare
from tools.data_pars import DataPars
from core_window_correction import CoreWindowCorrection
from presets.transmission_sapphire_window import SAPPHIRE_WINDOW_WAVELENGTHS, SAPPHIRE_WINDOW_TRANSMISSION


# full tests
def test_single_file_window_correction_simple_1_window():
    # INPUT
    file_path = "resources/!larderellite_32-80_A09-3_90K_c.txt"
    my_data_pars = DataPars(file_path)
    my_data_pars.file_pars_f()
    spectrum_to_correct = my_data_pars.file_body
    spectrum_wavelength = spectrum_to_correct[:, 0]
    spectrum_reflectance = spectrum_to_correct[:, 1]
    spectrum_reflectance_uncertainty = spectrum_to_correct[:, 2]
    window_wavelength = SAPPHIRE_WINDOW_WAVELENGTHS
    window_transmission = SAPPHIRE_WINDOW_TRANSMISSION
    windows_quantity = 1
    correction_type = "parasitic reflections"
    # Class EVOCATION
    my_window_correction = CoreWindowCorrection(spectrum_wavelength, spectrum_reflectance, spectrum_reflectance_uncertainty,
                                                window_wavelength, window_transmission,
                                                windows_quantity, correction_type)
    my_window_correction.window_correction()
    # OUTPUT
    corrected_reflectance = my_window_correction.class_getter_reflectance()
    corrected_reflectance_uncertainty = my_window_correction.class_getter_reflectance_uncertainty()
    # ASSERT
    file_path = "tests/files/core/simple_1_window.txt"
    my_data_pars = DataPars(file_path)
    my_data_pars.file_pars_f()
    expected_result = my_data_pars.file_body
    assert list_compare(corrected_reflectance, expected_result[:, 1], accuracy=10 ** -6)
    assert list_compare(corrected_reflectance_uncertainty, expected_result[:, 2], accuracy=10 ** -6)

def test_single_file_window_correction_simple_2_window():
    # INPUT
    file_path = "resources/!larderellite_32-80_A09-3_90K_c.txt"
    my_data_pars = DataPars(file_path)
    my_data_pars.file_pars_f()
    spectrum_to_correct = my_data_pars.file_body
    spectrum_wavelength = spectrum_to_correct[:, 0]
    spectrum_reflectance = spectrum_to_correct[:, 1]
    spectrum_reflectance_uncertainty = spectrum_to_correct[:, 2]
    window_wavelength = SAPPHIRE_WINDOW_WAVELENGTHS
    window_transmission = SAPPHIRE_WINDOW_TRANSMISSION
    windows_quantity = 2
    correction_type = "parasitic reflections"
    # Class EVOCATION
    my_window_correction = CoreWindowCorrection(spectrum_wavelength, spectrum_reflectance, spectrum_reflectance_uncertainty,
                                                window_wavelength, window_transmission,
                                                windows_quantity, correction_type)
    my_window_correction.window_correction()
    # OUTPUT
    corrected_reflectance = my_window_correction.class_getter_reflectance()
    corrected_reflectance_uncertainty = my_window_correction.class_getter_reflectance_uncertainty()
    # ASSERT
    file_path = "tests/files/core/simple_2_window.txt"
    my_data_pars = DataPars(file_path)
    my_data_pars.file_pars_f()
    expected_result = my_data_pars.file_body
    assert list_compare(corrected_reflectance, expected_result[:, 1], accuracy=10 ** -6)
    assert list_compare(corrected_reflectance_uncertainty, expected_result[:, 2], accuracy=10 ** -6)

def test_single_file_window_correction_extended_1_window():
    # INPUT
    file_path = "resources/!larderellite_32-80_A09-3_90K_c.txt"
    my_data_pars = DataPars(file_path)
    my_data_pars.file_pars_f()
    spectrum_to_correct = my_data_pars.file_body
    spectrum_wavelength = spectrum_to_correct[:, 0]
    spectrum_reflectance = spectrum_to_correct[:, 1]
    spectrum_reflectance_uncertainty = spectrum_to_correct[:, 2]
    window_wavelength = SAPPHIRE_WINDOW_WAVELENGTHS
    window_transmission = SAPPHIRE_WINDOW_TRANSMISSION
    windows_quantity = 1
    correction_type = "extended correction"
    # Class EVOCATION
    my_window_correction = CoreWindowCorrection(spectrum_wavelength, spectrum_reflectance, spectrum_reflectance_uncertainty,
                                                window_wavelength, window_transmission,
                                                windows_quantity, correction_type)
    my_window_correction.window_correction()
    # OUTPUT
    corrected_reflectance = my_window_correction.class_getter_reflectance()
    corrected_reflectance_uncertainty = my_window_correction.class_getter_reflectance_uncertainty()
    # ASSERT
    file_path = "tests/files/core/extended_1_window.txt"
    my_data_pars = DataPars(file_path)
    my_data_pars.file_pars_f()
    expected_result = my_data_pars.file_body
    assert list_compare(corrected_reflectance, expected_result[:, 1], accuracy=10 ** -6)
    assert list_compare(corrected_reflectance_uncertainty, expected_result[:, 2], accuracy=10 ** -6)

def test_single_file_window_correction_extended_2_window():
    # INPUT
    file_path = "resources/!larderellite_32-80_A09-3_90K_c.txt"
    my_data_pars = DataPars(file_path)
    my_data_pars.file_pars_f()
    spectrum_to_correct = my_data_pars.file_body
    spectrum_wavelength = spectrum_to_correct[:, 0]
    spectrum_reflectance = spectrum_to_correct[:, 1]
    spectrum_reflectance_uncertainty = spectrum_to_correct[:, 2]
    window_wavelength = SAPPHIRE_WINDOW_WAVELENGTHS
    window_transmission = SAPPHIRE_WINDOW_TRANSMISSION
    windows_quantity = 2
    correction_type = "extended correction"
    # Class EVOCATION
    my_window_correction = CoreWindowCorrection(spectrum_wavelength, spectrum_reflectance, spectrum_reflectance_uncertainty,
                                                window_wavelength, window_transmission,
                                                windows_quantity, correction_type)
    my_window_correction.window_correction()
    # OUTPUT
    corrected_reflectance = my_window_correction.class_getter_reflectance()
    corrected_reflectance_uncertainty = my_window_correction.class_getter_reflectance_uncertainty()
    # ASSERT
    file_path = "tests/files/core/extended_2_window.txt"
    my_data_pars = DataPars(file_path)
    my_data_pars.file_pars_f()
    expected_result = my_data_pars.file_body
    assert list_compare(corrected_reflectance, expected_result[:, 1], accuracy=10 ** -6)
    assert list_compare(corrected_reflectance_uncertainty, expected_result[:, 2], accuracy=10 ** -6)

def file_end():
    pass
