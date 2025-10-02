# -*- mode: python ; coding: utf-8 -*-

import sys
import os

# ----- Path to your script -----
script_path = 'conector_cordiax.py'

# ----- Data files -----
# Adjust these paths if your sound files are located elsewhere
datas = [
    ('alarm.wav', '.'),  # Source file, destination folder
    ('ring.wav', '.')
]

# ----- Hidden imports -----
# PyInstaller sometimes needs explicit imports for pystray & PIL
hiddenimports = [
    'PIL._tkinter_finder',
    'pystray._win32',
    'requests',
    'playsound',
]

# ----- PyInstaller build spec -----
block_cipher = None

a = Analysis(
    [script_path],
    pathex=[os.path.abspath('.')],  # Current directory
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
    console=False  # Hide console window
)

coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='ConectorCordiax'
)
