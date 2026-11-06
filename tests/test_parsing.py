def test_cell_expressions(self):
    cases = {
        "2*(3+4j)": 6 + 8j,
        "(1+2j)^2": -3 + 4j,
        "10L0/2": 5 + 0j,
        "5-10L0": -5 + 0j,
        "10L90+5": 5 + 10j,
        "2j*3j": -6 + 0j,
        "1/2": 0.5 + 0j,
    }
    for text, expected in cases.items():
        with self.subTest(text=text):
            self.assertAlmostEqual(parse_value(text), expected)

def test_cell_expressions_invalid(self):
    for bad in ["2*", "(1+2j", "1/0", "abc", "10L", "__import__('os')"]:
        with self.subTest(text=bad):
            with self.assertRaises(ValueError):
                parse_value(bad)

# test_solver.py
def test_solve_with_expressions(self):
    r = solve_from_strings([["2*1", "0"], ["0", "10L0/5"]], ["4", "1+1"])
    self.assertAlmostEqual(r["x"][0], 2)
    self.assertAlmostEqual(r["x"][1], 1)

def test_error_names_the_cell(self):
    with self.assertRaisesRegex(ValueError, r"A\[1,2\]"):
        solve_from_strings([["1", "xx"], ["0", "1"]], ["1", "1"])