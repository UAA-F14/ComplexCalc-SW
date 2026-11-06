"""Rutas de la app. Recursos empaquetados (solo lectura) vs datos del usuario (escribibles).

- resources/ viaja dentro del ejecutable (PyInstaller lo extrae en sys._MEIPASS).
- data/ queda junto al .exe (frozen) o junto al código (dev), para que los
  sistemas guardados sobrevivan entre ejecuciones (onefile extrae a un temp que se borra).
"""
import sys
from pathlib import Path

FROZEN = getattr(sys, "frozen", False)
ROOT = Path(__file__).resolve().parent
RESOURCES_DIR = Path(getattr(sys, "_MEIPASS", ROOT)) / "resources"
DATA_DIR = (Path(sys.executable).parent if FROZEN else ROOT) / "data"

SAVED_FILE = DATA_DIR / "saved_systems.txt"
EXPORT_FILE = DATA_DIR / "exported_systems.py"


def resource_path(name):
    return str(RESOURCES_DIR / name)
