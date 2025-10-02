# -*- mode: python ; coding: utf-8 -*-

import sys
import os
from PyInstaller.utils.hooks import collect_submodules

# Path to your script
script_path = 'conector_cordiax.py'

# Data files to embed in the exe
datas = [
    ('alarm.wav', '.'),  # Will be accessible via resource_path
    ('ring.wav', '.')
]

# Hidden imports that PyInstaller may not detect automatically
hiddenimports = collect_submodules('pystray') + [
    'PIL._tkinter_finder',
    'requests',
    'playsound',
]

block_cipher = None

a = Analysis(
    [script_path],
    pathex=[os.path.abspath('.')],  
    binaries=[],
    datas=datas,
    hiddenimports=hiddenimports,
    hookspath=[],
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='ConectorCordiax',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,  # Hide console window
)
