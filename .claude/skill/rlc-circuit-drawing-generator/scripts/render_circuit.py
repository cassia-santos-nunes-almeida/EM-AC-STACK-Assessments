#!/usr/bin/env python3
"""
Render a CircuiTikZ/TikZ .tex file to SVG.

This is a thin wrapper around shared/scripts/render_circuitikz.py.
For direct usage, prefer the shared script:

    python shared/scripts/render_circuitikz.py input.tex [output.svg]
    python shared/scripts/render_circuitikz.py --all directory/

This script is kept for backward compatibility with the skill interface.

Usage:
    python render_circuit.py input.tex output.svg
"""
import sys
import os
from pathlib import Path

# Add shared scripts to path
repo_root = Path(__file__).resolve().parent.parent.parent.parent
sys.path.insert(0, str(repo_root / "shared" / "scripts"))

from render_circuitikz import compile_tex_to_svg


def main():
    if len(sys.argv) < 2:
        print("Usage: python render_circuit.py input.tex [output.svg]")
        print("")
        print("Compiles a CircuiTikZ/TikZ .tex file to SVG via pdflatex + pdf2svg.")
        print("For batch mode, use: python shared/scripts/render_circuitikz.py --all directory/")
        sys.exit(1)

    tex_path = Path(sys.argv[1])
    if not tex_path.exists():
        print(f"Error: {tex_path} not found")
        sys.exit(1)

    if len(sys.argv) >= 3:
        svg_path = Path(sys.argv[2])
    else:
        svg_path = tex_path.with_suffix(".svg")

    if not compile_tex_to_svg(tex_path, svg_path):
        sys.exit(1)


if __name__ == "__main__":
    main()
