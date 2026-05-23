import webview
import sys
import os

# Bezpieczne ładowanie HTML dzięki 'r'
html_content = r"""
<!DOCTYPE html>
<html lang="pl">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>HCalculator - Hydraulic Calculator</title>
<style>
  /* 1. RESET TŁA: Ustawiamy tło okna na jednolity, jasny kolor bez marginesów */
  html, body { 
      margin: 0; 
      padding: 0; 
      background-color: #f4f7f9; /* Główne tło aplikacji */
      font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; 
      height: 100%; 
      display: flex; 
      flex-direction: column; 
  }
  
  /* 2. KONTENER: Brak cieni i marginesów - wypełnia 100% okna */
  .br-app-container { 
      width: 100%; 
      flex: 1; 
      display: flex; 
      flex-direction: column;
  }
  
  /* Pasek górny (INFO i Język) */
  .top-bar { background-color: #002244; display: flex; justify-content: flex-end; align-items: center; padding: 8px 15px; gap: 15px; flex-shrink: 0; }
  .lang-selector select { background-color: #003366; color: white; border: 1px solid #0055a5; padding: 5px 10px; border-radius: 4px; font-size: 13px; cursor: pointer; outline: none; }
  .about-btn { background: none; border: none; color: #a0c4e8; font-size: 13px; cursor: pointer; font-weight: bold; text-transform: uppercase; }
  .about-btn:hover { color: #fff; }
  
  /* Zakładki (Zablokowane na górze przy przewijaniu) */
  .br-tabs { display: flex; flex-wrap: wrap; background-color: #003366; border-bottom: 2px solid #0055a5; position: sticky; top: 0; z-index: 10; flex-shrink: 0; }
  .br-tab-btn { flex: 1 1 auto; background: none; border: none; color: #a0c4e8; padding: 16px 5px; font-size: 13px; font-weight: bold; text-transform: uppercase; cursor: pointer; transition: 0.2s; text-align: center; outline: none; }
  .br-tab-btn:hover { color: #ffffff; background-color: #004080; }
  .br-tab-btn.active { color: #ffffff; background-color: #0055a5; border-bottom: 3px solid #ffaa00; }
  
  /* Zawartość zakładek */
  .br-tab-content { display: none; padding: 25px; flex: 1; overflow-y: auto; }
  .br-tab-content.active { display: block; animation: fadeIn 0.3s ease-in-out; }
  @keyframes fadeIn { from { opacity: 0; transform: translateY(5px); } to { opacity: 1; transform: translateY(0); } }
  
  .br-tab-content h3 { color: #003366; text-align: center; margin-top: 0; margin-bottom: 5px; font-size: 22px; text-transform: uppercase; }
  .br-tab-content p.desc { font-size: 14px; color: #555; text-align: center; margin-bottom: 25px; }
  
  /* Formularze */
  .br-form-group { margin-bottom: 15px; }
  .br-form-group label { display: block; font-weight: bold; margin-bottom: 6px; font-size: 14px; color: #333; }
  .br-form-group input, .br-form-group select { width: 100%; padding: 12px; border: 1px solid #ccc; border-radius: 6px; box-sizing: border-box; font-size: 14px; font-family: inherit; }
  .br-form-group input:focus, .br-form-group select:focus { border-color: #0055a5; outline: none; box-shadow: 0 0 0 2px rgba(0, 85, 165, 0.2); }
  
  /* Przyciski operacyjne */
  .br-calc-btn { width: 100%; background-color: #0055a5; color: white; padding: 14px; border: none; border-radius: 25px; font-size: 16px; font-weight: bold; cursor: pointer; transition: 0.2s; margin-top: 15px; }
  .br-calc-btn:hover { background-color: #004080; }
  
  .br-coffee-btn { display: flex; justify-content: center; align-items: center; width: 100%; box-sizing: border-box; background-color: #ffaa00; color: #003366; padding: 14px; border: none; border-radius: 25px; font-size: 16px; font-weight: bold; cursor: pointer; transition: 0.2s; margin-top: 25px; text-decoration: none; box-shadow: 0 4px 10px rgba(255, 170, 0, 0.3); }
  .br-coffee-btn:hover { background-color: #ffb732; transform: translateY(-2px); }
  .br-coffee-btn svg { margin-right: 10px; width: 20px; height: 20px; }
  
  /* Wyniki */
  .br-results { margin-top: 25px; padding: 20px; background-color: #ffffff; border: 2px solid #0055a5; border-radius: 6px; display: none; box-shadow: 0 4px 10px rgba(0,0,0,0.05); }
  .br-results p { margin: 0 0 10px 0; font-size: 16px; }
  
  .br-copy-btn { background-color: #e2e8f0; border: 1px solid #ccc; color: #003366; padding: 8px 12px; border-radius: 4px; font-size: 13px; cursor: pointer; margin-top: 15px; width: 100%; transition: 0.2s; font-weight: bold; display: none; }
  .br-copy-btn:hover { background-color: #cbd5e1; border-color: #0055a5; }
  .br-copy-btn.success { background-color: #5cb85c; color: white; border-color: #4cae4c; }
  
  /* Stopka (przyklejona do dołu okna) */
  .br-footer { text-align: center; padding: 15px; background-color: #e8ecef; color: #666; font-size: 12px; border-top: 1px solid #dcdcdc; flex-shrink: 0; }
  
  #toast { visibility: hidden; min-width: 250px; background-color: #d9534f; color: #fff; text-align: center; border-radius: 6px; padding: 16px; position: fixed; z-index: 1000; left: 50%; bottom: 30px; transform: translateX(-50%); font-size: 14px; font-weight: bold; box-shadow: 0 4px 12px rgba(0,0,0,0.3); }
  #toast.show { visibility: visible; animation: fadein 0.5s, fadeout 0.5s 2.5s; }
  @keyframes fadein { from {bottom: 0; opacity: 0;} to {bottom: 30px; opacity: 1;} }
  @keyframes fadeout { from {bottom: 30px; opacity: 1;} to {bottom: 0; opacity: 0;} }

  /* Style obszaru drukowania (PDF) */
  #print-area { display: none; }
  @media print {
      body * { visibility: hidden; }
      body { background-color: #fff; }
      #print-area, #print-area * { visibility: visible; }
      #print-area { display: block; position: absolute; left: 0; top: 0; width: 100%; padding: 20px; }
      #print-area h2 { color: #003366; border-bottom: 2px solid #ffaa00; padding-bottom: 10px; margin-top: 0; }
      #print-area .print-block { margin-bottom: 20px; padding: 15px; background: #f4f7f9; border-radius: 8px; border: 1px solid #ccc; }
      #print-area strong { color: #333; }
      .no-print { display: none !important; }
  }
</style>
</head>
<body>

<div id="toast">Wystąpił błąd!</div>

<div id="print-area">
    <h2 id="print-title">HCalculator - Raport Obliczeń</h2>
    <p id="print-date" style="color: #666; font-size: 14px;"></p>
    <div class="print-block">
        <h3 style="margin-top:0; color:#0055a5;">Parametry Wejściowe:</h3>
        <pre id="print-params" style="font-family: 'Segoe UI', sans-serif; font-size: 14px; white-space: pre-wrap; margin:0;"></pre>
    </div>
    <div class="print-block" style="background: #e6f0fa; border-color: #0055a5;">
        <h3 style="margin-top:0; color:#d9534f;">Wyniki Obliczeń:</h3>
        <pre id="print-results" style="font-family: 'Segoe UI', sans-serif; font-size: 16px; font-weight: bold; color: #002244; white-space: pre-wrap; margin:0;"></pre>
    </div>
    <p style="font-size: 12px; color: #999; text-align: center; margin-top: 40px;">Wygenerowano w programie HCalculator v1.0.2</p>
</div>

<div class="no-print br-app-container">
    <div class="top-bar">
      <button class="about-btn" id="show-about-btn" data-i18n="about">ℹ️ O Programie</button>
      <div class="lang-selector">
        <select id="lang-switch">
          <option value="pl">🇵🇱 Polski</option>
          <option value="en">🇬🇧 English</option>
          <option value="de">🇩🇪 Deutsch</option>
          <option value="ro">🇷🇴 Română</option>
        </select>
      </div>
    </div>

    <div class="br-tabs">
      <button class="br-tab-btn active" data-tab="tab-sila" data-i18n="tab_force">Siła</button>
      <button class="br-tab-btn" data-tab="tab-predkosc" data-i18n="tab_speed">Prędkość</button>
      <button class="br-tab-btn" data-tab="tab-moc" data-i18n="tab_power">Moc</button>
      <button class="br-tab-btn" data-tab="tab-wydajnosc" data-i18n="tab_flow">Wydajn.</button>
      <button class="br-tab-btn" data-tab="tab-zbiornik" data-i18n="tab_tank">Zbiornik</button>
      <button class="br-tab-btn" data-tab="tab-historia" data-i18n="tab_history">Historia</button>
    </div>

    <div class="br-tab-content active" id="tab-sila">
      <h3 data-i18n="force_title">Siła Siłownika</h3>
      <p class="desc" data-i18n="force_desc">Oblicz siłę pchania i ciągnięcia.</p>
      <div class="br-form-group">
        <label data-i18n="pressure">Ciśnienie robocze (bar):</label>
        <input type="number" id="calc-pressure" data-i18n-ph="ph_180" placeholder="np. 180" min="0">
      </div>
      <div class="br-form-group">
        <label data-i18n="bore">Wewn. średnica tłoka (mm):</label>
        <input type="number" id="calc-bore" data-i18n-ph="ph_80" placeholder="np. 80" min="0">
      </div>
      <div class="br-form-group">
        <label data-i18n="rod">Średnica tłoczyska (mm):</label>
        <input type="number" id="calc-rod" data-i18n-ph="ph_40" placeholder="np. 40" min="0">
      </div>
      <button class="br-calc-btn" id="run-calc-btn" data-i18n="btn_force">Oblicz siłę</button>
      <div class="br-results" id="calc-results">
        <p><strong data-i18n="push">Siła pchania:</strong> <span id="res-push" style="color: #d9534f; font-weight: bold;">0</span> kg</p>
        <p><strong data-i18n="pull">Siła ciągnięcia:</strong> <span id="res-pull" style="color: #d9534f; font-weight: bold;">0</span> kg</p>
      </div>
    </div>

    <div class="br-tab-content" id="tab-predkosc">
      <h3 data-i18n="speed_title">Prędkość i Czas Cyklu</h3>
      <p class="desc" data-i18n="speed_desc">Oblicz czas pełnego wysuwu i powrotu.</p>
      <div class="br-form-group">
        <label data-i18n="flow">Przepływ oleju pompy (L/min):</label>
        <input type="number" id="spd-flow" data-i18n-ph="ph_40" placeholder="np. 40" min="0">
      </div>
      <div class="br-form-group">
        <label data-i18n="bore">Wewn. średnica tłoka (mm):</label>
        <input type="number" id="spd-bore" data-i18n-ph="ph_80" placeholder="np. 80" min="0">
      </div>
      <div class="br-form-group">
        <label data-i18n="rod">Średnica tłoczyska (mm):</label>
        <input type="number" id="spd-rod" data-i18n-ph="ph_40" placeholder="np. 40" min="0">
      </div>
      <div class="br-form-group">
        <label data-i18n="stroke">Skok siłownika (mm):</label>
        <input type="number" id="spd-stroke" data-i18n-ph="ph_500" placeholder="np. 500" min="0">
      </div>
      <button class="br-calc-btn" id="calc-spd-btn" data-i18n="btn_speed">Oblicz prędkość</button>
      <div class="br-results" id="spd-results">
        <p><strong data-i18n="v_push">Prędkość wysuwu:</strong> <span id="res-v-push" style="color: #d9534f; font-weight: bold;">0</span> cm/s</p>
        <p><strong data-i18n="t_push">Czas wysuwu:</strong> <span id="res-t-push" style="color: #0055a5; font-weight: bold;">0</span> s</p>
        <hr style="border: 0; border-top: 1px solid #eee; margin: 15px 0;">
        <p><strong data-i18n="v_pull">Prędkość powrotu:</strong> <span id="res-v-pull" style="color: #d9534f; font-weight: bold;">0</span> cm/s</p>
        <p><strong data-i18n="t_pull">Czas powrotu:</strong> <span id="res-t-pull" style="color: #0055a5; font-weight: bold;">0</span> s</p>
      </div>
    </div>

    <div class="br-tab-content" id="tab-moc">
      <h3 data-i18n="power_title">Moc Napędu Pompy</h3>
      <p class="desc" data-i18n="power_desc">Dobierz silnik elektryczny/spalinowy.</p>
      <div class="br-form-group">
        <label data-i18n="p_flow">Wydajność pompy (L/min):</label>
        <input type="number" id="pmp-flow" data-i18n-ph="ph_40" placeholder="np. 40" min="0">
      </div>
      <div class="br-form-group">
        <label data-i18n="p_max">Maksymalne ciśnienie (bar):</label>
        <input type="number" id="pmp-pressure" data-i18n-ph="ph_180" placeholder="np. 180" min="0">
      </div>
      <div class="br-form-group">
        <label data-i18n="p_type">Rodzaj pompy:</label>
        <select id="pmp-eff">
          <option value="0.85" data-i18n="gear" selected>Pompa zębata (~85%)</option>
          <option value="0.90" data-i18n="piston">Pompa wielotłoczkowa (~90%)</option>
        </select>
      </div>
      <button class="br-calc-btn" id="calc-pmp-btn" data-i18n="btn_power">Oblicz moc</button>
      <div class="br-results" id="pmp-results">
        <p><strong data-i18n="kw">Wymagana moc silnika:</strong> <span id="res-kw" style="color: #d9534f; font-weight: bold;">0</span> kW</p>
        <p><strong data-i18n="hp">Odpowiednik:</strong> <span id="res-km" style="color: #0055a5; font-weight: bold;">0</span> <span data-i18n="hp_unit">KM / HP</span></p>
      </div>
    </div>

    <div class="br-tab-content" id="tab-wydajnosc">
      <h3 data-i18n="flow_title">Wydajność Pompy</h3>
      <p class="desc" data-i18n="flow_desc">Oblicz L/min na podstawie chłonności.</p>
      <div class="br-form-group">
        <label data-i18n="disp">Chłonność pompy (cm³/obr):</label>
        <input type="number" id="flow-disp" data-i18n-ph="ph_14" placeholder="np. 14" min="0">
      </div>
      <div class="br-form-group">
        <label data-i18n="rpm">Prędkość obrotowa napędu (obr/min):</label>
        <select id="flow-rpm-select">
          <option value="1450" data-i18n="rpm1" selected>1450 obr/min (Silnik elektr.)</option>
          <option value="3000" data-i18n="rpm2">3000 obr/min (Silnik spalinowy)</option>
          <option value="540" data-i18n="rpm3">540 obr/min (Wałek WOM)</option>
          <option value="custom" data-i18n="rpm_custom">Inna wartość (wpisz poniżej)</option>
        </select>
        <input type="number" id="flow-rpm-custom" data-i18n-ph="ph_custom" placeholder="Wpisz obroty..." style="display: none; margin-top: 10px;" min="0">
      </div>
      <div class="br-form-group">
        <label data-i18n="cond">Stan pompy:</label>
        <select id="flow-eff">
          <option value="0.95" data-i18n="new_p" selected>Nowa pompa (~95%)</option>
          <option value="0.85" data-i18n="old_p">Używana pompa (~85%)</option>
        </select>
      </div>
      <button class="br-calc-btn" id="calc-flow-btn" data-i18n="btn_flow">Oblicz wydajność</button>
      <div class="br-results" id="flow-results">
        <p><strong data-i18n="actual">Rzeczywista wydajność:</strong> <span id="res-flow-actual" style="color: #d9534f; font-weight: bold;">0</span> L/min</p>
        <p style="font-size: 14px;"><span data-i18n="theo">Teoretyczna:</span> <span id="res-flow-theo" style="font-weight: bold;">0</span> L/min</p>
      </div>
    </div>

    <div class="br-tab-content" id="tab-zbiornik">
      <h3 data-i18n="tank_title">Pojemność Zbiornika</h3>
      <p class="desc" data-i18n="tank_desc">Zadbaj o właściwe chłodzenie oleju.</p>
      <div class="br-form-group">
        <label data-i18n="p_flow">Wydajność pompy (L/min):</label>
        <input type="number" id="tank-flow" data-i18n-ph="ph_40" placeholder="np. 40" min="0">
      </div>
      <div class="br-form-group">
        <label data-i18n="sys_type">Typ układu:</label>
        <select id="tank-type">
          <option value="mobile" data-i18n="mob" selected>Maszyny mobilne / rolnicze</option>
          <option value="industrial" data-i18n="ind">Maszyny stacjonarne / przemysłowe</option>
          <option value="closed" data-i18n="closed">Układ zamknięty</option>
        </select>
      </div>
      <button class="br-calc-btn" id="calc-tank-btn" data-i18n="btn_tank">Oblicz pojemność</button>
      <div class="br-results" id="tank-results">
        <p><strong data-i18n="rec">Rekomendowana pojemność:</strong> <span id="res-tank-range" style="color: #d9534f; font-weight: bold;">0</span> <span data-i18n="liters">litrów</span></p>
      </div>
    </div>

    <div class="br-tab-content" id="tab-historia">
      <h3 data-i18n="history_title">Historia Obliczeń</h3>
      <p class="desc" data-i18n="history_desc">Twoje 10 ostatnich wyników. (Lokalnie)</p>
      
      <div id="history-list"></div>
      
      <button id="clear-history-btn" class="br-copy-btn" style="display:block; margin-top:20px; background-color:#fce4e4; border-color:#d9534f; color:#d9534f;" data-i18n="clear_history">Wyczyść historię</button>
    </div>
    
    <div class="br-tab-content" id="tab-about">
      <h3 data-i18n="about_title">HCalculator v1.0.2</h3>
      <p class="desc" data-i18n="about_desc">Profesjonalny Kalkulator Hydrauliczny</p>
      <div style="background-color: #fff; padding: 20px; border-radius: 8px; border: 1px solid #e0e0e0; line-height: 1.6;">
          <p data-i18n="about_text" style="color: #444; font-size: 15px; margin-top: 0;">
              Ten program tworzę hobbystycznie. Jest w 100% darmowy, nie wyświetla reklam i szanuje Twoją prywatność działając offline. Jeśli HCalculator zaoszczędził Twój czas w warsztacie lub przy projekcie, możesz wesprzeć jego dalszy rozwój, stawiając mi symboliczną kawę. Dziękuję!
          </p>
          <a href="https://www.buymeacoffee.com/hcalculator" target="_blank" class="br-coffee-btn" id="coffee-link">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
              <path d="M18 8h1a4 4 0 0 1 0 8h-1"></path>
              <path d="M2 8h16v9a4 4 0 0 1-4 4H6a4 4 0 0 1-4-4V8z"></path>
              <line x1="6" y1="1" x2="6" y2="4"></line>
              <line x1="10" y1="1" x2="10" y2="4"></line>
              <line x1="14" y1="1" x2="14" y2="4"></line>
            </svg>
            <span data-i18n="btn_coffee">Postaw mi kawę</span>
          </a>
      </div>
    </div>
</div>

<div class="br-footer">
    <span id="currentYear"></span> &copy; Daniel Kaliski
</div>

<script>
// --- ZMIENNA PRZECHOWUJĄCA HISTORIĘ ---
window.appHistory = [];

document.getElementById('coffee-link').addEventListener('click', function(e) {
    e.preventDefault();
    if(window.pywebview) { window.pywebview.api.open_url(this.href); } else { window.open(this.href, '_blank'); }
});

const langDict = {
  "pl": {
    "about": "ℹ️ O Programie", "tab_force": "Siła", "tab_speed": "Prędkość", "tab_power": "Moc", "tab_flow": "Wydajność", "tab_tank": "Zbiornik", "tab_history": "Historia",
    "force_title": "Siła Siłownika", "force_desc": "Oblicz siłę pchania i ciągnięcia.",
    "pressure": "Ciśnienie robocze (bar):", "bore": "Wewn. średnica tłoka (mm):", "rod": "Średnica tłoczyska (mm):",
    "btn_force": "Oblicz siłę", "push": "Siła pchania:", "pull": "Siła ciągnięcia:",
    "speed_title": "Prędkość i Czas Cyklu", "speed_desc": "Oblicz czas pełnego wysuwu i powrotu.",
    "flow": "Przepływ oleju pompy (L/min):", "stroke": "Skok siłownika (mm):", "btn_speed": "Oblicz prędkość",
    "v_push": "Prędkość wysuwu:", "t_push": "Czas wysuwu:", "v_pull": "Prędkość powrotu:", "t_pull": "Czas powrotu:",
    "power_title": "Moc Napędu Pompy", "power_desc": "Dobierz silnik elektryczny/spalinowy.",
    "p_flow": "Wydajność pompy (L/min):", "p_max": "Maksymalne ciśnienie (bar):", "p_type": "Rodzaj pompy:",
    "gear": "Pompa zębata (~85%)", "piston": "Pompa wielotłoczkowa (~90%)", "btn_power": "Oblicz moc",
    "kw": "Wymagana moc silnika:", "hp": "Odpowiednik:", "hp_unit": "KM / HP",
    "flow_title": "Wydajność Pompy", "flow_desc": "Oblicz L/min na podstawie chłonności.",
    "disp": "Chłonność pompy (cm³/obr):", "rpm": "Prędkość obrotowa napędu (obr/min):",
    "rpm1": "1450 obr/min (Silnik elektr.)", "rpm2": "3000 obr/min (Silnik spalinowy)", "rpm3": "540 obr/min (Wałek WOM)", "rpm_custom": "Inna wartość (wpisz poniżej)",
    "cond": "Stan pompy:", "new_p": "Nowa pompa (~95%)", "old_p": "Używana pompa (~85%)", "btn_flow": "Oblicz wydajność",
    "actual": "Rzeczywista wydajność:", "theo": "Teoretyczna:",
    "tank_title": "Pojemność Zbiornika", "tank_desc": "Zadbaj o właściwe chłodzenie oleju.",
    "sys_type": "Typ układu:", "mob": "Maszyny mobilne / rolnicze", "ind": "Maszyny stacjonarne / przemysłowe", "closed": "Układ zamknięty",
    "btn_tank": "Oblicz pojemność", "rec": "Rekomendowana pojemność:", "liters": "litrów",
    "history_title": "Historia Obliczeń", "history_desc": "Twoje 10 ostatnich wyników (Trwale zapisane).", "clear_history": "Wyczyść historię", "empty_history": "Brak zapisanej historii.",
    "btn_pdf": "📄 Generuj PDF (Zapisz)", "copy_btn": "📋 Kopiuj wynik",
    "about_title": "HCalculator v1.0.2", "about_desc": "Profesjonalny Kalkulator Hydrauliczny",
    "about_text": "Ten program tworzę hobbystycznie. Jest w 100% darmowy, nie wyświetla reklam i szanuje Twoją prywatność działając offline. Jeśli HCalculator zaoszczędził Twój czas w warsztacie lub przy projekcie, możesz wesprzeć jego dalszy rozwój, stawiając mi symboliczną kawę. Dziękuję!",
    "btn_coffee": "Postaw mi kawę",
    "ph_180": "np. 180", "ph_80": "np. 80", "ph_40": "np. 40", "ph_500": "np. 500", "ph_14": "np. 14", "ph_custom": "Wpisz obroty...",
    "err_empty": "Proszę poprawnie wypełnić wszystkie pola!",
    "err_bore": "Średnica tłoka musi być większa niż tłoczyska!"
  },
  "en": {
    "about": "ℹ️ About", "tab_force": "Force", "tab_speed": "Speed", "tab_power": "Power", "tab_flow": "Flow Rate", "tab_tank": "Tank", "tab_history": "History",
    "force_title": "Cylinder Force", "force_desc": "Calculate push and pull force.",
    "pressure": "Operating pressure (bar):", "bore": "Inner bore diameter (mm):", "rod": "Rod diameter (mm):",
    "btn_force": "Calculate force", "push": "Push force:", "pull": "Pull force:",
    "speed_title": "Speed & Cycle Time", "speed_desc": "Calculate full extension and retraction time.",
    "flow": "Pump flow rate (L/min):", "stroke": "Cylinder stroke (mm):", "btn_speed": "Calculate speed",
    "v_push": "Extension speed:", "t_push": "Extension time:", "v_pull": "Retraction speed:", "t_pull": "Retraction time:",
    "power_title": "Pump Drive Power", "power_desc": "Select electric or combustion engine.",
    "p_flow": "Pump flow rate (L/min):", "p_max": "Maximum pressure (bar):", "p_type": "Pump type:",
    "gear": "Gear pump (~85%)", "piston": "Piston pump (~90%)", "btn_power": "Calculate power",
    "kw": "Required engine power:", "hp": "Equivalent:", "hp_unit": "HP",
    "flow_title": "Pump Flow Rate", "flow_desc": "Calculate L/min from displacement.",
    "disp": "Pump displacement (cm³/rev):", "rpm": "Drive rotation speed (rpm):",
    "rpm1": "1450 rpm (Electric motor)", "rpm2": "3000 rpm (Combustion engine)", "rpm3": "540 rpm (PTO shaft)", "rpm_custom": "Other value (enter below)",
    "cond": "Pump condition:", "new_p": "New pump (~95%)", "old_p": "Used pump (~85%)", "btn_flow": "Calculate flow",
    "actual": "Actual flow rate:", "theo": "Theoretical:",
    "tank_title": "Tank Capacity", "tank_desc": "Ensure proper oil cooling.",
    "sys_type": "System type:", "mob": "Mobile / agricultural machinery", "ind": "Stationary / industrial machinery", "closed": "Closed loop system",
    "btn_tank": "Calculate capacity", "rec": "Recommended capacity:", "liters": "liters",
    "history_title": "Calculation History", "history_desc": "Your last 10 results (Saved persistently).", "clear_history": "Clear History", "empty_history": "No history saved yet.",
    "btn_pdf": "📄 Generate PDF (Save)", "copy_btn": "📋 Copy result",
    "about_title": "HCalculator v1.0.2", "about_desc": "Professional Hydraulic Calculator",
    "about_text": "This program is a passion project. It is 100% free, has no ads, and respects your privacy by working completely offline. If HCalculator has saved you time in the workshop or on a project, you can support its future development by buying me a virtual coffee. Thank you!",
    "btn_coffee": "Buy me a coffee",
    "ph_180": "e.g. 180", "ph_80": "e.g. 80", "ph_40": "e.g. 40", "ph_500": "e.g. 500", "ph_14": "e.g. 14", "ph_custom": "Enter RPM...",
    "err_empty": "Please fill in all fields correctly!",
    "err_bore": "Bore diameter must be larger than rod diameter!"
  },
  "de": {
    "about": "ℹ️ Über", "tab_force": "Kraft", "tab_speed": "Zykluszeit", "tab_power": "Leistung", "tab_flow": "Fördermenge", "tab_tank": "Tank", "tab_history": "Verlauf",
    "force_title": "Zylinderkraft", "force_desc": "Druck- und Zugkraft berechnen.",
    "pressure": "Betriebsdruck (bar):", "bore": "Kolbeninnendurchmesser (mm):", "rod": "Stangendurchmesser (mm):",
    "btn_force": "Kraft berechnen", "push": "Druckkraft:", "pull": "Zugkraft:",
    "speed_title": "Geschwindigkeit & Zykluszeit", "speed_desc": "Aus- und Einfahrzeit berechnen.",
    "flow": "Pumpenfördermenge (L/min):", "stroke": "Zylinderhub (mm):", "btn_speed": "Zeit berechnen",
    "v_push": "Ausfahrgeschwindigkeit:", "t_push": "Ausfahrzeit:", "v_pull": "Einfahrgeschwindigkeit:", "t_pull": "Einfahrzeit:",
    "power_title": "Pumpenantriebsleistung", "power_desc": "Elektro-/Verbrennungsmotor wählen.",
    "p_flow": "Pumpenfördermenge (L/min):", "p_max": "Maximaler Druck (bar):", "p_type": "Pumpentyp:",
    "gear": "Zahnradpumpe (~85%)", "piston": "Kolbenpumpe (~90%)", "btn_power": "Leistung berechnen",
    "kw": "Benötigte Motorleistung:", "hp": "Äquivalent:", "hp_unit": "PS",
    "flow_title": "Pumpenfördermenge", "flow_desc": "L/min aus Schluckvolumen berechnen.",
    "disp": "Schluckvolumen (cm³/U):", "rpm": "Antriebsdrehzahl (U/min):",
    "rpm1": "1450 U/min (Elektromotor)", "rpm2": "3000 U/min (Verbrennungsmotor)", "rpm3": "540 U/min (Zapfwelle)", "rpm_custom": "Anderer Wert (unten)",
    "cond": "Pumpenzustand:", "new_p": "Neue Pumpe (~95%)", "old_p": "Gebrauchte Pumpe (~85%)", "btn_flow": "Menge berechnen",
    "actual": "Tatsächliche Fördermenge:", "theo": "Theoretisch:",
    "tank_title": "Tankkapazität", "tank_desc": "Richtige Ölkühlung sicherstellen.",
    "sys_type": "Systemtyp:", "mob": "Mobile / Landmaschinen", "ind": "Stationäre / Industriemaschinen", "closed": "Geschlossenes System",
    "btn_tank": "Kapazität berechnen", "rec": "Empfohlene Kapazität:", "liters": "Liter",
    "history_title": "Berechnungsverlauf", "history_desc": "Ihre letzten 10 Ergebnisse (Lokal).", "clear_history": "Verlauf löschen", "empty_history": "Noch kein Verlauf gespeichert.",
    "btn_pdf": "📄 PDF erstellen", "copy_btn": "📋 Ergebnis kopieren",
    "about_title": "HCalculator v1.0.2", "about_desc": "Professioneller Hydraulik-Rechner",
    "about_text": "Dieses Programm ist ein Leidenschaftsprojekt. Es ist zu 100 % kostenlos, werbefrei und respektiert Ihre Privatsphäre, da es komplett offline funktioniert. Wenn HCalculator Ihnen in der Werkstatt oder bei einem Projekt Zeit gespart hat, können Sie die weitere Entwicklung unterstützen, indem Sie mir einen virtuellen Kaffee spendieren. Danke!",
    "btn_coffee": "Spendieren Sie mir einen Kaffee",
    "ph_180": "z.B. 180", "ph_80": "z.B. 80", "ph_40": "z.B. 40", "ph_500": "z.B. 500", "ph_14": "z.B. 14", "ph_custom": "U/min eingeben...",
    "err_empty": "Bitte füllen Sie alle Felder korrekt aus!",
    "err_bore": "Kolbendurchmesser muss größer als Stangendurchmesser sein!"
  },
  "ro": {
    "about": "ℹ️ Despre", "tab_force": "Forță", "tab_speed": "Viteză", "tab_power": "Putere", "tab_flow": "Debit", "tab_tank": "Rezervor", "tab_history": "Istoric",
    "force_title": "Forța Cilindrului", "force_desc": "Calculați forța de împingere și tragere.",
    "pressure": "Presiune de lucru (bar):", "bore": "Diametru interior piston (mm):", "rod": "Diametru tijă (mm):",
    "btn_force": "Calculați forța", "push": "Forță de împingere:", "pull": "Forță de tragere:",
    "speed_title": "Viteza și Timpul de Ciclu", "speed_desc": "Calculați timpul de extindere și retragere.",
    "flow": "Debit pompă (L/min):", "stroke": "Cursă cilindru (mm):", "btn_speed": "Calculați viteza",
    "v_push": "Viteză de extindere:", "t_push": "Timp de extindere:", "v_pull": "Viteză de retragere:", "t_pull": "Timp de retragere:",
    "power_title": "Putere Antrenare Pompă", "power_desc": "Alegeți motorul electric/termic.",
    "p_flow": "Debit pompă (L/min):", "p_max": "Presiune maximă (bar):", "p_type": "Tip pompă:",
    "gear": "Pompă roți dințate (~85%)", "piston": "Pompă cu pistoane (~90%)", "btn_power": "Calculați puterea",
    "kw": "Putere necesară motor:", "hp": "Echivalent:", "hp_unit": "CP",
    "flow_title": "Debitul Pompei", "flow_desc": "Calculați L/min din capacitatea cilindrică.",
    "disp": "Capacitate cilindrică (cm³/rot):", "rpm": "Turație antrenare (rot/min):",
    "rpm1": "1450 rot/min (Motor electric)", "rpm2": "3000 rot/min (Motor termic)", "rpm3": "540 rot/min (Priză putere)", "rpm_custom": "Altă valoare (mai jos)",
    "cond": "Stare pompă:", "new_p": "Pompă nouă (~95%)", "old_p": "Pompă uzată (~85%)", "btn_flow": "Calculați debitul",
    "actual": "Debit real:", "theo": "Teoretic:",
    "tank_title": "Capacitatea Rezervorului", "tank_desc": "Asigurați răcirea corectă a uleiului.",
    "sys_type": "Tip sistem:", "mob": "Utilaje mobile / agricole", "ind": "Utilaje staționare / industriale", "closed": "Sistem închis",
    "btn_tank": "Calculați capacitatea", "rec": "Capacitate recomandată:", "liters": "litri",
    "history_title": "Istoricul Calculelor", "history_desc": "Ultimele 10 rezultate (Local).", "clear_history": "Șterge Istoricul", "empty_history": "Nu există istoric salvat.",
    "btn_pdf": "📄 Generare PDF", "copy_btn": "📋 Copiați rezultatul",
    "about_title": "HCalculator v1.0.2", "about_desc": "Calculator Hidraulic Profesional",
    "about_text": "Acest program este un proiect de pasiune. Este 100% gratuit, nu are reclame și îți respectă confidențialitatea funcționând complet offline. Dacă HCalculator te-a ajutat să economisești timp în atelier sau la un proiect, poți susține dezvoltarea sa viitoare cumpărându-mi o cafea virtuală. Mulțumesc!",
    "btn_coffee": "Cumpără-mi o cafea",
    "ph_180": "ex. 180", "ph_80": "ex. 80", "ph_40": "ex. 40", "ph_500": "ex. 500", "ph_14": "ex. 14", "ph_custom": "Turație...",
    "err_empty": "Vă rugăm să completați corect toate câmpurile!",
    "err_bore": "Diametrul pistonului trebuie să fie mai mare decât tija!"
  }
};

document.addEventListener('DOMContentLoaded', function() {
  document.getElementById("currentYear").textContent = new Date().getFullYear();
  var langSwitch = document.getElementById('lang-switch');
  
  // Funkcja generująca PDF
  window.generatePDF = function(title, params, results) {
      document.getElementById('print-title').innerText = title;
      document.getElementById('print-date').innerText = "Data: " + new Date().toLocaleString();
      document.getElementById('print-params').innerText = params;
      document.getElementById('print-results').innerText = results;
      window.print();
  }

  // --- ZAPIS HISTORII Z WYKORZYSTANIEM PYTHON API (Trwałe) ---
  function persistHistory() {
      if(window.pywebview && window.pywebview.api) {
          window.pywebview.api.save_history(JSON.stringify(window.appHistory));
      } else {
          localStorage.setItem('hcalc_history', JSON.stringify(window.appHistory));
      }
  }

  function saveToHistory(typeKey, paramsText, resultsText) {
      let currentLang = langSwitch.value;
      let typeTranslated = langDict[currentLang][typeKey] || typeKey;
      
      const newEntry = {
          date: new Date().toLocaleString(),
          type: typeTranslated,
          params: paramsText,
          results: resultsText
      };
      
      window.appHistory.unshift(newEntry);
      if (window.appHistory.length > 10) { window.appHistory = window.appHistory.slice(0, 10); }
      
      persistHistory();
      renderHistory();
  }

  function renderHistory() {
      const list = document.getElementById('history-list');
      let currentLang = langSwitch.value;
      
      if (!window.appHistory || window.appHistory.length === 0) {
          list.innerHTML = `<p style="text-align:center; color:#777; margin: 30px 0;">${langDict[currentLang]['empty_history']}</p>`;
          return;
      }
      
      let html = '';
      window.appHistory.forEach(item => {
          html += `<div style="background: #f8fafc; padding: 15px; border-radius: 6px; border-left: 4px solid #0055a5; margin-bottom: 15px; box-shadow: 0 2px 5px rgba(0,0,0,0.05);">
              <div style="display:flex; justify-content:space-between; margin-bottom:8px;">
                  <strong style="color: #002244;">${item.type}</strong>
                  <span style="font-size: 12px; color: #777;">${item.date}</span>
              </div>
              <div style="font-size: 13px; color: #555; margin-bottom: 8px;"><strong>Wejście:</strong><br>${item.params.replace(/\n/g, '<br>')}</div>
              <div style="font-size: 14px; color: #d9534f; font-weight: bold;"><strong>Wynik:</strong><br>${item.results.replace(/\n/g, '<br>')}</div>
          </div>`;
      });
      list.innerHTML = html;
  }

  document.getElementById('clear-history-btn').addEventListener('click', function() {
      window.appHistory = [];
      persistHistory();
      renderHistory();
  });

  document.getElementById('show-about-btn').addEventListener('click', function(e) {
      e.preventDefault();
      document.querySelectorAll('.br-tab-btn').forEach(function(b) { b.classList.remove('active'); });
      document.querySelectorAll('.br-tab-content').forEach(function(c) { c.classList.remove('active'); });
      document.getElementById('tab-about').classList.add('active');
  });
  
  langSwitch.addEventListener('change', function(e) {
    var lang = e.target.value;
    document.querySelectorAll('[data-i18n]').forEach(function(el) {
      var key = el.getAttribute('data-i18n');
      if(langDict[lang] && langDict[lang][key]) { el.innerText = langDict[lang][key]; }
    });
    document.querySelectorAll('[data-i18n-ph]').forEach(function(el) {
      var key = el.getAttribute('data-i18n-ph');
      if(langDict[lang] && langDict[lang][key]) { el.placeholder = langDict[lang][key]; }
    });
    
    document.querySelectorAll('.btn-pdf-gen').forEach(btn => btn.innerText = langDict[lang]['btn_pdf']);
    document.querySelectorAll('.br-copy-btn[data-copy]').forEach(btn => btn.innerText = langDict[lang]['copy_btn']);
    renderHistory();
  });

  var userLang = navigator.language || navigator.userLanguage; 
  var langCode = userLang.split('-')[0].toLowerCase();
  var supportedLangs = ['pl', 'en', 'de', 'ro'];
  if (!supportedLangs.includes(langCode)) { langCode = 'en'; }
  langSwitch.value = langCode;
  langSwitch.dispatchEvent(new Event('change'));

  function showError(msgKey) {
    var toast = document.getElementById("toast");
    var currentLang = langSwitch.value;
    toast.innerText = langDict[currentLang][msgKey] || "Błąd / Error";
    toast.className = "show";
    setTimeout(function() { toast.className = toast.className.replace("show", ""); }, 3000);
  }

  document.querySelectorAll('input[type="number"]').forEach(function(input) {
    input.addEventListener('input', function() {
      if (this.value < 0) this.value = Math.abs(this.value);
    });
  });

  function copyToClipboard(text, btnId) {
    var textArea = document.createElement("textarea");
    textArea.value = text;
    textArea.style.position = "fixed";
    textArea.style.top = "-9999px";
    textArea.style.left = "-9999px";
    document.body.appendChild(textArea);
    textArea.focus();
    textArea.select();
    
    var successful = false;
    try { successful = document.execCommand('copy'); } 
    catch (err) { console.error('Nie udało się skopiować', err); }
    document.body.removeChild(textArea);
    
    if (successful) {
      var btn = document.getElementById(btnId);
      var originalText = btn.innerText;
      btn.innerText = "✓ OK!";
      btn.classList.add('success');
      setTimeout(function() {
        btn.innerText = originalText;
        btn.classList.remove('success');
      }, 2000);
    } else {
      showError('err_empty');
    }
  }

  var tabBtns = document.querySelectorAll('.br-tab-btn');
  var tabContents = document.querySelectorAll('.br-tab-content');
  tabBtns.forEach(function(btn) {
    btn.addEventListener('click', function(e) {
      e.preventDefault();
      tabBtns.forEach(function(b) { b.classList.remove('active'); });
      tabContents.forEach(function(c) { c.classList.remove('active'); });
      this.classList.add('active');
      document.getElementById(this.getAttribute('data-tab')).classList.add('active');
      if(this.getAttribute('data-tab') === 'tab-historia') { renderHistory(); }
    });
  });

  function createActionButtons(containerId, copyId, pdfId, paramsText, resultsText, moduleKey, printTitle) {
      let copyBtn = document.getElementById(copyId);
      let pdfBtn = document.getElementById(pdfId);
      let lang = langSwitch.value;
      
      if(!copyBtn) {
          document.getElementById(containerId).insertAdjacentHTML('beforeend', 
              `<button id="${copyId}" class="br-copy-btn" data-copy="true">${langDict[lang]['copy_btn']}</button>
               <button id="${pdfId}" class="br-copy-btn btn-pdf-gen" style="background-color: #e2e8f0; color: #002244; margin-top: 5px;">${langDict[lang]['btn_pdf']}</button>`
          );
          copyBtn = document.getElementById(copyId);
          pdfBtn = document.getElementById(pdfId);
      }
      
      copyBtn.style.display = 'block';
      pdfBtn.style.display = 'block';
      
      copyBtn.onclick = () => copyToClipboard(`${printTitle}\n--- Parametry ---\n${paramsText}\n--- Wynik ---\n${resultsText}`, copyId);
      pdfBtn.onclick = () => generatePDF(printTitle, paramsText, resultsText);
      
      saveToHistory(moduleKey, paramsText, resultsText);
  }

  // Obliczenia
  document.getElementById('run-calc-btn').addEventListener('click', function(e) {
    e.preventDefault(); 
    var p = parseFloat(document.getElementById('calc-pressure').value);
    var boreMm = parseFloat(document.getElementById('calc-bore').value);
    var rodMm = parseFloat(document.getElementById('calc-rod').value);
    
    if (isNaN(p) || isNaN(boreMm) || isNaN(rodMm)) return showError('err_empty');
    if (boreMm <= rodMm) return showError('err_bore');

    var aB = Math.PI * Math.pow((boreMm/10)/2, 2);
    var aR = Math.PI * Math.pow((rodMm/10)/2, 2);
    var pushForce = Math.round(p * aB * 1.0197);
    var pullForce = Math.round(p * (aB - aR) * 1.0197);
    
    document.getElementById('res-push').innerText = pushForce.toLocaleString('pl-PL');
    document.getElementById('res-pull').innerText = pullForce.toLocaleString('pl-PL');
    document.getElementById('calc-results').style.display = 'block';

    let pTxt = `Ciśnienie: ${p} bar\nTłok/Tłoczysko: ${boreMm} / ${rodMm} mm`;
    let rTxt = `Siła pchania: ${pushForce} kg\nSiła ciągnięcia: ${pullForce} kg`;
    createActionButtons('calc-results', 'copy-force', 'pdf-force', pTxt, rTxt, 'force_title', 'HCalculator | Siła Siłownika');
  });

  document.getElementById('calc-spd-btn').addEventListener('click', function(e) {
    e.preventDefault();
    var Q = parseFloat(document.getElementById('spd-flow').value);
    var D = parseFloat(document.getElementById('spd-bore').value);
    var d = parseFloat(document.getElementById('spd-rod').value);
    var s = parseFloat(document.getElementById('spd-stroke').value);
    
    if (isNaN(Q) || isNaN(D) || isNaN(d) || isNaN(s)) return showError('err_empty');
    if (D <= d) return showError('err_bore');

    var a1 = Math.PI * Math.pow((D/10)/2, 2); 
    var a2 = Math.PI * (Math.pow((D/10)/2, 2) - Math.pow((d/10)/2, 2));
    var Q_s = (Q * 1000) / 60;
    
    var vPush = (Q_s / a1).toFixed(2);
    var tPush = ((s/10) / (Q_s / a1)).toFixed(2);
    var vPull = (Q_s / a2).toFixed(2);
    var tPull = ((s/10) / (Q_s / a2)).toFixed(2);

    document.getElementById('res-v-push').innerText = vPush;
    document.getElementById('res-t-push').innerText = tPush;
    document.getElementById('res-v-pull').innerText = vPull;
    document.getElementById('res-t-pull').innerText = tPull;
    document.getElementById('spd-results').style.display = 'block';

    let pTxt = `Przepływ: ${Q} L/min\nTłok/Tłoczysko: ${D} / ${d} mm\nSkok: ${s} mm`;
    let rTxt = `Wysuw: ${tPush} s (Prędkość: ${vPush} cm/s)\nPowrót: ${tPull} s (Prędkość: ${vPull} cm/s)`;
    createActionButtons('spd-results', 'copy-speed', 'pdf-speed', pTxt, rTxt, 'speed_title', 'HCalculator | Prędkość i Czas Cyklu');
  });

  document.getElementById('calc-pmp-btn').addEventListener('click', function(e) {
    e.preventDefault();
    var Q = parseFloat(document.getElementById('pmp-flow').value);
    var p = parseFloat(document.getElementById('pmp-pressure').value);
    var eff = parseFloat(document.getElementById('pmp-eff').value);
    
    if (isNaN(Q) || isNaN(p)) return showError('err_empty');

    var kw = ((Q * p) / (600 * eff)).toFixed(2);
    var km = (kw * 1.36).toFixed(2);
    
    document.getElementById('res-kw').innerText = kw;
    document.getElementById('res-km').innerText = km;
    document.getElementById('pmp-results').style.display = 'block';

    let pTxt = `Wydajność pompy: ${Q} L/min\nCiśnienie: ${p} bar`;
    let rTxt = `Wymagana moc: ${kw} kW (${km} KM/HP)`;
    createActionButtons('pmp-results', 'copy-power', 'pdf-power', pTxt, rTxt, 'power_title', 'HCalculator | Moc Napędu Pompy');
  });

  var rSel = document.getElementById('flow-rpm-select');
  var rCus = document.getElementById('flow-rpm-custom');
  rSel.addEventListener('change', function() { rCus.style.display = (this.value === 'custom') ? 'block' : 'none'; });

  document.getElementById('calc-flow-btn').addEventListener('click', function(e) {
    e.preventDefault();
    var V = parseFloat(document.getElementById('flow-disp').value);
    var eff = parseFloat(document.getElementById('flow-eff').value);
    var rpm = (rSel.value === 'custom') ? parseFloat(rCus.value) : parseFloat(rSel.value);
    
    if (isNaN(V) || isNaN(rpm)) return showError('err_empty');

    var theo = ((V * rpm) / 1000).toFixed(1);
    var actual = (theo * eff).toFixed(1);
    
    document.getElementById('res-flow-theo').innerText = theo;
    document.getElementById('res-flow-actual').innerText = actual;
    document.getElementById('flow-results').style.display = 'block';

    let pTxt = `Chłonność: ${V} cm³/obr\nObroty napędu: ${rpm} obr/min`;
    let rTxt = `Rzeczywista wydajność: ${actual} L/min\n(Teoretyczna: ${theo} L/min)`;
    createActionButtons('flow-results', 'copy-flow', 'pdf-flow', pTxt, rTxt, 'flow_title', 'HCalculator | Wydajność Pompy');
  });

  document.getElementById('calc-tank-btn').addEventListener('click', function(e) {
    e.preventDefault();
    var Q = parseFloat(document.getElementById('tank-flow').value);
    var type = document.getElementById('tank-type').value;
    
    if (isNaN(Q)) return showError('err_empty');

    var minM = (type === 'mobile') ? 2 : (type === 'industrial' ? 3 : 1);
    var maxM = (type === 'mobile') ? 3 : (type === 'industrial' ? 5 : 1.5);
    var resultRange = Math.round(Q * minM) + " - " + Math.round(Q * maxM);
    
    document.getElementById('res-tank-range').innerText = resultRange;
    document.getElementById('tank-results').style.display = 'block';

    let pTxt = `Wydajność pompy: ${Q} L/min\nTyp układu: ${type}`;
    let rTxt = `Rekomendowana pojemność: ${resultRange} litrów`;
    createActionButtons('tank-results', 'copy-tank', 'pdf-tank', pTxt, rTxt, 'tank_title', 'HCalculator | Pojemność Zbiornika');
  });

  // --- INICJALIZACJA I POBRANIE TRWAŁEJ HISTORII Z PYTHONA ---
  window.addEventListener('pywebviewready', async function() {
      try {
          let h = await window.pywebview.api.load_history();
          window.appHistory = JSON.parse(h || "[]");
      } catch (e) {
          window.appHistory = JSON.parse(localStorage.getItem('hcalc_history') || "[]");
      }
      renderHistory();
  });
  
});
</script>
</body>
</html>
"""

class Api:
    def __init__(self):
        # Historia będzie zapisywana w bezpiecznym pliku w katalogu domowym użytkownika
        self.history_file = os.path.join(os.path.expanduser('~'), '.hcalc_history.json')

    def open_url(self, url):
        import webbrowser
        webbrowser.open(url)
        
    def save_history(self, history_json):
        try:
            with open(self.history_file, 'w', encoding='utf-8') as f:
                f.write(history_json)
        except Exception as e:
            print("Błąd zapisu historii:", e)

    def load_history(self):
        try:
            if os.path.exists(self.history_file):
                with open(self.history_file, 'r', encoding='utf-8') as f:
                    return f.read()
        except Exception as e:
            print("Błąd odczytu historii:", e)
        return "[]"

if __name__ == '__main__':
    api = Api()
    webview.create_window(
        title='HCalculator - Hydraulic Calculator', 
        html=html_content, 
        js_api=api,
        width=580, 
        height=850,
        min_size=(450, 600)
    )
    webview.start()
    
    os._exit(0)