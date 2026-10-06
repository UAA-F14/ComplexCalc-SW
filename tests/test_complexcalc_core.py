"""
Robustness tests for FasorCalculatorCore (the parsing/solving/persistence
logic behind the GUI). Goal: no input should ever raise anything other than
a clean, catchable Exception — the GUI wraps every call in try/except and
shows a messagebox, so an uncaught crash here would be an uncaught crash
in the app too.

Run with:
    python3 -m unittest discover -s tests
"""
import math
import os
import sys
import tempfile
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "code"))

from ComplexCalc import FasorCalculatorCore, complejo_a_fasor, complejo_rect


class ParseValueValidInputs(unittest.TestCase):
    def setUp(self):
        self.core = FasorCalculatorCore()

    def assertComplexClose(self, actual, expected, msg=None):
        self.assertAlmostEqual(actual.real, expected.real, places=6, msg=msg)
        self.assertAlmostEqual(actual.imag, expected.imag, places=6, msg=msg)

    def test_rectangular_forms(self):
        cases = {
            "3+4j": 3 + 4j,
            "-j2": -2j,
            "5": 5 + 0j,
            "2+1i": 2 + 1j,
            "1.2-3j": 1.2 - 3j,
            "j": 1j,
            "-j": -1j,
            "+j": 1j,
        }
        for text, expected in cases.items():
            with self.subTest(text=text):
                self.assertComplexClose(self.core.parse_value(text), expected)

    def test_phasor_forms(self):
        r, ang = 10, math.radians(30)
        expected = r * complex(math.cos(ang), math.sin(ang))
        self.assertComplexClose(self.core.parse_value("10L30"), expected)
        self.assertComplexClose(self.core.parse_value("10L30°"), expected)
        self.assertComplexClose(self.core.parse_value("10∠30"), expected)

    def test_negative_angle_phasor(self):
        r, ang = 5, math.radians(-90)
        expected = r * complex(math.cos(ang), math.sin(ang))
        self.assertComplexClose(self.core.parse_value("5L-90"), expected)


class ParseValueInvalidInputs(unittest.TestCase):
    """Every one of these must raise ValueError, never an unhandled crash."""

    def setUp(self):
        self.core = FasorCalculatorCore()

    def test_garbage_and_edge_strings(self):
        bad_inputs = [
            "", "   ", "abc", "10L", "LL30", "3++4j", "j-j-j",
            "10L30L45", "----", "3 + 4 j garbage", "∠∠5", "5LL", None,
        ]
        for bad in bad_inputs:
            with self.subTest(bad=bad):
                with self.assertRaises(ValueError):
                    self.core.parse_value(bad)


class SolveFromStringsTests(unittest.TestCase):
    def setUp(self):
        self.core = FasorCalculatorCore()

    def test_well_posed_system(self):
        A = [["1", "0"], ["0", "1"]]
        b = ["3+4j", "1L90"]
        result = self.core.solve_from_strings(A, b)
        self.assertAlmostEqual(result["x"][0].real, 3, places=6)
        self.assertAlmostEqual(result["x"][0].imag, 4, places=6)
        self.assertAlmostEqual(result["x"][1].real, 0, places=6)
        self.assertAlmostEqual(result["x"][1].imag, 1, places=6)

    def test_singular_matrix_raises_not_crashes(self):
        A = [["1", "1"], ["1", "1"]]
        b = ["1", "1"]
        with self.assertRaises(Exception):
            self.core.solve_from_strings(A, b)

    def test_empty_system_raises_value_error(self):
        with self.assertRaises(ValueError):
            self.core.solve_from_strings([], [])

    def test_oversized_system_raises_value_error(self):
        n = 11
        A = [["1" if i == j else "0" for j in range(n)] for i in range(n)]
        b = ["1"] * n
        with self.assertRaises(ValueError):
            self.core.solve_from_strings(A, b)

    def test_malformed_entry_raises_not_crashes(self):
        A = [["1", "0"], ["0", "not_a_number"]]
        b = ["1", "1"]
        with self.assertRaises(Exception):
            self.core.solve_from_strings(A, b)

    def test_ragged_matrix_raises_not_crashes(self):
        # b implies size 2, but A only has one row -> should raise, not IndexError-crash unhandled
        A = [["1", "0"]]
        b = ["1", "1"]
        with self.assertRaises(Exception):
            self.core.solve_from_strings(A, b)

    def test_max_allowed_size_10x10_solves(self):
        n = 10
        A = [["1" if i == j else "0" for j in range(n)] for i in range(n)]
        b = [str(i + 1) for i in range(n)]
        result = self.core.solve_from_strings(A, b)
        for i in range(n):
            self.assertAlmostEqual(result["x"][i].real, i + 1, places=6)


class PersistenceTests(unittest.TestCase):
    """Save/import round-trip using temp files so the real saved_systems.txt is untouched."""

    def setUp(self):
        self.tmpdir = tempfile.mkdtemp()
        self.saved_path = os.path.join(self.tmpdir, "saved_systems.txt")
        self.exported_path = os.path.join(self.tmpdir, "exported_systems.py")
        self.core = FasorCalculatorCore(saved_filename=self.saved_path, exported_py=self.exported_path)

    def test_save_then_load_round_trip(self):
        A = [["1", "0"], ["0", "1"]]
        b = ["3+4j", "1L90"]
        result = self.core.solve_from_strings(A, b)
        self.core.save_system(result)

        loaded = self.core.load_saved_items()
        self.assertEqual(len(loaded), 1)
        self.assertEqual(loaded[0]["size"], 2)

    def test_import_from_missing_file_returns_empty(self):
        missing = os.path.join(self.tmpdir, "does_not_exist.txt")
        self.assertEqual(self.core.import_from_file(missing), [])

    def test_import_from_corrupted_file_skips_bad_entries(self):
        with open(self.saved_path, "w", encoding="utf-8") as f:
            f.write("{not valid json}\n\n")
            f.write('{"timestamp": "t", "size": 1}\n\n')
        loaded = self.core.load_saved_items()
        self.assertEqual(len(loaded), 1)


class FormattingTests(unittest.TestCase):
    def test_complejo_a_fasor_and_rect_do_not_crash_on_zero(self):
        z = 0 + 0j
        self.assertIn("0", complejo_a_fasor(z))
        self.assertIn("0", complejo_rect(z))


class EvaluateExpressionTests(unittest.TestCase):
    """The standalone calculator's expression evaluator — must handle
    phasors combined with operators, not just a single standalone phasor
    (that's all parse_value ever supported, since matrix/vector cells are
    always a single value)."""

    def setUp(self):
        self.core = FasorCalculatorCore()

    def assertComplexClose(self, actual, expected, msg=None):
        self.assertAlmostEqual(actual.real, expected.real, places=6, msg=msg)
        self.assertAlmostEqual(actual.imag, expected.imag, places=6, msg=msg)

    def test_empty_and_zero_input(self):
        self.assertComplexClose(self.core.evaluate_expression(""), 0j)
        self.assertComplexClose(self.core.evaluate_expression("0"), 0j)

    def test_plain_rectangular_arithmetic_still_works(self):
        self.assertComplexClose(self.core.evaluate_expression("3+4j+1+2j"), 4 + 6j)
        self.assertComplexClose(self.core.evaluate_expression("5-3j"), 5 - 3j)
        self.assertComplexClose(self.core.evaluate_expression("2j*3j"), -6 + 0j)
        self.assertComplexClose(self.core.evaluate_expression("3+4i"), 3 + 4j)

    def test_bare_j_is_not_a_valid_python_literal_on_its_own(self):
        # "j" alone (or "-j", "3*j", "(j)"...) isn't a Python complex literal
        # -- only "<digits>j" is (e.g. "4j"); a bare 'j' is a NAME lookup and
        # raises NameError unless normalized to "1j" first.
        self.assertComplexClose(self.core.evaluate_expression("j"), 1j)
        self.assertComplexClose(self.core.evaluate_expression("-j"), -1j)
        self.assertComplexClose(self.core.evaluate_expression("+j"), 1j)
        self.assertComplexClose(self.core.evaluate_expression("3*j"), 3j)
        self.assertComplexClose(self.core.evaluate_expression("(j)"), 1j)
        self.assertComplexClose(self.core.evaluate_expression("2j+j"), 3j)
        self.assertComplexClose(self.core.evaluate_expression("j*j"), -1 + 0j)
        self.assertComplexClose(self.core.evaluate_expression("1/j"), 1 / 1j)

    def test_j_before_its_coefficient(self):
        # "j5" / "-j1" style (imaginary unit written BEFORE the number) has
        # no Python literal at all -- must be rewritten to "5j" / "-1j"
        # first. Real bug report: "(2+3j)+(5-j1)" raised "Invalid expression".
        self.assertComplexClose(self.core.evaluate_expression("(2+3j)+(5-j1)"), (2 + 3j) + (5 - 1j))
        self.assertComplexClose(self.core.evaluate_expression("j1"), 1j)
        self.assertComplexClose(self.core.evaluate_expression("-j1"), -1j)
        self.assertComplexClose(self.core.evaluate_expression("j5"), 5j)
        self.assertComplexClose(self.core.evaluate_expression("j1.5"), 1.5j)
        self.assertComplexClose(self.core.evaluate_expression("5-j1"), 5 - 1j)
        self.assertComplexClose(self.core.evaluate_expression("3+j4"), 3 + 4j)
        self.assertComplexClose(self.core.evaluate_expression("(3+j4)*(1-j2)"), (3 + 4j) * (1 - 2j))

    def test_two_phasors_added(self):
        # 10∠30° + 5∠45°, computed independently for the expected value.
        p1 = 10 * complex(math.cos(math.radians(30)), math.sin(math.radians(30)))
        p2 = 5 * complex(math.cos(math.radians(45)), math.sin(math.radians(45)))
        self.assertComplexClose(self.core.evaluate_expression("10L30+5L45"), p1 + p2)

    def test_phasor_mixed_with_rectangular(self):
        p = 10 * complex(math.cos(math.radians(30)), math.sin(math.radians(30)))
        self.assertComplexClose(self.core.evaluate_expression("3+4j+10L30"), 3 + 4j + p)

    def test_phasor_multiplication(self):
        p1 = 2 * complex(math.cos(math.radians(0)), math.sin(math.radians(0)))
        p2 = 3 * complex(math.cos(math.radians(90)), math.sin(math.radians(90)))
        self.assertComplexClose(self.core.evaluate_expression("2L0*3L90"), p1 * p2)

    def test_negative_angle_phasor_in_expression(self):
        p1 = 5 * complex(math.cos(math.radians(-90)), math.sin(math.radians(-90)))
        p2 = 5 * complex(math.cos(math.radians(90)), math.sin(math.radians(90)))
        self.assertComplexClose(self.core.evaluate_expression("5L-90+5L90"), p1 + p2)

    def test_degree_symbol_and_angle_notation_in_expression(self):
        p1 = 10 * complex(math.cos(math.radians(30)), math.sin(math.radians(30)))
        p2 = 5 * complex(math.cos(math.radians(45)), math.sin(math.radians(45)))
        self.assertComplexClose(self.core.evaluate_expression("10L30°+5∠45"), p1 + p2)

    def test_exponent_operator(self):
        self.assertComplexClose(self.core.evaluate_expression("2^3"), 8 + 0j)

    def test_division_by_zero_raises_value_error(self):
        with self.assertRaises(ValueError):
            self.core.evaluate_expression("5/0")

    # ------------------------------------------------------------------
    # +, -, * across rectangular / phasor / mixed — the exact combinations
    # the reported bug ("no suma complejos o fasores") covers.
    # ------------------------------------------------------------------

    def _phasor(self, r, deg):
        return r * complex(math.cos(math.radians(deg)), math.sin(math.radians(deg)))

    def test_addition_rectangular(self):
        self.assertComplexClose(self.core.evaluate_expression("2+3j+4+5j"), 6 + 8j)

    def test_addition_phasor(self):
        expected = self._phasor(10, 30) + self._phasor(5, 45)
        self.assertComplexClose(self.core.evaluate_expression("10L30+5L45"), expected)

    def test_addition_mixed(self):
        expected = (2 + 3j) + self._phasor(5, 60)
        self.assertComplexClose(self.core.evaluate_expression("2+3j+5L60"), expected)

    def test_subtraction_rectangular(self):
        self.assertComplexClose(self.core.evaluate_expression("7+2j-3-1j"), 4 + 1j)

    def test_subtraction_phasor(self):
        expected = self._phasor(10, 60) - self._phasor(4, 20)
        self.assertComplexClose(self.core.evaluate_expression("10L60-4L20"), expected)

    def test_subtraction_mixed(self):
        expected = self._phasor(8, 15) - (1 + 1j)
        self.assertComplexClose(self.core.evaluate_expression("8L15-1-1j"), expected)

    def test_multiplication_rectangular(self):
        self.assertComplexClose(self.core.evaluate_expression("(2+3j)*(1-2j)"), (2 + 3j) * (1 - 2j))

    def test_multiplication_phasor(self):
        # magnitudes multiply, angles add — a classic AC-circuit identity.
        expected = self._phasor(2, 10) * self._phasor(3, 20)
        self.assertComplexClose(self.core.evaluate_expression("2L10*3L20"), expected)
        self.assertComplexClose(expected, self._phasor(6, 30))

    def test_multiplication_mixed(self):
        expected = (2 + 0j) * self._phasor(5, 40)
        self.assertComplexClose(self.core.evaluate_expression("2*5L40"), expected)

    def test_division_phasor(self):
        expected = self._phasor(10, 50) / self._phasor(2, 20)
        self.assertComplexClose(self.core.evaluate_expression("10L50/2L20"), expected)
        self.assertComplexClose(expected, self._phasor(5, 30))

    def test_malformed_expression_raises_value_error_not_crash(self):
        # Note: "3+++4" is deliberately NOT here — it's valid Python (chained
        # unary +), evaluates to 7, not an error.
        bad_inputs = ["10L", "LL30", "3+*4", "__import__('os')", "3+"]
        for bad in bad_inputs:
            with self.subTest(bad=bad):
                with self.assertRaises(ValueError):
                    self.core.evaluate_expression(bad)


if __name__ == "__main__":
    unittest.main()
