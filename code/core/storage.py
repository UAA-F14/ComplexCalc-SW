"""Persistencia: guardado JSON (saved_systems.txt), export a .py y carga/importación."""
import json
import os
from datetime import datetime

_KEYS = ("A_polar", "b_polar", "x_polar", "A_rect", "b_rect", "x_rect")


def rect_to_complex(s):
    """'a + bj' -> complex; si no se puede convertir devuelve s tal cual."""
    try:
        return complex(s.replace(" ", ""))
    except Exception:
        return s


def _append(path, text):
    os.makedirs(os.path.dirname(os.path.abspath(path)), exist_ok=True)
    with open(path, "a", encoding="utf-8") as f:
        f.write(text)


def save_system(result, saved_filename, exported_py):
    """Agrega `result` (dict de solve_from_strings) a saved_filename (JSON + línea en blanco)
    y a exported_py (asignación Python con complejos)."""
    data = {"timestamp": result.get("timestamp"), "size": result.get("size")}
    data.update({k: result.get(k) for k in _KEYS})
    _append(saved_filename, json.dumps(data, ensure_ascii=False) + "\n\n")

    header_needed = not os.path.exists(exported_py) or os.path.getsize(exported_py) == 0
    py_dict = {
        "timestamp": result.get("timestamp"),
        "size": result.get("size"),
        "A": [[rect_to_complex(s) for s in row] for row in result.get("A_rect", [])],
        "b": [rect_to_complex(s) for s in result.get("b_rect", [])],
        "x": [rect_to_complex(s) for s in result.get("x_rect", [])],
    }
    varname = "system_" + datetime.now().strftime("%Y%m%d_%H%M%S")
    header = "# Exported systems from FasorCalculator\n\n" if header_needed else ""
    _append(exported_py, f"{header}{varname} = {py_dict}\n\n")


def load_saved_items(path):
    """Lista de entradas válidas del archivo (separadas por línea en blanco); [] si no existe."""
    if not os.path.exists(path):
        return []
    with open(path, "r", encoding="utf-8") as f:
        raw = f.read().strip()
    items = []
    for chunk in (c for c in raw.split("\n\n") if c.strip()):
        try:
            items.append(json.loads(chunk))
        except Exception:
            continue
    return items
