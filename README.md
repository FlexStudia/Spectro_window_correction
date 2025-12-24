# Spectro Window correction

This desktop application corrects window-induced reflections in calibrated spectral data acquired with SHINE or SHADOW instruments.

## Who is this for?

- **End users**: [download the ready-to-use executable](https://github.com/FlexStudia/Spectro_window_correction/releases)
- **Researchers / developers**:  use the scientific core as a Python module to integrate window reflection correction into your own code

# Features

- Supports plain text and CSV files containing calibrated spectral data, with wavelength values stored in the first column.
- Automatically detects file structure, including:
    - three-column formats,
    - instrument-native multi-column formats (11 or 13 columns),
    - compilation formats (geo, …).
- Input data may include a header with column names and additional metadata.
- Includes a transmission preset for a sapphire window.
- Supports custom window transmission data provided as plain text files.
- Supports correction for one or two optical windows.
- Provides two correction modes:
    - SHINE collimated beam mode,
    - SHADOW and SHINE in Gognoto mode.

# Executable

- The executable can be downloaded from the [Releases page](https://github.com/FlexStudia/Spectro_window_correction/releases)
- **OS support**:
    - Currently available as a Windows executable (EXE)
    - A macOS version is planned
    - Linux support is possible but has not yet been requested
- The executable is distributed as an archive containing:
    - the executable file,
    - an `icons` directory,
    - a `transmission` directory with sapphire window transmission data.

After extracting the archive, the application is ready to use.

# Scientific core

The scientific core, implemented in `core.py`, is a self-contained, UI-agnostic Python module. It can be reused independently of the graphical interface and requires only the `numpy` package.

## How to use

Example usage of the scientific core:

```
from core import CoreWindowCorrection

# initialize the correction
correction_action = CoreWindowCorrection(
	spectrum_wavelength, 
	spectrum_reflectance, 
	spectrum_reflectance_uncertainty, 
	window_wavelength, 
	window_transmission, 
	windows_quantity, 
	correction_type)
	
# perform the correction
correction_action.window_correction()

# retrieve corrected data
corrected_reflectance = correction_action.class_getter_reflectance()
corrected_reflectance_uncertainty = correction_action.class_getter_reflectance_uncertainty()
```

Here:

- `spectrum_wavelength`, `spectrum_reflectance`, and `spectrum_reflectance_uncertainty` are NumPy 1D arrays containing the input spectral data.
- `window_wavelength` and `window_transmission` are NumPy 1D arrays describing the window material transmission.
- The spectral wavelength range must be fully covered by the transmission data.
- `windows_quantity` must be an integer (`1` or `2`) corresponding to the number of windows.
- `correction_type` must be either `"parasitic reflections"` (SHINE collimated beam) or `"extended correction"` (SHADOW and SHINE in Gognotto mode).

A more detailed usage example is provided in the `demo_f` function at the end of `core.py`.

## Core tests & validation

The scientific core was validated by comparing its output with reference files in which the correction had been performed manually.

These reference files are located in `resources/files_to_apply_and_to_compare`. 
Automated tests covering different configurations (number of windows and correction type) are located in `tests/test_core_window_correction.py`. They are powered by the PyTest package, which must be installed in order to run the tests.

# Repository structure

```
icons/           # icons used by the UI notification system
maps/            # logic maps (mind maps)
presets/         # Python files containing transmission presets
resources/       # fspectral data files used as examples and for testing
template/        # UI templates
tests/           # core and interface tests, test utilities, and test data
tools/           # auxiliary modules (array handling & data parsing)
transmission/    # transmission data files (TXT)
core.py          # scientific core
main.py          # UI layer and executable entry point
requirements.txt # project dependencies (pip install -r requirements.txt)
LICENCE          # GNU GPL-3 license text
README.md        # this readme file

```

# Licensing

This project is licensed under the GNU General Public License v3.0 (GPL-3).

### Scientific use

The executable and source code may be freely used for research and educational purposes.
You may run the software, analyze the results, and incorporate them into scientific work.

Citation of this software in scientific publications is appreciated, but not required by the license.

### Redistribution and modifications

If you modify or redistribute the software (in source or binary form), the resulting work must be distributed under the same GPL-3 license, and the corresponding source code must be made publicly available.

This requirement applies to the executable, the scientific core, and all derived works.

# Documentation

Documentation is currently limited to inline comments and usage examples provided in the source code.

# Contributing

If you encounter any bugs or issues, please report them by email at [flex.studia.help@gmail.com](mailto:flex.studia.help@gmail.com).
