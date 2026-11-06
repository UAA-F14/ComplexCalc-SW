"""Corre los tests y compila el ejecutable. Uso:  python packaging/build.py [--no-tests]"""
import subprocess
import sys
from pathlib import Path

CODE = Path(__file__).resolve().parent.parent  # code/


def run(*cmd):
    print("->", " ".join(cmd))
    subprocess.run(cmd, cwd=CODE, check=True)


if "--no-tests" not in sys.argv:
    run(sys.executable, "-m", "unittest", "discover", "-s", "../tests")
run(sys.executable, "-m", "PyInstaller", "packaging/UI_ComplexCalc.spec", "--noconfirm",
    "--distpath", "dist", "--workpath", "build")
print("Listo:", CODE / "dist")
