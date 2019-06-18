from cx_Freeze import setup, Executable
import os.path
import sys

PYTHON_INSTALL_DIR = os.path.dirname(os.path.dirname(os.__file__))

includes = []
include_files = [r"C:/Program Files/Python36/DLLs/tcl86t.dll",
                 r"C:/Program Files/Python36/DLLs/tk86t.dll",
                ]


os.environ['TCL_LIBRARY'] = os.path.join(PYTHON_INSTALL_DIR, 'tcl', 'tcl8.6')
os.environ['TK_LIBRARY'] = os.path.join(PYTHON_INSTALL_DIR, 'tcl', 'tk8.6')
base = 'Win64GUI' if sys.platform == "win64" else None

setup(
    name = "Objectif_Terre",
    version = "2.0",
    description = "Jeu de reflexion",
    options={"build_exe": {"includes": includes, "include_files": include_files}},
    executables = [Executable("Objectif_Terre.py", base=base)],
    )