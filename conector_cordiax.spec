# -*- mode: python ; coding: utf-8 -*-

import sys
import os
from PyInstaller.utils.hooks import collect_submodules, collect_dynamic_libs
from PyInstaller.utils.win32 import get_system_path

block_cipher = None

# 1️⃣ Hidden imports
hidden_imports = collect_submodules('pystray')

# 2️⃣ Data files
datas = [
    ('ring.wav', '.'),
    ('alarm.wav', '.')
]

# 3️⃣ Collect dynamic libraries from dependencies
binaries = []
for pkg in ['PIL', 'pystray']:
    binaries += collect_dynamic_libs(pkg)

# 4️⃣ Include Python DLL
python_dll_name = f'python{sys.version_info.major}{sys.version_info.minor}.dll'
python_dll_path = os.path.join(sys.base_prefix, python_dll_name)
if os.path.exists(python_dll_path):
    binaries.append((python_dll_path, ''))

# 5️⃣ Include MSVC runtime DLLs automatically
msvc_dlls = ['vcruntime140.dll', 'vcruntime140_1.dll', 'ucrtbase.dll']
for dll in msvc_dlls:
    dll_path = get_system_path(dll)
    if dll_path and os.path.exists(dll_path):
        binaries.append((dll_path, ''))

# 6️⃣ Analysis
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

# 7️⃣ Package pure Python code
pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

# 8️⃣ EXE creation with UPX compression enabled
exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=False,
    name='ConectorCordiax',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,           # Enable UPX compression for all binaries
    console=False,      # GUI only
    icon=None,          # Optional icon path
    onefile=True        # Single EXE
)
