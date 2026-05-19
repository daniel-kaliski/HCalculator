# HCalculator - Professional Hydraulic Calculator

**HCalculator** is a proprietary, multilingual desktop application designed for engineers, technicians, and designers of hydraulic power systems. The program works 100% offline, making it an ideal tool for use on production floors, in workshops, and in the field.

## Main Features
* **Cylinder parameter calculations:** Push/pull force, extension speed.
* **Pump parameter calculations:** Flow rate, drive motor power, torque.
* **Multilingual support:** Full support for 4 languages (Polish, English, German, Romanian) with automatic system language detection.
* **Offline Operation:** Requires no internet connection or installation on the target computer (Portable version).

## System Requirements (For Developers)
To run the `.py` source code or compile your own version of the application, you need:
* **Python:** Version 3.8 or newer.
* **PyInstaller:** For compiling executable files (`pip install pyinstaller`).
* Graphical dependencies: The program uses built-in libraries (e.g., Tkinter/PyQt - *make sure they are installed in your environment*).

## Project Structure
Recommended directory structure for the proper operation of the script and compiler:

```text
/HCalculator
├── main.py               # Main application script
├── HCalculator.spec      # Configuration file for PyInstaller (macOS/Windows)
├── icon.ico              # Application icon for Windows
├── icon.icns             # Application icon for macOS
├── /lang                 # Directory with translation files (.json)
│   ├── pl.json
│   ├── en.json
│   ├── de.json
│   └── ro.json
└── /assets               # Directory with auxiliary graphics (diagrams, logos)
