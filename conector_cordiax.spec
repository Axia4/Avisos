# -*- mode: python ; coding: utf-8 -*-

import sys
from PyInstaller.utils.hooks import collect_submodules, collect_dynamic_libs

block_cipher = None
hidden_imports = collect_submodules('pystray')

# Include your WAV files in the bundle
datas = [
    ('ring.wav', '.'), 
    ('alarm.wav', '.')
]

# Collect dynamic libraries (DLLs) from PIL/Pillow and pystray
binaries = []
binaries += collect_dynamic_libs('PIL')
binaries += collect_dynamic_libs('pystray')

a = Analysis(
    ['conector_cordiax.py'],
    pathex=[],
    binaries=binaries,
    datas=datas,
    hiddenimports=hidden_imports,
    hookspath=[],
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=False,
    name='ConectorCordiax',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,
    icon=None,
    onefile=True
)
