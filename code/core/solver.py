"""Resuelve Ax=b complejo a partir de cadenas y devuelve arreglos + formatos polar/rect."""
from datetime import datetime

import numpy as np

from .formatting import complejo_a_fasor, complejo_rect
from .parsing import parse_value


def solve_from_strings(A_strings, b_strings, max_size=10):
    """A_strings: lista de listas de str; b_strings: lista de str. Devuelve dict con
    timestamp, size, A/b/x (numpy) y A/b/x _polar / _rect (str)."""
    size = len(b_strings)
    if size == 0:
        raise ValueError("Empty system")
    if size > max_size:
        raise ValueError(f"Size {size} exceeds maximum {max_size}")

    rng = range(size)
    A = np.array([[parse_value(A_strings[i][j]) for j in rng] for i in rng], dtype=complex)
    b = np.array([parse_value(s) for s in b_strings], dtype=complex)
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
