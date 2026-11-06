"""Punto de entrada: `python main.py` (dev) o el ejecutable generado por packaging/UI_ComplexCalc.spec."""
from ui.app import FasorCalculator


def main():
    FasorCalculator().mainloop()


if __name__ == "__main__":
    main()
