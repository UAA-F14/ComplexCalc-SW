"""Resuelve Ax=b complejo a partir de cadenas y devuelve arreglos + formatos polar/rect."""
from datetime import datetime

import numpy as np

from .formatting import complejo_a_fasor, complejo_rect
from .parsing import parse_value


def _parse_cell(text, label):
    """parse_value con la posición de la celda en el mensaje de error."""
    try:
        return parse_value(text)
    except ValueError as e:
        raise ValueError(f"{label}: {e}") from None


def solve_from_strings(A_strings, b_strings, max_size=10):
    """A_strings: lista de listas de str (valores o expresiones); b_strings: lista de str.
    Devuelve dict con timestamp, size, A/b/x (numpy) y A/b/x _polar / _rect (str)."""
    size = len(b_strings)
    if size == 0:
        raise ValueError("Empty system")
    if size > max_size:
        raise ValueError(f"Size {size} exceeds maximum {max_size}")

    rng = range(size)
    A = np.array([[_parse_cell(A_strings[i][j], f"A[{i + 1},{j + 1}]") for j in rng] for i in rng],
                 dtype=complex)
    b = np.array([_parse_cell(s, f"b[{i + 1}]") for i, s in enumerate(b_strings)], dtype=complex)
    x = np.linalg.solve(A, b)

    def fmt(fn, arr):
        return [[fn(z) for z in row] for row in arr] if arr.ndim == 2 else [fn(z) for z in arr]

    return {
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "size": size,
        "A": A, "b": b, "x": x,
        "A_polar": fmt(complejo_a_fasor, A), "b_polar": fmt(complejo_a_fasor, b), "x_polar": fmt(complejo_a_fasor, x),
        "A_rect": fmt(complejo_rect, A), "b_rect": fmt(complejo_rect, b), "x_rect": fmt(complejo_rect, x),
    }