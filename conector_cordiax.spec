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

# Collect DLLs from Pillow and pystray
binaries = collect_dynamic_libs('PIL') + collect_dynamic_libs('pystray')

# Include python311.dll manually (use '.' for top-level)
python_dll = os.path.join(sys.base_prefix, 'python311.dll')
if os.path.exists(python_dll):
    binaries.append((python_dll, '.'))

# Manually include MSVC runtime DLLs (also use '.')
msvc_dlls = ['vcruntime140.dll', 'vcruntime140_1.dll', 'ucrtbase.dll']

for dll in msvc_dlls:
    dll_path = os.path.join(sys.base_prefix, 'DLLs', dll)
    if not os.path.exists(dll_path):
        # Try the system32 folder if not found
        dll_path = os.path.join(os.environ.get('SystemRoot', r'C:\Windows'), 'System32', dll)
    if os.path.exists(dll_path):
        binaries.append((dll_path, '.'))

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
    upx=True,           # UPX compression
    console=False,      # GUI only
    icon=None,          # Optional icon
    onefile=True        # Single EXE
)
