# -*- mode: python ; coding: utf-8 -*-
# ==============================================================================
# Nazwa pliku: HCalculator.spec
# 
# Copyright (c) 2026 Daniel Kaliski
# Ten kod jest objęty licencją GNU GENERAL PUBLIC LICENSE GPL-3.0.
# Pełny tekst licencji znajduje się w pliku LICENSE lub na stronie:
# https://opensource.org/license/gpl-3.0
# ==============================================================================

a = Analysis(
    ['HCalculator.py'],
    pathex=[],
    binaries=[],
    datas=[],
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=0,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='HCalculator',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements=None,
    icon=['HCalculator.icns'],
)
coll = COLLECT(
    exe,
    a.binaries,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='HCalculator',
)
app = BUNDLE(
    coll,
    name='HCalculator.app',
    icon='HCalculator.icns',
    bundle_identifier='com.danielkaliski.hcalculator',
    info_plist={
        'CFBundleName': 'HCalculator',
        'CFBundleDisplayName': 'HCalculator',
        'CFBundleExecutable': 'HCalculator',
        'CFBundlePackageType': 'APPL',
        'CFBundleShortVersionString': '1.0.4',
        'CFBundleVersion': '1.0.4',
        'NSHumanReadableCopyright': 'Copyright © 2026 Daniel Kaliski. Wszelkie prawa zastrzeżone.',
        'NSHighResolutionCapable': True,
    },
)