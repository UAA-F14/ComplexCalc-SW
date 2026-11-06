"""Parseo de valores y expresiones complejas (rectangular, 'i'/'j', fasores 'rLθ')."""
import re

import numpy as np

# "j5" / "+j5" / "-j5" -> "5j" / "+5j" / "-5j". El lookbehind evita leer "5-j1" como "51j".
_J_BEFORE_DIGITS = re.compile(r"(?<!\d)([+-]?)j(\d+(?:\.\d+)?)")
# Fasor dentro de una expresión mayor. La magnitud no lleva signo propio:
# "5-10L30" = 5 menos el fasor 10∠30°, igual que "5-4j".
PHASOR_TOKEN = re.compile(r"(\d+(?:\.\d+)?)[Ll]([+-]?\d+(?:\.\d+)?)°?")


def parse_value(text: str) -> complex:
    """Parsea UN valor (celda de matriz/vector): '3+4j', '-j2', '1.2-3i', '10L30°', '10∠30'."""
    t = (text or "").strip()
    if not t:
        raise ValueError("Empty value")
    t = t.replace(" ", "").replace("∠", "L")

    if "L" in t:
        r, ang = t.split("L", 1)
        r = float(r)
        ang = np.deg2rad(float(ang.rstrip("°")))
        return r * (np.cos(ang) + 1j * np.sin(ang))

    t = re.sub(r"(?i)i", "j", t)
    t = _J_BEFORE_DIGITS.sub(r"\1\2j", t)
    t = t.replace("+j", "+1j").replace("-j", "-1j")
    t = re.sub(r"^j", "1j", t)
    try:
        return complex(t)
    except Exception:
        try:
            return complex(float(t), 0)
        except Exception:
            raise ValueError(f"Invalid complex value: {text}")


def evaluate_expression(text: str) -> complex:
    """Evalúa una expresión completa que mezcla rectangular y fasores: '10L30+5L45', '2j*3j'.

    `parse_value` solo acepta un valor; esto es para la calculadora auxiliar (+ - * / ^).
    """
    t = (text or "").strip()
    if not t or t == "0":
        return 0j

    t = t.replace(" ", "").replace("∠", "L")
    t = re.sub(r"(?i)i", "j", t).replace("^", "**")
    t = _J_BEFORE_DIGITS.sub(r"\1\2j", t)
    # 'j' suelto (no precedido de dígito/punto) = 1j: "j", "-j", "3*j", "(j)", "2j+j"
    t = re.sub(r"(?<![\d.])j", "1j", t)

    def _phasor_to_literal(m):
        r, ang = float(m.group(1)), np.deg2rad(float(m.group(2)))
        # float(): con numpy>=2 un np.float64 se imprime "np.float64(...)" (NEP 51) y
        # su 'l' dispararía el chequeo de 'L' sobrante de abajo.
        return f"({float(r * np.cos(ang))!r}+{float(r * np.sin(ang))!r}j)"

    t = PHASOR_TOKEN.sub(_phasor_to_literal, t)
    if "L" in t.upper():
        raise ValueError(f"Invalid phasor in expression: {text}")

    try:
        return complex(eval(t, {"__builtins__": {}}))
    except ZeroDivisionError:
        raise ValueError("Division by zero")
    except Exception:
        raise ValueError(f"Invalid expression: {text}")
