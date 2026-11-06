"""Formato de números complejos (polar / rectangular). Sin dependencias de UI."""
import math


def complejo_a_fasor(z):
    """Forma polar 'r L ang°' (ángulo en grados, 4 cifras significativas)."""
    r = abs(z)
    ang = math.degrees(math.atan2(z.imag, z.real))
    return f"{r:.4g} L {ang:.4g}°"


def complejo_rect(z):
    """Forma rectangular 'a + bj' con 4 cifras significativas."""
    if z.imag > 0:
        return f"{z.real:.4g} + {z.imag:.4g}j"
    elif z.imag < 0:
        return f"{z.real:.4g} - {abs(z.imag):.4g}j"
    return f"{z.real:.4g} + 0j"


def format_rect_result(result):
    """Resultado de la calculadora en rectangular: real simple si imag ~ 0, si no 'a + bj'."""
    if isinstance(result, complex):
        if abs(result.imag) < 1e-10:
            return f"{result.real:.6g}"
        return complejo_rect(result)
    return f"{result:.6g}"
