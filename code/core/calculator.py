"""Fachada FasorCalculatorCore: API estable para la UI y los tests; delega en los módulos de core/."""
from . import parsing, solver, storage


class FasorCalculatorCore:
    """Lógica independiente de UI. Los métodos lanzan excepciones; la UI muestra los mensajes."""

    def __init__(self, saved_filename="saved_systems.txt", exported_py="exported_systems.py", max_size=10):
        self.saved_filename = saved_filename
        self.exported_py = exported_py
        self.max_size = max_size

    def parse_value(self, text):
        return parsing.parse_value(text)

    def evaluate_expression(self, text):
        return parsing.evaluate_expression(text)

    def solve_from_strings(self, A_strings, b_strings):
        return solver.solve_from_strings(A_strings, b_strings, self.max_size)

    def save_system(self, result_dict):
        storage.save_system(result_dict, self.saved_filename, self.exported_py)

    def load_saved_items(self, file_path=None):
        return storage.load_saved_items(file_path or self.saved_filename)

    def import_from_file(self, file_path):
        return storage.load_saved_items(file_path)
