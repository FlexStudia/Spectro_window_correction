# coding: utf-8

# PACKAGES
import numpy as np

# MODULES
from tools.data_pars import DataPars # for demo_f only
from presets.transmission_sapphire_window import SAPPHIRE_WINDOW_WAVELENGTHS, SAPPHIRE_WINDOW_TRANSMISSION # preset for demo_f only


class CoreWindowCorrection:
    def __init__(self, spectrum_wavelength, spectrum_reflectance, spectrum_reflectance_uncertainty,
                 window_material_wavelengths, window_material_transmission, windows_quantity, correction_type):
        self.class_setter(spectrum_wavelength, spectrum_reflectance, spectrum_reflectance_uncertainty, window_material_wavelengths, window_material_transmission, windows_quantity, correction_type)
        self.globals()

    # class setter
    def class_setter(self, spectrum_wavelength, spectrum_reflectance, spectrum_reflectance_uncertainty,
                     window_material_wavelengths, window_material_transmission, windows_quantity, correction_type):
        self.spectrum_wavelength = spectrum_wavelength
        self.spectrum_reflectance = spectrum_reflectance
        self.spectrum_reflectance_uncertainty = spectrum_reflectance_uncertainty
        self.window_material_wavelengths = window_material_wavelengths
        self.window_material_transmission = window_material_transmission
        self.windows_quantity = windows_quantity
        self.correction_type = correction_type

    # class globals
    def globals(self):
        # OUTPUT
        self.corrected_reflectance = np.zeros(len(self.spectrum_wavelength))
        self.corrected_reflectance_uncertainty = np.zeros(len(self.spectrum_wavelength))

    # class getters
    def class_getter_reflectance(self):
        return self.corrected_reflectance

    def class_getter_reflectance_uncertainty(self):
        return self.corrected_reflectance_uncertainty

    # main function window_correction
    def window_correction(self):
        try:
            for index, wavelength in enumerate(self.spectrum_wavelength):
                transmission = np.interp(wavelength, self.window_material_wavelengths, self.window_material_transmission)
                polynomial_roots = self.get_polynomial_roots(self.spectrum_reflectance[index], transmission)
                self.corrected_reflectance[index] = self.get_corrected_reflectance_value(polynomial_roots)
                self.corrected_reflectance_uncertainty[index] = self.corrected_reflectance[index] * self.spectrum_reflectance_uncertainty[index] / self.spectrum_reflectance[index]
        except Exception as e:
            raise Exception(f"Critical error in CoreWindowCorrection::window_correction: {str(e)}") from e

    # window_correction -> get_polynomial_roots
    def get_polynomial_roots(self, R0, T):
        try:
            coefficients = [-R0]
            for i in range(1, 10):
                coefficients.append(T ** (2 * self.windows_quantity) * ((1 - T) ** (i - 1)))
            polynom = np.polynomial.Polynomial(coefficients)
            root = polynom.roots()
            return root
        except Exception as e:
            raise Exception(f"Critical error in CoreWindowCorrection::get_polynomial_roots: {str(e)}") from e

    # window_correction -> get_corrected_reflectance_value
    def get_corrected_reflectance_value(self, roots):
        def get_real_roots(roots):
            for root in roots:
                if root.imag == 0:
                    return root.real
            return np.nan

        try:
            real_root = get_real_roots(roots)
            if self.correction_type == "parasitic reflections":
                return real_root
            else:
                return real_root / (1.0245 - real_root * 0.10612)
        except Exception as e:
            raise Exception(f"Critical error in CoreWindowCorrection::get_corrected_reflectance_value: {str(e)}") from e


def demo():
    # INPUT
    # spectrum
    file_path = "resources/!larderellite_32-80_A09-3_90K_c.txt"
    my_data_pars = DataPars(file_path)
    my_data_pars.file_pars_f()
    spectrum_to_correct = my_data_pars.file_body
    spectrum_wavelength = spectrum_to_correct[:, 0]
    spectrum_reflectance = spectrum_to_correct[:, 1]
    spectrum_reflectance_uncertainty = spectrum_to_correct[:, 2]
    # transmission
    window_wavelength = SAPPHIRE_WINDOW_WAVELENGTHS
    window_transmission = SAPPHIRE_WINDOW_TRANSMISSION
    # windows quantity
    windows_quantity = 1 # 1 OR 2
    # correction type
    correction_type = "parasitic reflections" # "parasitic reflections" OR "extended correction"
    # Class instance EVOCATION
    my_window_correction = CoreWindowCorrection(spectrum_wavelength, spectrum_reflectance, spectrum_reflectance_uncertainty,
                                                window_wavelength, window_transmission,
                                                windows_quantity, correction_type)
    my_window_correction.window_correction()
    # OUTPUT
    corrected_reflctance = my_window_correction.class_getter_reflectance()
    corrected_reflectance_uncertainty = my_window_correction.class_getter_reflectance_uncertainty()
    print("Corrected data:")
    print(corrected_reflctance)
    print(corrected_reflectance_uncertainty)


# demo()
