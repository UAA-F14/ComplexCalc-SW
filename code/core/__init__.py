"""Lógica de negocio sin UI. API pública re-exportada aquí; ver AGENTS.md."""
from .calculator import FasorCalculatorCore
from .formatting import complejo_a_fasor, complejo_rect, format_rect_result
from .parsing import evaluate_expression, parse_value
from .solver import solve_from_strings
from .storage import load_saved_items, save_system

__all__ = [
    "FasorCalculatorCore", "complejo_a_fasor", "complejo_rect", "format_rect_result",
    "parse_value", "evaluate_expression", "solve_from_strings", "save_system", "load_saved_items",
]
