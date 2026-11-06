# -*- mode: python ; coding: utf-8 -*-
"""Spec de PyInstaller (mismo archivo en Windows y Linux: compila para el SO donde corre).

    cd code
    python packaging/build.py            # corre tests + compila
    # o directo:
    pyinstaller packaging/UI_ComplexCalc.spec --noconfirm

Salida: code/dist/UI_ComplexCalc(.exe). Los paths son relativos a este spec (SPECPATH),
así que funciona desde cualquier directorio. Qué se empaqueta:
  - main.py + core/ + ui/ + paths.py  -> se detectan solos por los imports
  - resources/ (themes.json, languages.json, HK.jpg, IE.png) -> datas, en sys._MEIPASS/resources
  - assets de customtkinter (temas/fuentes) -> collect_data_files
  - data/ NO se empaqueta: se crea junto al ejecutable (ver paths.py) para que los guardados persistan
Si agregas un archivo a resources/ ya queda incluido; si agregas un paquete con imports
dinámicos, añádelo a hiddenimports (como PIL._tkinter_finder).
"""
from pathlib import Path

from PyInstaller.utils.hooks import collect_data_files

ROOT = Path(SPECPATH).parent  # code/

a = Analysis(
    [str(ROOT / "main.py")],
    pathex=[str(ROOT)],
    binaries=[],
    datas=[(str(ROOT / "resources"), "resources")] + collect_data_files("customtkinter"),
    hiddenimports=["PIL._tkinter_finder"],  # import dinámico de Pillow (ImageTk); sin él el .exe no abre
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=["matplotlib", "scipy", "pandas", "IPython", "pytest", "PyQt5", "PyQt6", "PySide2", "PySide6"],
    noarchive=False,
    optimize=0,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name="UI_ComplexCalc",
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
