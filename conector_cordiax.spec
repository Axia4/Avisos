# -*- mode: python ; coding: utf-8 -*-

import sys
import os
from PyInstaller.utils.hooks import collect_submodules, collect_dynamic_libs

block_cipher = None

# Hidden imports
hidden_imports = collect_submodules('pystray')

# Include WAV files
datas = [
    ('ring.wav', '.'), 
    ('alarm.wav', '.')
]

# Collect DLLs from Pillow
binaries = collect_dynamic_libs('PIL')
# Collect DLLs from pystray (if any)
binaries += collect_dynamic_libs('pystray')

# Add python311.dll manually
python_dll = os.path.join(sys.base_prefix, 'python311.dll')
if os.path.exists(python_dll):
    binaries.append((python_dll, '.'))

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
    console=False,       # GUI only
    icon=None,           # Optional: add your icon here
    onefile=True         # Single EXE
)
