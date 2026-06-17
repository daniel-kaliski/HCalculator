<h1 id="english">HCalculator - Professional Hydraulic Calculator v1.1.4</h1>

**HCalculator** is a proprietary, multilingual application designed for engineers, technicians, and fluid power system designers. The program works 100% offline, making it an ideal tool for work in production halls, workshops, and in the field. 

With version 1.1.4, the project features a modern WebView-based UI, native file saving, and fully automated cloud builds.

## Main Features
* **Cylinder parameters:** Push/pull force, cycle time, and extension/retraction speed.
* **Pump parameters:** Flow rate, drive motor power (kW/HP), and efficiency.
* **Hydraulic motor:** Rotational speed and torque on the motor shaft.
* **Oil tank capacity:** Selection of optimal tank capacity for different machine types.
* **Hydraulic hoses:** Optimal inner diameter calculation and advanced pressure drop (Δp) estimation.
* **Accumulator Sizing:** Total volume (V0) and gas pre-charge pressure (P0) calculation.
* **Oil Cooler Power:** Estimation of heat power to dissipate and specific cooling capacity.
* **Flow Coefficient Kv / Cv:** Capacity selection for valves and manifolds.
* **Export & History:** Save calculation reports natively as PNG images or PDF documents. 
* **UI & UX:** Dark mode support, SVG vector flags, and a fully responsive interface.
* **Multilingualism:** Full support for 3 languages (Polish, English, German) with automatic system detection.

## Project Structure (v1.1.4)
The application has transitioned to a lightweight Python backend with an HTML/JS frontend, automated via CI/CD:

```text
/HCalculator
├── .github/workflows/    # CI/CD automation scripts for macOS and Windows
├── HCalculator.py        # Main Python application script (PyWebView)
├── HCalculator.spec      # Configuration file for macOS PyInstaller
├── index.html            # Main UI, logic, and translations
├── html2canvas.min.js    # Library for generating PNG reports
├── flag_*.svg            # Vector UI flag icons
└── HCalculator.ico/icns  # Application icons
```

**System Requirements (For Developers)**
To run the ```.py``` source code or compile your own version, you need:

Python: Version 3.11 (recommended).

Dependencies: ```pip install pywebview pyinstaller```

Running the Source Code
To run the program directly from the script in the terminal, go to the project folder and type:

```bash
python HCalculator.py
```

**Application Compilation (Executable Files)**
The project is fully configured to be built locally or automatically via GitHub Actions.

**For Windows (.exe)**
To generate a standalone, single `.exe` file without a visible background console, run:

```bash
pyinstaller --name "HCalculator" --onefile --windowed --icon="HCalculator.ico" --noconfirm --add-data "index.html;." --add-data "html2canvas.min.js;." --add-data "flag_pl.svg;." --add-data "flag_en.svg;." --add-data "flag_de.svg;." HCalculator.py
```

The compiled `HCalculator.exe` will be located in the `dist/` folder.

**For macOS (.app)**
Use the prepared `.spec` file, which automatically manages the folder structure, icons, and Apple security settings:

```bash
pyinstaller --noconfirm HCalculator.spec
```

The compiled `HCalculator.app` application will appear in the `dist/` folder.

**CI/CD Automation (GitHub Actions)**

This repository includes automated workflows. Every push to the main branch automatically triggers cloud builds for both macOS and Windows. The compiled, ready-to-use packages (`.zip`) are available in the **Actions -> Artifacts** tab.

**Author and License**

Author: Daniel Kaliski

License: Freeware (Free for commercial and private use). Code shared for personal development and portfolio purposes.

