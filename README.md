# HCalculator - Profesjonalny Kalkulator Hydrauliczny

**HCalculator** to autorska, wielojęzyczna aplikacja desktopowa zaprojektowana dla inżynierów, techników i projektantów układów hydrauliki siłowej. Program działa w 100% offline, co czyni go idealnym narzędziem do pracy w halach produkcyjnych, warsztatach i w terenie.

## Główne funkcje
* **Obliczenia parametrów siłowników:** Siła pchania/ciągnięcia, prędkość wysuwu.
* **Obliczenia parametrów pomp:** Wydajność, moc silnika napędowego, moment obrotowy.
* **Obliczenia parametrów silnika hydraulicznego:** Prędkość obrotowa, moment obrotowy.
* **Kubatura zbiornika oleju:** Dobór optymalnej pojemności zbiornika.
* **Obliczenia doboru węży hydraulicznych:** Maszyny mobilne, stacjonarne oraz instalacje przemysłowe.
* **Wielojęzyczność:** Pełne wsparcie dla 3 języków (Polski, Angielski, Niemiecki) z automatycznym wykrywaniem języka systemu.
* **Praca Offline:** Nie wymaga połączenia z internetem ani instalacji na komputerze docelowym (wersja Portable).

## Wymagania systemowe (Dla deweloperów)
Aby uruchomić kod źródłowy `.py` lub skompilować własną wersję aplikacji, potrzebujesz:
* **Python:** Wersja 3.8 lub nowsza.
* **PyInstaller:** Do kompilacji plików wykonywalnych (`pip install pyinstaller`).
* Zależności graficzne: Program wykorzystuje wbudowane biblioteki (np. Tkinter/PyQt - *upewnij się, że są zainstalowane w Twoim środowisku*).

## Struktura projektu
Zalecana struktura katalogów dla prawidłowego działania skryptu i kompilatora:

```text
/HCalculator
├── main.py               # Główny skrypt aplikacji
├── HCalculator.spec      # Plik konfiguracyjny dla PyInstaller (macOS/Windows)
├── icon.ico              # Ikona aplikacji dla Windows
├── icon.icns             # Ikona aplikacji dla macOS
├── /lang                 # Katalog z plikami tłumaczeń (.json)
│   ├── pl.json
│   ├── en.json
│   └── de.json
└── /assets               # Katalog z grafikami pomocniczymi (schematy, logotypy)
```

## Uruchamianie kodu źródłowego
Aby uruchomić program bezpośrednio ze skryptu w terminalu, przejdź do folderu projektu i wpisz:
```bash
python main.py
```

## Kompilacja aplikacji (Tworzenie plików wykonywalnych)

### Dla systemu Windows (.exe)
Aby wygenerować samodzielny plik `.exe` (bez widocznej konsoli w tle), uruchom:
```bash
pyinstaller --noconsole --onefile --windowed --icon=icon.ico --add-data "lang;lang" --add-data "assets;assets" main.py
```
*Gotowy plik `main.exe` (możesz zmienić mu nazwę na `HCalculator.exe`) znajdzie się w folderze `dist/`.*

### Dla systemu macOS (.app)
Użyj przygotowanego wcześniej pliku `.spec`, który automatycznie zarządza strukturą folderów dla Apple:
```bash
pyinstaller HCalculator.spec
```
*Gotowa aplikacja `HCalculator.app` pojawi się w folderze `dist/`.*

## Uwaga dotycząca ścieżek (PyInstaller)
Jeżeli rozwijasz kod `main.py`, pamiętaj o używaniu funkcji mapującej ścieżki do plików statycznych (`/lang`, `/assets`), aby skompilowana aplikacja potrafiła je odnaleźć w swoim tymczasowym środowisku uruchomieniowym (`sys._MEIPASS`).

## Zrzut ekranu
<img width="712" height="912" alt="Zrzut ekranu 2026-06-11 o 11 56 29" src="https://github.com/user-attachments/assets/f9206b59-e912-43d3-b059-e136602aeb21" />

## Autor i Licencja
**Autor:** Daniel Kaliski
**Licencja:** Freeware (Darmowa do użytku komercyjnego i prywatnego). Kod udostępniony na potrzeby rozwoju własnego.
