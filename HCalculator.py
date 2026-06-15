#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# ==============================================================================
# Nazwa pliku: HCalculator.py
# 
# Copyright (c) 2026 Daniel Kaliski
# Ten kod jest objęty licencją GNU GENERAL PUBLIC LICENSE GPL-3.0.
# Pełny tekst licencji znajduje się w pliku LICENSE lub na stronie:
# https://opensource.org/license/gpl-3.0
# ==============================================================================

import urllib.request
import json
import webview
import sys
import os
import base64
import re
class Api:
    def __init__(self):
        self.history_file = os.path.join(os.path.expanduser('~'), '.hcalc_history.json')
        self.theme_file = os.path.join(os.path.expanduser('~'), '.hcalc_theme.txt')

    def open_url(self, url):
        import webbrowser
        webbrowser.open(url)
        
    def save_history(self, history_json):
        try:
            with open(self.history_file, 'w', encoding='utf-8') as f:
                f.write(history_json)
        except Exception as e:
            pass

    def load_history(self):
        try:
            if os.path.exists(self.history_file):
                with open(self.history_file, 'r', encoding='utf-8') as f:
                    return f.read()
        except Exception as e:
            pass
        return "[]"

    def save_theme(self, theme):
        try:
            with open(self.theme_file, 'w', encoding='utf-8') as f:
                f.write(theme)
        except Exception as e:
            pass

    def load_theme(self):
        try:
            if os.path.exists(self.theme_file):
                with open(self.theme_file, 'r', encoding='utf-8') as f:
                    return f.read().strip()
        except Exception as e:
            pass
        return "auto"

    
    def save_png(self, title, b64_data):
        try:

            if "," in b64_data:
                b64_data = b64_data.split(",")[1]
                
            file_data = base64.b64decode(b64_data)
            window = webview.windows[0]
        
            safe_title = re.sub(r'[\\/*?:"<>|]', "-", title)
            # Zamiana spacji na podkreślniki
            save_filename = f"{safe_title.replace(' ', '_')}.png"
            
            result = window.create_file_dialog(
                webview.SAVE_DIALOG, 
                directory='', 
                save_filename=save_filename
            )
            
            if result:
                file_path = result[0] if isinstance(result, (tuple, list)) else result
                
                if not file_path.lower().endswith('.png'):
                    file_path += '.png'
                    
                with open(file_path, 'wb') as f:
                    f.write(file_data)
        except Exception as e:
            print("Błąd zapisu PNG z poziomu Pythona:", e)

    def check_update(self, current_version):
        repo = "daniel-kaliski/HCalculator"
        url = f"https://api.github.com/repos/{repo}/releases/latest"
        try:
            req = urllib.request.Request(url, headers={'User-Agent': 'HCalculator-App'})
            with urllib.request.urlopen(req, timeout=3) as response:
                data = json.loads(response.read().decode())
                latest_version = data.get('tag_name', '').lstrip('v')
                current_version_clean = current_version.lstrip('v')
                l_parts = [int(x) for x in latest_version.split('.')]
                c_parts = [int(x) for x in current_version_clean.split('.')]
                if l_parts > c_parts:
                    return {
                        "update_available": True,
                        "latest_version": latest_version,
                        "url": data.get('html_url')
                    }
        except Exception as e:
            pass
        return {"update_available": False}


def get_resource_path(relative_path):
    """Zwraca absolutną ścieżkę do zasobów, odporną na strukturę macOS .app"""
    if getattr(sys, 'frozen', False):
        
        base_path = getattr(sys, '_MEIPASS', os.path.dirname(sys.executable))
        
       
        mac_resources = os.path.join(os.path.dirname(sys.executable), '..', 'Resources')
        if os.path.exists(os.path.join(mac_resources, relative_path)):
            return os.path.join(mac_resources, relative_path)
            
        return os.path.join(base_path, relative_path)
        
    return os.path.join(os.path.dirname(os.path.abspath(__file__)), relative_path)


if __name__ == '__main__':
    api = Api()
    
    
    html_path = get_resource_path('index.html')
    
    webview.create_window(
        title='HCalculator - Hydraulic Calculator v1.1.4', 
        url=html_path, 
        js_api=api,
        width=600,       
        height=800,      
        resizable=False  
    )
    
    # UWAGA: Uruchomienie z wbudowanym mikro-serwerem! 
    # Zapobiega to blokowaniu plików JS przez system bezpieczeństwa macOS.
    webview.start(http_server=True)
    os._exit(0)