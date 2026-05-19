readme_content = """# HCalculator - Professional Hydraulic Calculator

**HCalculator** is a proprietary, multilingual desktop application designed for engineers, technicians, and designers of hydraulic power systems. The program works 100% offline, making it an ideal tool for use on production floors, in workshops, and in the field.

## Main Features
* **Cylinder parameter calculations:** Push/pull force, extension speed.
* **Pump parameter calculations:** Flow rate, drive motor power, torque.
* **Multilingual support:** Full support for 4 languages (Polish, English, German, Romanian) with automatic system language detection.
* **Offline Operation:** Requires no internet connection or installation on the target computer (Portable version).

## System Requirements (For Developers)
To run the `.py` source code or compile your own version of the application, you need:
* **Python:** Version 3.8 or newer.
* **PyInstaller:** For compiling executables (`pip install pyinstaller`).
* **Graphical dependencies:** The program uses built-in libraries (e.g., Tkinter/PyQt - *make sure they are installed in your environment*).

## Project Structure
Recommended directory structure for the proper operation of the script and compiler:

## Running the Source Code
To run the program directly from the script in the terminal, navigate to the project folder and type:
python main.py

## Application Compilation (Creating Executables)

### For Windows (.exe)
To generate a standalone .exe file (without a visible console in the background), run:
pyinstaller --noconsole --onefile --windowed --icon=icon.ico --add-data "lang;lang" --add-data "assets;assets" main.py
*The compiled main.exe file (you can rename it to HCalculator.exe) will be located in the dist/ folder.*

### For macOS (.app)
Use the previously prepared .spec file, which automatically manages the folder structure for Apple:
pyinstaller HCalculator.spec
*The compiled HCalculator.app application will appear in the dist/ folder.*

## Note on Paths (PyInstaller)
If you are developing the main.py code, remember to use a path mapping function for static files (/lang, /assets) so that the compiled application can find them in its temporary runtime environment (sys._MEIPASS).

## Author and License
Author: Daniel Kaliski
License: Freeware (Free for commercial and private use). Code shared for personal development purposes.
